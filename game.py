import random
import asyncio
from base64 import b64decode
from textwrap import dedent
from discord import ChannelType

from board import Board
from playerstate import PlayerState

rps_options = ('Rock', 'Paper', 'Scissors')

class Game:

    def __init__(self, ch, wait_for, player1, player2):
        self.ch = ch
        self.wait_for = lambda event, check: wait_for(event, check=check)
        self.ps1, self.ps2 = PlayerState(player1), PlayerState(player2)
        self.board = Board()

    async def broadcast(self, text):
        await asyncio.wait((self.ch.send(text),
                            self.ps1.member.dm_channel.send(text),
                            self.ps2.member.dm_channel.send(text)))


    async def start(self):
        # gotta do this in a coro
        if not self.ps1.member.dm_channel:
            await self.ps1.member.create_dm()
        if not self.ps2.member.dm_channel:
            await self.ps2.member.create_dm()

        #Allow forfeit at any time
        done, pending = await asyncio.wait({self.main(), self.wait_for_ff()},
                                           return_when = asyncio.FIRST_COMPLETED)
        print('Game ended')
        for task in pending: task.cancel()

    async def wait_for_ff(self):
        message = await self.wait_for('message', self.is_ff)
        await self.broadcast(f"{message.author.display_name} has forfeit the match. {(self.ps1.member if message.author == self.ps2.member else self.ps2.member).display_name} wins!")

    def is_ff(self, message):
        return message.channel.type == ChannelType.private and message.content == 'ff'

    async def for_both(self, coro):
        f1 = asyncio.ensure_future(coro(self.ps1))
        f2 = asyncio.ensure_future(coro(self.ps2))
        return await f1, await f2

    async def name_opponent_to(self, player):
        opponent = self.ps1.member if player == self.ps2.member else self.ps2.member
        await player.dm_channel.send(f"Your opponent is {opponent.display_name}.")

    async def get_reaction_choice(self, member, msg, choices):
        ch = msg.channel
        async with ch.typing():
            for emoji in choices:
                await msg.add_reaction(emoji)
        def check(reaction, user):
            return user == member and reaction.message.id == msg.id and str(reaction.emoji) in choices
        reaction, _ = await self.wait_for('reaction_add', check)
        return ord(str(reaction.emoji))

    async def main(self):
        await self.broadcast("Selecting decks...")
        await self.for_both(self.select_deck)
        await self.broadcast("Determine turn order")
        rps_winner = await self.rps()
        prefers_right = await self.choose_side(rps_winner)
        if prefers_right ^ (rps_winner == self.ps2.member):
            self.ps1.member, self.ps2.member = self.ps2.member, self.ps1.member
        #so now player1 is left and player2 is right
        self.ps1.set_left()
        self.ps2.set_right()

        await self.show_board()

    async def rps(self):
        choice1, choice2 = await self.for_both(self.rps_to)
        diff = (choice1 - choice2) % 3
        if diff == 0:
            await self.broadcast(f"Both chose **{rps_options[choice1]}**! A tie!")
            return await self.rps()
        elif diff == 2:
            await self.broadcast(f"**{rps_options[choice2]}** beats **{rps_options[choice1]}**! {self.ps2.member.display_name} wins!")
            return self.ps2
        else:
            await self.broadcast(f"**{rps_options[choice1]}** beats **{rps_options[choice2]}**! {self.ps1.member.display_name} wins!")
            return self.ps1

    async def rps_to(self, player):
        ch = player.member.dm_channel
        msg = await ch.send("React to choose rock, paper, or scissors")
        choice = await self.get_reaction_choice(player.member, msg, '\u270a\u270b\u270c') - 0x270a
        await ch.send(f"You chose **{rps_options[choice]}**.")
        return choice

    async def choose_side(self, player):
        ch = player.member.dm_channel
        msg = await ch.send("Do you want first turn on the left, or second turn on the right?")
        choice = await self.get_reaction_choice(player.member, msg, '\U0001f448\U0001f449') - 0x1f448
        await self.broadcast(f"{player.member.display_name} has chosen the {('left', 'right')[choice]} side.")
        return choice

    async def show_board(self):
        text = f'''\
        ```
        {self.ps1.member.display_name}{self.ps2.member.display_name.rjust(50-len(self.ps1.member.display_name))}
        {self.ps1.display_mana()} HAND 4/6              HAND 4/6 {self.ps2.display_mana()}

        '''
        await self.broadcast(dedent(text) + self.board.render() + '```')

    async def select_deck(self, player):
        ch = player.member.dm_channel
        await ch.send("Paste a base64-encoded deck.")
        msg = await self.wait_for('message', lambda message: message.channel == ch and message.author == player.member)
        rawdeck = b64decode(msg.content).decode()
        player.deck.load_from_text(rawdeck)
import random
import asyncio
from discord import ChannelType

from board import Board

rps_options = ('Rock', 'Paper', 'Scissors')

class Game:

    def __init__(self, ch, wait_for, player1, player2):
        self.ch = ch
        self.wait_for = lambda event, check: wait_for(event, check=check)
        self.player1, self.player2 = player1, player2
        self.board = Board()

    async def broadcast(self, text):
        await asyncio.wait((self.ch.send(text),
                            self.player1.dm_channel.send(text),
                            self.player2.dm_channel.send(text)))


    async def start(self):
        # gotta do this in a coro
        if not self.player1.dm_channel:
            await self.player1.create_dm()
        if not self.player2.dm_channel:
            await self.player2.create_dm()

        #await self.broadcast("THE GAME IS BEGIN !!")

        #Allow forfeit at any time
        done, pending = await asyncio.wait({self.main(), self.wait_for_ff()},
                                           return_when = asyncio.FIRST_COMPLETED)
        print('game should be over...')
        for task in pending: task.cancel()

    async def wait_for_ff(self):
        message = await self.wait_for('message', self.is_ff)
        await self.broadcast(f"{message.author.display_name} has forfeit the match. {(self.player1 if message.author == self.player2 else self.player2).display_name} wins!")

    def is_ff(self, message):
        return message.channel.type == ChannelType.private and message.content == 'ff'

    async def for_both(self, coro):
        f1 = asyncio.ensure_future(coro(self.player1))
        f2 = asyncio.ensure_future(coro(self.player2))
        return await f1, await f2

    async def name_opponent_to(self, player):
        opponent = self.player1 if player == self.player2 else self.player2
        await player.dm_channel.send(f"Your opponent is {opponent.display_name}.")

    async def get_reaction_choice(self, player, msg, choices):
        ch = msg.channel
        async with ch.typing():
            for emoji in choices:
                await msg.add_reaction(emoji)
        def check(reaction, user):
            return user == player and reaction.message.id == msg.id and str(reaction.emoji) in choices
        reaction, _ = await self.wait_for('reaction_add', check)
        return ord(str(reaction.emoji))

    async def main(self):
        await self.broadcast("Rock, paper, scissors, shoot!")
        rps_winner = await self.rps()
        prefers_right = await self.choose_side(rps_winner)
        if prefers_right ^ (rps_winner == self.player2):
            self.player1, self.player2 = self.player2, self.player1
        #so now player1 is left and player2 is right
        await self.show_board()

    async def rps(self):
        choice1, choice2 = await self.for_both(self.rps_to)
        diff = (choice1 - choice2) % 3
        if diff == 0:
            await self.broadcast(f"Both chose **{rps_options[choice1]}**! A tie!")
            return await self.rps()
        elif diff == 2:
            await self.broadcast(f"**{rps_options[choice2]}** beats **{rps_options[choice1]}**! {self.player2.display_name} wins!")
            return self.player2
        else:
            await self.broadcast(f"**{rps_options[choice1]}** beats **{rps_options[choice2]}**! {self.player1.display_name} wins!")
            return self.player1

    async def rps_to(self, player):
        ch = player.dm_channel
        msg = await ch.send("React to choose rock, paper, or scissors")
        choice = await self.get_reaction_choice(player, msg, '\u270a\u270b\u270c') - 0x270a
        await ch.send(f"You chose **{rps_options[choice]}**.")
        return choice

    async def choose_side(self, player):
        ch = player.dm_channel
        msg = await ch.send("Do you want first turn on the left, or second turn on the right?")
        choice = await self.get_reaction_choice(player, msg, '\U0001f448\U0001f449') - 0x1f448
        await self.broadcast(f"{player.display_name} has chosen the {('left', 'right')[choice]} side.")
        return choice

    async def show_board(self):
        text = '''```PLAYER1NAME                             PLAYER2NAME
@@....... HAND 4/6               HAND 4/6 ......@@@

'''+self.board.render()+'```'
        await self.broadcast(text)
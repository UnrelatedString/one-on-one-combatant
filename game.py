import random
import asyncio
from discord import ChannelType

class Game:

    def __init__(self, ch, wait_for, player1, player2):
        self.ch = ch
        self.wait_for = lambda event, check: wait_for(event, check=check)
        self.player1, self.player2 = random.sample((player1, player2), 2)

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

        await self.broadcast("THE GAME IS BEGIN !!")

        #Allow forfeit at any time
        done, pending = await asyncio.wait({self.main(), self.wait_for_ff()},
                                           return_when = asyncio.FIRST_COMPLETED)
        print('game should be over...')
        for task in pending: task.cancel()

    async def wait_for_ff(self):
        message = await self.wait_for('message', self.is_ff)
        await self.broadcast(f"{message.author.display_name} has forfeit the match. {self.player1 if message.author == self.player2 else self.player2} wins!")

    def is_ff(self, message):
        return message.channel.type == ChannelType.private and message.content == 'ff'

    async def for_both(self, coro):
        f1 = asyncio.ensure_future(coro(self.player1))
        f2 = asyncio.ensure_future(coro(self.player2))
        return await f1, await f2

    async def name_opponent_to(self, player):
        opponent = self.player1 if player == self.player2 else self.player2
        await player.dm_channel.send(f"Your opponent is {opponent.display_name}.")

    async def main(self):
        await self.for_both(self.name_opponent_to)
        await asyncio.sleep(15)
        await self.broadcast("Fifteen seconds have passed and nobody gave up. Draw")

    async def rps(self):
        pass

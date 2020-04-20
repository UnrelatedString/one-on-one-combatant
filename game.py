import random
import asyncio

class Game:
    task = None

    def __init__(self, ch, player1, player2):
        self.ch = ch
        self.player1, self.player2 = random.sample((player1, player2), 2)

    async def start(self):
        self.task = asyncio.ensure_future(self.main())
        await asyncio.wait_for(self.task, None)

    async def main(self):
        await asyncio.sleep(30)
        await self.ch.send("Thirty seconds have passed and nobody gave up. Draw")

    def abort(self):
        self.task.cancel()

    async def forfeit(self, player):
        await self.ch.send(f"{self.player1 if player == self.player2 else self.player2} wins by default!")
        self.abort()
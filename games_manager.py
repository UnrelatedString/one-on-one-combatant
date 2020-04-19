from game import Game

class GamesManager:
    challenges = {} #Member: Member
    games = {} #Member: Game

    async def challenge(self, challenger, challenged):
        if challenger in self.challenges:
            return "You must wait for your first challenge to expire!"
        if challenger in self.games:
            return "You are already in game!"
        self.challenges[challenger] = challenged

    async def accept(self, challenger, challenged):
        if self.challenges.get(challenger, None) != challenged:
            return f"{challenger.display_name} has not challenged you!"
        if challenged in self.games:
            return "You are already in game!"
        del self.challenges[challenger]

    async def expire(self, challenger):
        if challenger in self.challenges:
            del self.challenges[challenger]
            return True
        else:
            return False

    async def start_game(self, ch, player1, player2):
        game = Game(ch, player1, player2)
        self.games[player1] = game
        self.games[player2] = game
        await game.start()
        del self.games[player1]
        if player2 in self.games: #could be playing myself
            del self.games[player2]
        await ch.send("GAME OVER")
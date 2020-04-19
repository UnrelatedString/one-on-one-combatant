class GamesManager:
    challenges = {} #user id: user id, maybe throw Guild in there
    games = {} #user id: Game

    async def challenge(self, challenger, challenged):
        if challenger.id in self.challenges:
            return "You must wait for your first challenge to expire!"
        if challenger.id in self.games:
            return "You are already in game!"
        self.challenges[challenger.id] = challenged.id

    async def accept(self, challenger, challenged):
        if self.challenges.get(challenger.id, None) != challenged.id:
            return f"{challenger.display_name} has not challenged you!"
        if challenged.id in self.games:
            return "You are already in game!"
        del self.challenges[challenger.id]

    async def expire(self, challenger):
        if challenger.id in self.challenges:
            del self.challenges[challenger.id]
            return True
        else:
            return False

    async def start_game(self, ch, player1, player2):
        await ch.send(f"{player1.display_name} ambushes {player2.display_name}, winning instantly. lul")
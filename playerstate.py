from deck import Deck

class PlayerState:
    def __init__(self, member):
        self.member = member
        self.deck = Deck()
        self.mana = 0

    def set_left(self):
        self.left = True
        self.max_mana = 2
        self.mana = self.max_mana

    def set_right(self):
        self.left = False
        self.max_mana = 3
        self.mana = self.max_mana

    def display_mana(self):
        return ('.' * (9 - self.max_mana) +
                'O' * (self.max_mana - self.mana) +
                '@' * self.mana)[::(-1)**self.left]
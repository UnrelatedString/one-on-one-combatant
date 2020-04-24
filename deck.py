from random import shuffle

class Deck:
    def __init__(self, cards = None):
        self.cards = cards or []

    def shuffle(self):
        shuffle(self.cards)

    def push_top(self, card):
        self.cards.append(card)

    def push_bottom(self, card):
        self.cards.insert(0, card)

    def shuffle_in(self, *cards):
        self.cards.extend(cards)
        self.shuffle()

    def load_from_text(self, text):
        for pair in text.split(','):
            count, card = map(int, pair.split(':'))
            self.cards.extend(card for _ in range(count))
        self.shuffle()
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value + self.suit}"

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def can_beat(self, other, trump_suit):
        values = ["6", "7", "8", "9", "10", "Валет", "Королева", "Король", "Туз"]
        if self.suit == trump_suit and other.suit != trump_suit:
            return True
        if self.suit == other.suit:
            return values.index(self.value) > values.index(other.value)
        return False

def create_deck():
    suits = ["Черви", "Бубны", "Пики", "Крести"]
    values = ["6", "7", "8", "9", "10", "Валет", "Королева", "Король", "Туз"]
    return [Card(suit, value) for suit in suits for value in values]

import unittest
from GameBase import *

class MyTestCase(unittest.TestCase):
    def test_creation_deck(self):
        deck = create_deck()
        self.assertEqual(len(deck), 36)
        suits = ["Черви", "Бубны", "Пики", "Крести"]
        values = ["6", "7", "8", "9", "10", "Валет", "Королева", "Король", "Туз"]
        for suit in suits:
            for value in values:
                self.assertIn(Card(suit,value), deck)

    def test_Card_Deck(self):
        card = Card('Черви', 'Туз')
        self.assertEqual('Черви', card.suit)
        self.assertEqual("Туз", card.value)
        self.assertEqual(str(card), card.value + card.suit)
        card1 = Card('Черви', 'Туз')
        card2 = Card('Черви', 'Туз')
        self.assertEqual(card1 == card2, True)
        card3 = Card('Черви', '10')
        self.assertEqual(card1 == card3, False)


if __name__ == '__main__':
    unittest.main()
import unittest
from GameBase import Card
from Game import Game

class MyTestCase(unittest.TestCase):
    def test_initial_deal(self):
        game = Game()
        self.assertEqual(len(game.player_hand), 6)
        self.assertEqual(len(game.bot_hand), 6)
        self.assertEqual(len(game.deck), 36 - 12 - 1)
        self.assertIsNotNone(game.trump_card)
        self.assertIn(game.trump_card.suit, ["Черви", "Бубны", "Пики", "Крести"])

    def test_player_move(self):
        game = Game()
        game.table = [Card("Крести", "6")]
        game.player_hand = [Card("Черви", "6")]
        game.trump_card = Card("Черви", "Туз")
        result = game.player_move(0)
        self.assertTrue(result)
        self.assertEqual(len(game.table), 2)
        self.assertEqual(len(game.player_hand), 0)

    def test_bot_move(self):
        game = Game()
        game.trump_card = Card('Черви', '6')
        game.table = [Card("Крести", "6")]
        game.bot_hand = [Card("Крести", "7"), Card("Бубны", "6")]
        result = game.bot_move()
        self.assertTrue(result)
        self.assertEqual(len(game.table), 2)
        self.assertEqual(len(game.bot_hand), 1)
        game.table = [Card("Крести", "Туз")]
        game.bot_hand = [Card("Бубны", "6")]
        result = game.bot_move()
        self.assertFalse(result)

    def test_draw_cards(self):
        game = Game()
        game.player_hand = [Card("Пики", "6")]
        game.bot_hand = [Card("Черви", "6")]
        game.deck = [Card("Бубны", "7"), Card("Крести", "8")]
        game.draw_cards()
        self.assertEqual(len(game.player_hand), 3)
        self.assertEqual(len(game.bot_hand), 1)
        self.assertEqual(len(game.deck), 0)

    def test_game_over(self):
        game = Game()
        game.bot_hand = []
        game.deck = []
        self.assertEqual(game.check_winner(), "Робот победил!")
        game.bot_hand = [Card("Пики", "6")]
        game.player_hand = []
        self.assertEqual(game.check_winner(), "Игрок победил!")

if __name__ == '__main__':
    unittest.main()

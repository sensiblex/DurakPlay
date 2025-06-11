import unittest
import logging
from Game import Game
from GameBase import Card

class TestErrorLogging(unittest.TestCase):
    def test_logging_on_invalid_move(self):
        game = Game()
        # "Мокаем" (подменяем) обработчик логов, чтобы перехватывать сообщения
        with self.assertLogs('game_errors', level='ERROR') as cm:
            game.player_move(-1) # Неверный ход
            # Проверяем, что в лог записалось сообщение
            self.assertEqual(len(cm.output), 1)
            self.assertIn("ERROR:game_errors:Invalid card index: -1", cm.output[0])

            # Пробуем сделать ход с индексом, выходящим за пределы
            game.player_move(10)
            self.assertEqual(len(cm.output), 2)
            self.assertIn("ERROR:game_errors:Invalid card index: 10", cm.output[1])

if __name__ == '__main__':
    unittest.main()
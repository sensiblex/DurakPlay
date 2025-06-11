import unittest
from GameBase import Card, create_deck
from Game import Game


class TestGameRules(unittest.TestCase):
    def setUp(self):
        # Настраиваем игру для каждого теста, чтобы иметь предсказуемое состояние
        self.game = Game()
        self.game.deck = create_deck()  # Пересоздаем колоду для контроля
        self.game.trump_card = self.game.deck.pop()  # Устанавливаем козырь

        # Убедимся, что у игроков есть карты для теста
        self.game.player_hand = [Card("Крести", "6"), Card("Черви", "Туз")]  # Игрок имеет козырь для отбоя
        self.game.bot_hand = [Card("Бубны", "6"), Card("Пики", "Туз")]

    def test_attacker_after_player_beats(self):
        # Игрок отбивается, он должен стать атакующим
        self.game.attacker = "bot"  # Бот атакует
        self.game.table = [Card("Крести", "6")]  # Карта, которую бот атаковал

        # Игрок отбивается
        player_card_index = next((i for i, card in enumerate(self.game.player_hand)
                                  if card.can_beat(self.game.table[0], self.game.trump_card.suit)), -1)

        self.assertNotEqual(player_card_index, -1, "Игрок должен иметь карту для отбоя в этом тесте")

        initial_player_hand_len = len(self.game.player_hand)
        initial_bot_hand_len = len(self.game.bot_hand)
        initial_deck_len = len(self.game.deck)

        self.game.player_move(player_card_index)  # Игрок делает ход (отбивается)

        # Проверяем, что стол очищен после отбоя
        self.assertEqual(len(self.game.table), 0)

        # Проверяем, что атакующий стал игроком
        self.assertEqual(self.game.attacker, "player")  # Ожидаем, что атакующий - игрок

        # Проверяем, что карты добираются
        self.assertGreater(len(self.game.player_hand), initial_player_hand_len - 1)
        self.assertGreater(len(self.game.bot_hand), initial_bot_hand_len)  # У бота тоже должны были добираться карты
        self.assertLess(len(self.game.deck), initial_deck_len)

    def test_attacker_after_bot_beats(self):
        # Бот отбивается, он должен стать атакующим
        self.game.attacker = "player"  # Игрок атакует
        self.game.table = [Card("Бубны", "6")]  # Карта, которую игрок атаковал

        # Бот отбивается
        initial_player_hand_len = len(self.game.player_hand)
        initial_bot_hand_len = len(self.game.bot_hand)
        initial_deck_len = len(self.game.deck)

        # Моделируем, что бот может отбиться
        original_bot_move = self.game.bot_move

        def mock_bot_move():
            # Заменяем реальный bot_move на мок, который всегда отбивается
            if self.game.table:
                # Находим карту в руке бота, которая может бить
                for i, card in enumerate(self.game.bot_hand):
                    if card.can_beat(self.game.table[0], self.game.trump_card.suit):
                        self.game.table.append(self.game.bot_hand.pop(i))
                        return True
            return False

        self.game.bot_move = mock_bot_move

        self.game.bot_move()  # Бот делает ход (отбивается)
        self.game.bot_move = original_bot_move  # Восстанавливаем оригинальный метод

        # Проверяем, что стол очищен после отбоя
        self.assertEqual(len(self.game.table), 0)

        # Проверяем, что атакующий стал ботом
        self.assertEqual(self.game.attacker, "bot")  # Ожидаем, что атакующий - бот

        # Проверяем, что карты добираются
        self.assertGreater(len(self.game.player_hand),
                           initial_player_hand_len)  # У игрока тоже должны были добираться карты
        self.assertGreater(len(self.game.bot_hand), initial_bot_hand_len - 1)
        self.assertLess(len(self.game.deck), initial_deck_len)
import unittest
from GameBase import Card, create_deck
from Game import Game
import random


class TestGameRules(unittest.TestCase):
    def setUp(self):
        # Настраиваем игру для каждого теста, чтобы иметь предсказуемое состояние
        self.game = Game()
        self.game.deck = []  # Очищаем колоду
        self.trump_card_test = Card("Черви", "6")  # Устанавливаем предсказуемый козырь
        self.game.trump_card = self.trump_card_test

        # Гарантируем, что у игрока есть карта, которой он может отбиться от Крести 6
        self.player_card_to_beat = Card("Крести", "7")
        self.player_trump_card = Card("Черви", "Туз")
        self.game.player_hand = [self.player_card_to_beat, self.player_trump_card,
                                 Card("Пики", "8"), Card("Бубны", "9"), Card("Черви", "Валет"),
                                 Card("Крести", "Король")]
        random.shuffle(self.game.player_hand)

        # Гарантируем, что у бота есть карта, которой он может отбиться от Бубны 6
        self.bot_card_to_beat = Card("Бубны", "7")
        self.bot_trump_card = Card("Черви", "Король")
        self.game.bot_hand = [self.bot_card_to_beat, self.bot_trump_card,
                              Card("Крести", "8"), Card("Пики", "9"), Card("Бубны", "Валет"), Card("Черви", "Туз")]
        random.shuffle(self.game.bot_hand)

        # Заполняем остальную колоду, чтобы draw_cards работал корректно
        all_cards = create_deck()
        for card in self.game.player_hand + self.game.bot_hand + [self.game.trump_card]:
            if card in all_cards:
                all_cards.remove(card)
        self.game.deck.extend(all_cards)
        random.shuffle(self.game.deck)

    def test_attacker_after_player_beats(self):
        # Игрок отбивается, он должен стать атакующим
        self.game.attacker = "bot"  # Бот атакует
        self.game.table = [Card("Крести", "6")]  # Карта, которую бот атаковал

        player_card_index = -1
        for i, card in enumerate(self.game.player_hand):
            if card.can_beat(self.game.table[0], self.game.trump_card.suit):
                player_card_index = i
                break

        self.assertNotEqual(player_card_index, -1, "Игрок должен иметь карту для отбоя в этом тесте")

        initial_player_hand_len = len(self.game.player_hand)
        initial_bot_hand_len = len(self.game.bot_hand)
        initial_deck_len = len(self.game.deck)

        self.game.player_move(player_card_index)  # Игрок делает ход (отбивается)
        self.game.end_round_success()  # Очищаем стол и добираем карты

        # *** НОВОЕ ДОБАВЛЕНИЕ ДЛЯ ТЕСТА ***
        # Вызываем новый метод для смены атакующего
        self.game.set_next_attacker_after_defense_success("player")
        # *** КОНЕЦ НОВОГО ДОБАВЛЕНИЯ ***

        # Проверяем, что стол очищен после отбоя
        self.assertEqual(len(self.game.table), 0)

        # Проверяем, что атакующий стал игроком
        self.assertEqual(self.game.attacker, "player")

        # Проверяем, что карты добираются
        self.assertGreater(len(self.game.player_hand), initial_player_hand_len - 1)
        self.assertGreaterEqual(len(self.game.bot_hand), initial_bot_hand_len)
        self.assertLess(len(self.game.deck), initial_deck_len)

    def test_attacker_after_bot_beats(self):
        # Бот отбивается, он должен стать атакующим
        self.game.attacker = "player"  # Игрок атакует
        self.game.table = [Card("Бубны", "6")]  # Карта, которую игрок атаковал

        initial_player_hand_len = len(self.game.player_hand)
        initial_bot_hand_len = len(self.game.bot_hand)
        initial_deck_len = len(self.game.deck)

        # Моделируем, что бот может отбиться
        original_bot_move = self.game.bot_move

        def mock_bot_move():
            if self.game.table:
                for i, card in enumerate(self.game.bot_hand):
                    if card.can_beat(self.game.table[0], self.game.trump_card.suit):
                        self.game.table.append(self.game.bot_hand.pop(i))
                        return True
            return False

        self.game.bot_move = mock_bot_move

        self.game.bot_move()  # Бот делает ход (отбивается)
        self.game.bot_move = original_bot_move  # Восстанавливаем оригинальный метод
        self.game.end_round_success()  # Очищаем стол и добираем карты

        # *** НОВОЕ ДОБАВЛЕНИЕ ДЛЯ ТЕСТА ***
        # Вызываем новый метод для смены атакующего
        self.game.set_next_attacker_after_defense_success("bot")
        # *** КОНЕЦ НОВОГО ДОБАВЛЕНИЯ ***

        # Проверяем, что стол очищен после отбоя
        self.assertEqual(len(self.game.table), 0)

        # Проверяем, что атакующий стал ботом
        self.assertEqual(self.game.attacker, "bot")

        # Проверяем, что карты добираются
        self.assertGreaterEqual(len(self.game.player_hand), initial_player_hand_len)
        self.assertGreater(len(self.game.bot_hand), initial_bot_hand_len - 1)
        self.assertLess(len(self.game.deck), initial_deck_len)
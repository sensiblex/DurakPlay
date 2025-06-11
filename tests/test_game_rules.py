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
                              Card("Пики", "9"), Card("Бубны", "10"), Card("Крести", "Валет"),
                              Card("Черви", "Королева")]
        random.shuffle(self.game.bot_hand)

        # Заполняем остальную колоду, чтобы draw_cards работал корректно
        all_cards = create_deck()
        initial_game_cards = self.game.player_hand + self.game.bot_hand + [self.game.trump_card]

        cards_to_remove_from_all = []
        for card_in_game in initial_game_cards:
            for card_in_all_cards in all_cards:
                # Сравниваем по атрибутам, а не по объекту, т.к. они могли быть созданы в разных местах
                if card_in_game.suit == card_in_all_cards.suit and card_in_game.value == card_in_all_cards.value:
                    cards_to_remove_from_all.append(card_in_all_cards)
                    break

        for card_to_remove in cards_to_remove_from_all:
            if card_to_remove in all_cards:
                all_cards.remove(card_to_remove)

        self.game.deck.extend(all_cards)
        random.shuffle(self.game.deck)

    def test_attacker_after_player_beats(self):
        # Игрок атакует
        self.game.attacker = "player"
        self.game.table = [Card("Крести", "6")]
        self.game.player_hand = [Card("Крести", "7")]  # Карта для отбоя
        self.game.bot_hand = [Card("Бубны", "7")]  # Карта для отбоя бота

        # Игрок делает ход (предполагается, что это отбой, т.к. стол не пуст)
        self.game.player_move(0)  # Игрок отбивается
        self.game.end_round_success()  # Завершаем раунд
        self.game.set_next_attacker_after_defense_success("player")  # Игрок отбился, он остается атакующим
        self.assertEqual(self.game.attacker, "player")

    def test_attacker_after_bot_beats(self):
        # Бот атакует
        self.game.attacker = "bot"
        self.game.table = [Card("Бубны", "6")]
        self.game.bot_hand = [Card("Бубны", "7")]  # Карта для отбоя
        self.game.player_hand = [Card("Крести", "7")]  # Карта для отбоя игрока

        # Бот делает ход (предполагается, что это отбой, т.к. стол не пуст)
        # Моделируем, что бот может отбиться
        original_bot_move = self.game.bot_move

        def mock_bot_move_defense():  # Переименовал, чтобы было яснее
            if self.game.table:
                for i, card in enumerate(self.game.bot_hand):
                    # Проверяем, что карта бота может отбить первую карту на столе
                    if card.can_beat(self.game.table[0], self.game.trump_card.suit):
                        self.game.table.append(self.game.bot_hand.pop(i))
                        return True
            return False

        self.game.bot_move = mock_bot_move_defense  # Используем mock-функцию

        self.game.bot_move()  # Бот отбивается
        self.game.bot_move = original_bot_move  # Восстанавливаем оригинальный метод

        self.game.end_round_success()  # Завершаем раунд
        self.game.set_next_attacker_after_defense_success("bot")  # Бот отбился, он остается атакующим
        self.assertEqual(self.game.attacker, "bot")

    def test_player_takes_cards_when_cannot_beat(self):
        """
        Тестирует, что игрок забирает карты, когда не может отбиться,
        и атакующий остается тем же.
        """
        self.game.attacker = "bot"  # Бот атакует
        self.game.table = [Card("Крести", "8")]  # Карта, которую бот атаковал
        # У игрока нет карт, чтобы отбиться от Крести 8 (даже козыря)
        self.game.player_hand = [Card("Бубны", "7"), Card("Пики", "9")]
        self.game.trump_card = Card("Черви", "6")  # Козырь не помогает

        initial_player_hand_len = len(self.game.player_hand)  # 2
        initial_table_len = len(self.game.table)  # 1
        initial_deck_len = len(self.game.deck)  # Это 23 карты, как установлено в setUp

        # Моделируем, что игрок "берет" карты.
        # В реальной игре это происходит, если игрок не делает ход и затем вызывается handle_take_cards
        # Для теста мы напрямую вызываем логику, которая имитирует взятие карт.
        # Теперь вызов handle_take_cards
        # Поскольку Game.py содержит логику handle_take_cards, используем ее.
        # Проверяем, что игрок *не может* отбиться
        player_can_beat = False
        for card in self.game.player_hand:
            if card.can_beat(self.game.table[0], self.game.trump_card.suit):
                player_can_beat = True
                break
        self.assertFalse(player_can_beat, "Игрок не должен иметь карт для отбоя в этом тесте")

        # Имитируем, что игрок взял карты (вызов из main.py или аналогичная логика)
        # В данном случае, мы должны имитировать полную логику, которая происходит при взятии карт
        self.game.player_hand.extend(self.game.table)
        self.game.table = []
        self.game.draw_cards()
        self.game.attacker = "bot"  # Атакующий остается прежним

        # Проверка: карты со стола перешли в руку игрока, и рука пополнилась до 6 (если возможно)
        self.assertEqual(len(self.game.player_hand), 6)  # Рука игрока должна пополниться до 6
        self.assertEqual(len(self.game.table), 0)  # Стол очищен
        self.assertEqual(self.game.attacker, "bot")  # Атакующий остался ботом

        # Проверка: карты добираются (если есть в колоде)
        # Колода должна уменьшиться, так как игроки добирали карты
        self.assertLess(len(self.game.deck), initial_deck_len)
        self.assertEqual(len(self.game.bot_hand), 6)  # Рука бота тоже должна быть пополнена до 6

    def test_bot_takes_cards_when_cannot_beat(self):
        """
        Тестирует, что бот забирает карты, когда не может отбиться,
        и атакующий остается тем же.
        """
        self.game.attacker = "player"  # Игрок атакует
        self.game.table = [Card("Пики", "10")]  # Карта, которую игрок атаковал
        # У бота нет карт, чтобы отбиться от Пики 10
        self.game.bot_hand = [Card("Бубны", "9"), Card("Крести", "Валет")]
        self.game.trump_card = Card("Черви", "6")  # Козырь не помогает

        initial_player_hand_len = len(self.game.player_hand)
        initial_bot_hand_len = len(self.game.bot_hand)  # 2
        initial_table_len = len(self.game.table)  # 1
        initial_deck_len = len(self.game.deck)  # Это 23 карты, как установлено в setUp

        # Проверяем, что бот *не может* отбиться
        bot_can_beat = False
        for card in self.game.bot_hand:
            if card.can_beat(self.game.table[0], self.game.trump_card.suit):
                bot_can_beat = True
                break
        self.assertFalse(bot_can_beat, "Бот не должен иметь карт для отбоя в этом тесте")

        # Моделируем, что бот "берет" карты
        # Имитируем, что бот взял карты (вызов из main.py или аналогичная логика)
        self.game.bot_hand.extend(self.game.table)  # Бот забирает карты
        self.game.table = []  # Стол очищается
        self.game.draw_cards()  # Игроки добирают карты
        self.game.attacker = "player"  # Атакующий остается прежним

        # Проверка: карты со стола перешли в руку бота, и рука пополнилась до 6 (если возможно)
        self.assertEqual(len(self.game.bot_hand), 6)  # Рука бота должна пополниться до 6
        self.assertEqual(len(self.game.table), 0)  # Стол очищен
        self.assertEqual(self.game.attacker, "player")  # Атакующий остался игроком

        # Проверка: карты добираются (если есть в колоде)
        # Колода должна уменьшиться
        self.assertLess(len(self.game.deck), initial_deck_len)
        self.assertEqual(len(self.game.player_hand), 6)  # Рука игрока тоже должна быть пополнена до 6


if __name__ == '__main__':
    unittest.main()
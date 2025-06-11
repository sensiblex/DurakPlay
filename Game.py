import random
import logging
from GameBase import create_deck

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, filename="game-log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")
error_logger = logging.getLogger('game_errors')
error_handler = logging.FileHandler('game_errors.log')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

class Game:
    def __init__(self):
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = self.deck[:6]
        self.bot_hand = self.deck[6:12]
        self.deck = self.deck[12:]
        self.trump_card = self.deck.pop()
        self.table = []
        self.attacker = "player"  # Игрок начинает атаку

    def end_round_success(self):
        """Обрабатывает успешное завершение раунда (карты уходят в сброс и добираются)."""
        logging.info("Round ended successfully. Cards discarded.")
        self.table = []
        self.draw_cards() # Передача этой логики сюда

    def set_next_attacker_after_defense_success(self, defender_role):
        """Устанавливает следующего атакующего после успешного отбоя.
        Args:
            defender_role (str): Роль игрока, который успешно отбился ('player' или 'bot').
        """
        logging.info(f"Setting attacker to {defender_role} after successful defense.")
        self.attacker = defender_role

    def player_move(self, card_index):
        if card_index < 0 or card_index >= len(self.player_hand):
            error_logger.error(f"Invalid card index: {card_index}")
            return False
        card = self.player_hand[card_index]
        logging.info(f"Player attempts to play {card}")

        # Если игрок атакует, он может положить любую карту
        # Если защищается, должен бить карту на столе
        if self.attacker == "player" or (self.attacker == "bot" and any(
                card.can_beat(table_card, self.trump_card.suit) for table_card in self.table)):
            self.table.append(card)
            self.player_hand.pop(card_index)
            logging.info(f"Player's move with {card} was successful.")

            return True
        logging.warning(f"Player's move with {card} was not valid.")
        return False

    def bot_move(self):
        for i, card in enumerate(self.bot_hand):
            # Бот атакует или защищается в зависимости от текущего атакующего
            if (self.attacker == "bot" and not self.table) or \
                    (self.attacker == "player" and any(
                        card.can_beat(table_card, self.trump_card.suit) for table_card in self.table)):
                self.table.append(card)
                self.bot_hand.pop(i)
                return True
        return False

    def draw_cards(self):
        # Сначала карты берет атакующий, затем защищающийся
        if self.attacker == "player":
            while len(self.player_hand) < 6 and self.deck:
                self.player_hand.append(self.deck.pop(0))
            while len(self.bot_hand) < 6 and self.deck:
                self.bot_hand.append(self.deck.pop(0))
        else:
            while len(self.bot_hand) < 6 and self.deck:
                self.bot_hand.append(self.deck.pop(0))
            while len(self.player_hand) < 6 and self.deck:
                self.player_hand.append(self.deck.pop(0))

    def check_winner(self):
        if not self.bot_hand and not self.deck:
            return "Робот победил!"
        if not self.player_hand and not self.deck:
            return "Игрок победил!"
        return None
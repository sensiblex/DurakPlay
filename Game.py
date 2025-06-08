import random
from GameBase import Card, create_deck

class Game:
    def __init__(self):
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = self.deck[:6]
        self.bot_hand = self.deck[6:12]
        self.deck = self.deck[12:]
        self.trump_card = self.deck.pop()
        self.table = []

    def player_move(self, card_index):
        if card_index < 0 or card_index >= len(self.player_hand):
            return False
        card = self.player_hand[card_index]
        if not self.table or any(card.can_beat(table_card, self.trump_card.suit) for table_card in self.table):
            self.table.append(card)
            self.player_hand.pop(card_index)
            return True
        return False

    def bot_move(self):
        for i, card in enumerate(self.bot_hand):
            if not self.table or any(card.can_beat(table_card, self.trump_card.suit) for table_card in self.table):
                self.table.append(card)
                self.bot_hand.pop(i)
                return True
        return False

    def draw_cards(self):
        while len(self.player_hand) < 6 and self.deck:
            self.player_hand.append(self.deck.pop(0))
        while len(self.bot_hand) < 6 and self.deck:
            self.bot_hand.append(self.deck.pop(0))

    def check_winner(self):
        if not self.bot_hand and not self.deck:
            return "Робот победил!"
        if not self.player_hand and not self.deck:
            return "Игрок победил!"
        return None
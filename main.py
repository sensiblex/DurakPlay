import random
from GameBase import Card, create_deck
from Game import Game

def main():
    game = Game()
    while not game.check_winner():
        print(f"Козырь: {game.trump_card}")
        print("\nКарты игрока:", [str(card) for card in game.player_hand])
        print("На столе:", [str(card) for card in game.table])
        print("Введите индекс карты(0-5) (или -1 для пасса):")
        try:
            card_index = int(input())
            if card_index == -1:
                if game.table and not game.bot_move():
                    print("Робот взял карты")
                    game.bot_hand.extend(game.table)
                    game.table = []
                    game.draw_cards()
                continue
            if game.player_move(card_index):
                print("Игрок сыграл:", game.table[-1])
                if game.bot_move():
                    print("Робот сыграл:", game.table[-1])
                else:
                    print("Робот берет карты")
                    game.bot_hand.extend(game.table)
                    game.table = []
                game.draw_cards()
            else:
                print("Неправильный ход")
        except (ValueError, IndexError):
            print("Неправильный ввод")
    print(game.check_winner())

if __name__ == "__main__":
    main()
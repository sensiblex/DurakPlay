import random
from GameBase import Card, create_deck
from Game import Game


def main():
    game = Game()
    while not game.check_winner():
        print(f"\nКозырь: {game.trump_card}")
        print(f"Атакующий: {'Игрок' if game.attacker == 'player' else 'Робот'}")
        print("Ваши карты:", [f"{i}:{str(card)}" for i, card in enumerate(game.player_hand)])
        print("На столе:", [str(card) for card in game.table])

        if game.attacker == "player":
            # Ход игрока (атака)
            print("Ваш ход (атака). Введите индекс карты (0-5) или -1 для передачи хода:")
            try:
                card_index = int(input())
                if card_index == -1:
                    # Игрок пасует, ход переходит к боту
                    game.attacker = "bot"
                    continue

                if game.player_move(card_index):
                    print(f"Вы атакуете: {game.table[-1]}")

                    # Теперь бот должен защищаться
                    if not game.bot_move():
                        print("Робот не может отбиться и забирает карты")
                        game.bot_hand.extend(game.table)
                        game.table = []
                        game.draw_cards()
                        # После того как бот взял карты, он становится атакующим
                        game.attacker = "bot"
                    else:
                        print(f"Робот отбивается: {game.table[-1]}")
                        print("Бито! Карты уходят в сброс")
                        game.table = []
                        game.draw_cards()
                        # После успешного отбоя ход переходит к защищавшемуся (боту)
                        game.attacker = "bot"
                else:
                    print("Невозможно сыграть эту карту, попробуйте другую")
            except (ValueError, IndexError):
                print("Неправильный ввод")
        else:
            # Ход бота (атака)
            print("Робот атакует...")
            if game.bot_move():
                print(f"Робот атакует: {game.table[-1]}")

                # Теперь игрок должен защищаться
                print("Ваш ход (защита). Введите индекс карты для отбоя или -1 чтобы взять карты:")
                try:
                    card_index = int(input())
                    if card_index == -1:
                        print("Вы берете карты")
                        game.player_hand.extend(game.table)
                        game.table = []
                        game.draw_cards()
                        # После того как игрок взял карты, он становится атакующим
                        game.attacker = "player"
                    else:
                        if game.player_move(card_index):
                            print(f"Вы отбиваете: {game.table[-1]}")
                            print("Бито! Карты уходят в сброс")
                            game.table = []
                            game.draw_cards()
                            # После успешного отбоя ход переходит к защищавшемуся (игроку)
                            game.attacker = "player"
                        else:
                            print("Невозможно сыграть эту карту, попробуйте другую")
                            continue
                except (ValueError, IndexError):
                    print("Неправильный ввод")
            else:
                print("Робот не может атаковать, передает ход")
                game.attacker = "player"

        # Если стол пуст, добор карт
        if not game.table:
            game.draw_cards()

    print(game.check_winner())


if __name__ == "__main__":
    main()
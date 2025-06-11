import random
from GameBase import Card, create_deck
from Game import Game

def print_game_state(game):
    print(f"\nКозырь: {game.trump_card}")
    print(f"Атакующий: {'Игрок' if game.attacker == 'player' else 'Робот'}")
    print("Ваши карты:", [f"{i}:{str(card)}" for i, card in enumerate(game.player_hand)])
    print("На столе:", [str(card) for card in game.table])

def player_attack(game):
    while True:
        print("Ваш ход (атака). Введите индекс карты (0-5) или -1 для передачи хода:")
        try:
            card_index = int(input())
            if card_index == -1:
                game.attacker = "bot"
                return
            if game.player_move(card_index):
                print(f"Вы атакуете: {game.table[-1]}")
                # Проверяем, отбился ли бот
                if not game.bot_move():  # Бот не смог отбиться
                    game.handle_take_cards("bot")  # <-- ИСПОЛЬЗУЕМ НОВЫЙ МЕТОД
                else:  # Робот отбивается
                    print(f"Робот отбивается: {game.table[-1]}")
                    print("Бито! Карты уходят в сброс")
                    game.end_round_success()
                    game.set_next_attacker_after_defense_success("bot")
                return  # Выходим после хода (атаки) игрока
            else:
                print("Невозможно сыграть эту карту, попробуйте другую")
        except (ValueError, IndexError):
            print("Неправильный ввод")

def player_defense(game):
    while True:
        print("Ваш ход (защита). Введите индекс карты для отбоя или -1 чтобы взять карты:")
        try:
            card_index = int(input())
            if card_index == -1:  # Игрок решил взять карты
                game.handle_take_cards("player")  # <-- ИСПОЛЬЗУЕМ НОВЫЙ МЕТОД
                return
            if game.player_move(card_index):
                print(f"Вы отбиваете: {game.table[-1]}")
                print("Бито! Карты уходят в сброс")
                game.end_round_success()  # <-- ИСПОЛЬЗУЕМ НОВЫЙ МЕТОД
                game.set_next_attacker_after_defense_success("player")  # <-- ИСПОЛЬЗУЕМ НОВЫЙ МЕТОД
                return
            else:
                print("Невозможно сыграть эту карту, попробуйте другую")
        except (ValueError, IndexError):
            print("Неправильный ввод")

def bot_attack(game):
    print("Робот атакует...")
    if game.bot_move():
        print(f"Робот атакует: {game.table[-1]}")
        player_defense(game) # Передаем управление игроку для защиты
        # Логика смены атакующего уже в player_defense
    else:
        print("Робот не может атаковать, передает ход")
        game.attacker = "player"  # <--- Убедитесь, что эта строка есть и она такая

def main():
    game = Game()
    while not game.check_winner():
        print_game_state(game)
        if game.attacker == "player":
            player_attack(game)
        else:
            bot_attack(game)

        if not game.table:
            game.draw_cards()

    print(game.check_winner())

if __name__ == "__main__":
    main()

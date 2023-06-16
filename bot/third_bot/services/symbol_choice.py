from random import choice


def get_choice():
    symbols = ['Камень', 'Ножницы', 'Бумага']
    symbol = choice(symbols)
    return symbol

def get_winner(bot_choice, player_choice):
    winer_dict = {
        'Камень': {
            'Ножницы': 'Я',
            'Бумага': 'Ты'
        },
        'Ножницы': {
            'Бумага': 'Я',
            'Камень': 'Ты'

        },
        'Бумага': {
            'Камень': 'Я',
            'Ножницы': 'Ты',
        }
    }
   
    if bot_choice == player_choice:
        return None
    return winer_dict[bot_choice][player_choice]


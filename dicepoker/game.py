import sys
from typing import List

from dicepoker import Player, Hand, Human
from dicepoker.profile import sanitize_selection


def play(player1: Player,
         player2: Player,
         initial_coin=100,
         initial_stake=10,
         raise_amount=10,
         num_rounds=3):

    if type(num_rounds) != int or num_rounds < 1:
        raise ValueError(f'num_rounds = {num_rounds}, expected >= 1')

    player1_name = player1.name()
    player2_name = player2.name()
    if player1_name == player2_name:
        player1_name += ' (1)'
        player2_name += ' (2)'

    player1_coin = initial_coin
    player2_coin = initial_coin

    rv = [[0, player1_coin, player2_coin]]

    for round_num in range(1, num_rounds + 1):

        round_msg = f'Round {round_num} of {num_rounds}'
        print()
        print('#' * 80)
        print(f'# {round_msg:<76} #')
        print('#' * 80)
        print()

        stake = initial_stake

        if player1_coin >= stake and player2_coin >= stake:

            player1_coin = player1_coin - stake
            player2_coin = player2_coin - stake

            print(f'{player1_name} vs {player2_name}')
            print()

            player1_hand = Hand()
            player2_hand = Hand()

            print(f'{player1_name:>20}   {player1_hand}')
            print(f'{player2_name:>20}   {player2_hand}')

            if player1_coin >= raise_amount and player2_coin >= raise_amount:
                player1_accept = player1.accept_raise_stakes(stake, player1_coin, player1_hand, player2_hand, raise_amount)
                player2_accept = player2.accept_raise_stakes(stake, player2_coin, player2_hand, player1_hand, raise_amount)
                if player1_accept and player2_accept:
                    stake += raise_amount
                    player1_coin -= raise_amount
                    player2_coin -= raise_amount
                    print(f'players raised stake to is {stake}')
                elif not player1_accept and not player2_accept:
                    print(f'players agreed not to raise stakes')
                elif not player1_accept:
                    print(f'{player1_name} did not agree to raise stakes')
                else:
                    print(f'{player2_name} did not agree to raise stakes')
            else:
                if player1_coin < raise_amount:
                    print(f'{player1_name} does not have enough coin to raise stakes')
                if player2_coin < raise_amount:
                    print(f'{player2_name} does not have enough coin to raise stakes')

            player1_selection = player1.choose_dice_to_reroll(stake, player1_coin, player1_hand, player2_hand)
            player2_selection = player2.choose_dice_to_reroll(stake, player2_coin, player2_hand, player1_hand)
            player1_selection = sanitize_selection(player1_selection)
            player2_selection = sanitize_selection(player2_selection)
            if player1_selection:
                print(f'{player1_name:>20}   will re-roll {player1_selection}')
            elif player1_selection == player1_hand.dice:
                print(f'{player1_name:>20}   will re-roll all five dice')
            else:
                print(f'{player1_name:>20}   will not re-roll')
            if player2_selection:
                print(f'{player2_name:>20}   will re-roll {player2_selection}')
            elif player2_selection == player2_hand.dice:
                print(f'{player2_name:>20}   will re-roll all five dice')
            else:
                print(f'{player2_name:>20}   will not re-roll')

            print('re-rolling')
            player1_hand = player1_hand.re_roll(player1_selection)
            player2_hand = player2_hand.re_roll(player2_selection)

            print(f'{player1_name:>20}   {player1_hand}')
            print(f'{player2_name:>20}   {player2_hand}')

            if player1_hand > player2_hand:
                print(f'{player1_name} won')
                player1_coin += stake * 2
            elif player1_hand < player2_hand:
                print(f'{player2_name} won')
                player2_coin += stake * 2
            else:
                print("it's a draw")
                player1_coin += stake
                player2_coin += stake

            print(f'{player1_name} has {player1_coin}')
            print(f'{player2_name} has {player2_coin}')

            rv.append([round_num, player1_coin, player2_coin])

            print()

        else:

            if player1_coin < stake:
                print(f'{player1_name} is out of coin and loses')
                print(f'{player2_name} is the winner')
            else:
                print(f'{player2_name} is out of coin and loses')
                print(f'{player1_name} is the winner')

            break

        print(f'{player1_name} has {player1_coin} coin')
        print(f'{player2_name} has {player2_coin} coin')
        if player1_coin < player2_coin:
            print(f'{player2_name} is the winner')
        elif player1_coin > player2_coin:
            print(f'{player1_name} is the winner')
        else:
            print("It's a draw!")

    return rv


def print_rounds(result, player1, player2):
    player1_name = player1.name()
    player2_name = player2.name()
    if player1_name == player2_name:
        player1_name += ' (1)'
        player2_name += ' (2)'
    print(f'       Round {player1_name:>12} {player2_name:>12}')
    print(f'------------ ------------ ------------')
    for round_num, player1_coin, player2_coin in result:
        print(f'{round_num:>12} {player1_coin:>12} {player2_coin:>12}')


def challenge(cpu_player: Player,
              initial_coin=100,
              initial_stake=10,
              raise_amount=10,
              num_rounds=3) -> None:
    try:
        human_player = Human()
        result = play(human_player, cpu_player, initial_coin, initial_stake, raise_amount, num_rounds)
        print()
        print_rounds(result, human_player, cpu_player)
    except KeyboardInterrupt:
        print()
        print()
        print('[challenge cancelled by user]')
        sys.exit(1)

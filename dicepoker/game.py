from typing import List

from dicepoker import Player, Hand
from dicepoker.profile import sanitize_selection


def print_verbose(verbose: bool, text: str) -> None:
    if verbose:
        print(text)


def play_until_bankrupt(player1: Player,
                        player2: Player,
                        verbose=True,
                        initial_coin=100,
                        initial_stake=10,
                        raise_amount=10) -> List[List[int]]:

    player1_name = player1.name()
    player2_name = player2.name()
    if player1_name == player2_name:
        player1_name += ' (1)'
        player2_name += ' (2)'

    player1_coin = initial_coin
    player2_coin = initial_coin

    round_num = 0
    rv = [[round_num, player1_coin, player2_coin]]

    while True:

        round_num += 1

        stake = initial_stake

        if player1_coin >= stake and player2_coin >= stake:

            player1_coin = player1_coin - stake
            player2_coin = player2_coin - stake

            print_verbose(verbose, f'{player1_name} vs {player2_name}')
            print_verbose(verbose, f'stake is {stake}')

            player1_hand = Hand()
            player2_hand = Hand()

            print_verbose(verbose, f'{player1_name:>20}   {player1_hand}')
            print_verbose(verbose, f'{player2_name:>20}   {player2_hand}')

            if player1_coin >= raise_amount and player2_coin >= raise_amount:
                player1_accept = player1.accept_raise_stakes(stake, player1_coin, player1_hand, player2_hand)
                player2_accept = player2.accept_raise_stakes(stake, player2_coin, player2_hand, player1_hand)
                if player1_accept and player2_accept:
                    stake += raise_amount
                    player1_coin -= raise_amount
                    player2_coin -= raise_amount
                    print_verbose(verbose, f'players raised stake to is {stake}')
                elif not player1_accept and not player2_accept:
                    print_verbose(verbose, f'players agreed not to raise stakes')
                elif not player1_accept:
                    print_verbose(verbose, f'{player1_name} did not agree to raise stakes')
                else:
                    print_verbose(verbose, f'{player2_name} did not agree to raise stakes')
            else:
                if player1_coin < raise_amount:
                    print_verbose(verbose, f'{player1_name} does not have enough coin to raise stakes')
                if player2_coin < raise_amount:
                    print_verbose(verbose, f'{player2_name} does not have enough coin to raise stakes')

            player1_selection = player1.choose_dice_to_reroll(stake, player1_coin, player1_hand, player2_hand)
            player2_selection = player2.choose_dice_to_reroll(stake, player2_coin, player2_hand, player1_hand)
            player1_selection = sanitize_selection(player1_selection)
            player2_selection = sanitize_selection(player2_selection)
            if player1_selection:
                print_verbose(verbose, f'{player1_name:>20}   will re-roll {player1_selection}')
            elif player1_selection == player1_hand.dice:
                print_verbose(verbose, f'{player1_name:>20}   will re-roll all five dice')
            else:
                print_verbose(verbose, f'{player1_name:>20}   will not re-roll')
            if player2_selection:
                print_verbose(verbose, f'{player2_name:>20}   will re-roll {player2_selection}')
            elif player2_selection == player2_hand.dice:
                print_verbose(verbose, f'{player2_name:>20}   will re-roll all five dice')
            else:
                print_verbose(verbose, f'{player2_name:>20}   will not re-roll')

            print_verbose(verbose, 're-rolling')
            player1_hand = player1_hand.re_roll(player1_selection)
            player2_hand = player2_hand.re_roll(player2_selection)

            print_verbose(verbose, f'{player1_name:>20}   {player1_hand}')
            print_verbose(verbose, f'{player2_name:>20}   {player2_hand}')

            if player1_hand > player2_hand:
                print_verbose(verbose, f'{player1_name} won')
                player1_coin += stake * 2
            elif player1_hand < player2_hand:
                print_verbose(verbose, f'{player2_name} won')
                player2_coin += stake * 2
            else:
                print_verbose(verbose, "it's a draw")
                player1_coin += stake
                player2_coin += stake

            print_verbose(verbose, f'{player1_name} has {player1_coin}')
            print_verbose(verbose, f'{player2_name} has {player2_coin}')

            rv.append([round_num, player1_coin, player2_coin])

            print_verbose(verbose, '')

        else:

            if player1_coin < stake:
                print_verbose(verbose, f'{player1_name} is out of coin and loses')
                print_verbose(verbose, f'{player2_name} is the winner')
            else:
                print_verbose(verbose, f'{player2_name} is out of coin and loses')
                print_verbose(verbose, f'{player1_name} is the winner')

            break

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

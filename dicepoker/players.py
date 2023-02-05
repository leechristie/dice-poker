from abc import ABC, abstractmethod
from typing import List
from dicepoker import Hand


class Player(ABC):

    def __str__(self):
        return self.name()

    def __repr__(self):
        return self.name()

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def accept_raise_stakes(self,
                            current_stakes: int,
                            available_money: int,
                            my_hand: Hand,
                            opponent_hand: Hand) -> bool:
        pass

    @abstractmethod
    def choose_dice_to_reroll(self,
                              current_stakes: int,
                              available_money: int,
                              my_hand: Hand,
                              opponent_hand: Hand) -> List[int]:
        pass

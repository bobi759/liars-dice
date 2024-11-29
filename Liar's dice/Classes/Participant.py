from random import randint
from abc import ABC, abstractmethod


class Participant(ABC):
    """
    Abstract base class representing a participant in the game that is inherited.

    Each participant is initialised with starting count of dice and hand of dice.

    Each participant has decision-making method that implements later.
    """

    def __init__(self):
        self.dice_count = 5
        self.dice = []

    def roll_dice(self):
        self.dice = [randint(1, 6) for _ in range(self.dice_count)]

    @abstractmethod
    def decide_action(self, current_count, current_face, all_dice_count):
        pass



from random import choice, random
from scipy.stats import binom
import time
from .participant import Participant


class Bot(Participant):
    LIAR_PROBABILITY = 0.3
    RAISE_BET_THRESHOLD = 0.5
    PIRATE_NAMES = ["Blackbeard", "Blade", "The Drunk", "Speechless", "Traitor", "Mac McKraken", "Jack Sparrow",
                    "Will Turner", "Barbosa", "Davy Jones", "Bill Turner"]

    def __init__(self, game_mod):
        super().__init__()
        self.game_mode = game_mod
        self.name = self._chose_name()
        time.sleep(self.DELAY_TIME)

    @staticmethod
    def _chose_name():
        name = choice(Bot.PIRATE_NAMES)
        Bot.PIRATE_NAMES.remove(name)
        print(f"{name} entered the game RRRR!")
        return name

    def decide_action(self, current_count, current_face, total_dice_count):
        """
        Method that manages bot's decision-making strategy.
        Cases:
            1. First bid:
                - Bids it's first die with count 1.
            2. Probability-based bid:
                - Тhe calculations were done with probabilities and binomial distribution
                - Counts the dice of the same face in hand
                - Counts dice on table
                - Calls new bid depending on whether probability of (current_face, current_count + 1) is above minimal threshold
            3. Bot calls randomly liar, making the game more unpredictable
            4. Raises face of bid since the chance of (current_face, current_count +1 ) is low
            5. If there is neither good chance if higher count nor better face, bot calls liar as there no other option

        :param current_count: current count of the bid
        :param current_face: current face of the bid
        :param total_dice_count: count of dices on the table
        :return:
            - Tuple of new bid.
            - Liar call.
        """
        time.sleep(self.DELAY_TIME)
        if current_count == 0 and current_face == 0:
            first_dice_face = self.dice[0]
            first_dice_count = 1
            print(f"{self.name} makes the first bid: {first_dice_face} with count {first_dice_count}.")
            return first_dice_count, first_dice_face

        on_hand_count = self.dice.count(current_face)
        if self.game_mode == 'Wild':
            on_hand_count += self.dice.count(1)
        unseen_dice_count = total_dice_count - self.dice_count
        increase_bid_dice_needed = current_count - on_hand_count + 1
        probability_of_success = 2/6 if (self.game_mode == 'Wild' and current_face != 1) else 1/6

        if self._high_probability_for_increasing_bid(unseen_dice_count, increase_bid_dice_needed, probability_of_success, Bot.RAISE_BET_THRESHOLD):
            return self._increase_bid(current_count, current_face)

        if random() < Bot.LIAR_PROBABILITY:
            print(f"{self.name} called a liar!")
            return "Liar"

        better_face_result = self._better_face(current_face)
        if better_face_result is not None:
            return better_face_result

        print(f"{self.name} calls a liar!")
        return "Liar"

    def _better_face(self, current_face):
        """
        Finding better face to bid on.
        """
        possible_options = [i for i in range(1, 7) if i > current_face and i in self.dice]
        if possible_options:
            better_face = possible_options[0]
            better_face_count = self.dice.count(better_face)
            print(f"{self.name} bids {better_face} with count {better_face_count}.")
            return better_face_count, better_face
        return None

    @staticmethod
    def probability_at_least_k(number_of_trials, number_of_unfavorable_cases, probability_of_success_on_trial):
        """
        Calculate P(X >= k) for binomial distribution.
        Subtracts the probability of unfavorable events from 1.
        In normal mode probability of success is 1/6 as exactly one face satisfy our bid.
        In comparison, in wild mode probability of success rises to 2/6 as current_face and face 1 satisfy our bid.
        """
        return 1 - binom.cdf(number_of_unfavorable_cases - 1, number_of_trials, probability_of_success_on_trial)

    def _high_probability_for_increasing_bid(self, unseen_dice_count, required_count_from_unseen, probability_of_success, probability_threshold):
        """
        Method that returns whether probability of success is satisfactory
        """
        return self.probability_at_least_k(unseen_dice_count,required_count_from_unseen,probability_of_success) > probability_threshold

    def _increase_bid(self, current_count, current_face):
        """
        Increasing count of current face with one after chances are in bot's favour.
        """
        current_count += 1
        print(f"{self.name} bids {current_face} with count {current_count}.")
        return current_count, current_face
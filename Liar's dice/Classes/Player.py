from Classes.Participant import Participant


class Player(Participant):

    def __init__(self):
        super().__init__()
        self.name = self._chose_name()

    @staticmethod
    def _chose_name():
        player_name = input("Please enter your name: ")
        print(f"{player_name} entered the game!")
        return player_name

    def decide_action(self, current_count, current_face, all_dice_count):
        """
        Manages the logic of taking making a bid or challenging the current one.
        Returns new bid or liar call.
        """
        print(f"Your hand is {self.dice}")
        while True:
            decision = input("Bid or challenge? (B/C) ").upper()
            if decision == 'B':
                 return self._make_valid_bet(current_count,current_face,all_dice_count)
            elif decision == 'C':
                if self._handle_challenge(current_count, current_face):
                    return "Liar"
            else:
                print("Invalid input. Please enter 'B' to bid or 'C' to challenge.")

    @staticmethod
    def _validate_bet(current_count, current_face, new_count, new_face, all_dice_count):
        """
        Validates a new bid in the game.
        The following bids are valid:

        1. First Bid:
            - Face must be between 1 and 6
            - Count must be between 1 and count of dices on the table
        2. Same Face Bid:
            - Face remains the same
            - Count must be higher
        3. Higher Face Bid:
            - Face must be higher
            - Count must be between 1 and count of dices on the table
        """
        if current_count == current_face == 0 and 1 <= int(new_face) <= 6 and 1 <= int(new_count) <= all_dice_count:
            return True
        if current_face == int(new_face) and 0 < int(new_face) <= 6 and all_dice_count >= int(new_count) > current_count:
            return True
        if current_face < int(new_face) <= 6  and current_count > 0:
            return True
        return False

    def _make_valid_bet(self,current_count,current_face,all_dice_count):
        """
        Repeatedly asks the player to make valid bid.
        """
        while True:
            new_face = int(input("Enter face value: "))
            new_count = int(input("Enter count value: "))
            if self._validate_bet(current_count, current_face, new_count, new_face, all_dice_count):
                print(f"{self.name} bids {new_face} with count {new_count}.")
                return int(new_count), int(new_face)
            else:
                print("Invalid bid. Try again!")

    def _handle_challenge(self,current_count, current_face):
        """
        Manages challenge call of current bid.
        """
        if current_count == 0 and current_face == 0:
            print("You cannot challenge when no bid has been made. Please take a valid action.")
            return False
        else:
            print(f"{self.name} calls liar!")
            return True

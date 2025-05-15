from collections import deque
from .player import Player
from .bot import Bot


class Game:
    def __init__(self, mode: str, enemies_count: int):
        """
        Defines game's rule such as game mode and enemies count.
        All bids are in format (count,face).
        """
        self.mode = mode
        self.enemies_count = enemies_count
        self.participants = deque([Player()] + [Bot(self.mode) for _ in range(self.enemies_count)])
        self.current_bet = (0, 0)

    def update_dice_count(self, player, reason):
        """
        Updates loser's dice and eliminates them if needed.
        """
        player.dice_count -= 1
        print(f"{reason} {player.name} loses a dice! Remaining dices: {player.dice_count}.")
        if player.dice_count == 0:
            print(f"{player.name} eliminated!")
            self.participants.popleft()

    def play(self):
        """
        Main game loop including:
            - Staring new round.
            - Rolling new dice.
            - Dealing with liar's logic.
        """
        while len(self.participants) > 1:
            [p.roll_dice() for p in self.participants]
            all_dice = [dice for participant in self.participants for dice in participant.dice]
            self.current_bet = (0, 0)

            # Current round loop
            while True:
                current_player = self.participants[0]
                result = current_player.decide_action(*self.current_bet, len(all_dice))

                if result == "Liar":
                    count, face = self.current_bet
                    print(f"Dices on the table: \n{', '.join(sorted([str(x) for x in all_dice]))}")

                    if self.mode == 'Wild':
                        actual_count = all_dice.count(face) + all_dice.count(1)
                    else:
                        actual_count = all_dice.count(face)

                    if actual_count >= count:
                        self.update_dice_count(self.participants[0], "Disputant is incorrect.")
                    else:
                        self.participants.rotate(1)
                        self.update_dice_count(self.participants[0], "Challenge is valid!")
                    break
                else:
                    self.current_bet = result

                self.participants.rotate(-1)
        print(f"{self.participants[0].name} wins the game. Congratulations!")

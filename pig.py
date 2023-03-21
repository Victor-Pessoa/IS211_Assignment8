import argparse
import random
import time


class Player:
    def _init_(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points

    def take_turn(self):
        """
        This method should be implemented by sub-classes of Player
        """
        raise NotImplementedError


class HumanPlayer(Player):
    def take_turn(self):
        move = input(f"{self.name}, enter 'roll' to roll or 'hold' to hold: ")
        while move not in ["roll", "hold"]:
            print("Invalid move. Please enter 'roll' or 'hold'.")
            move = input(f"{self.name}, enter 'roll' to roll or 'hold' to hold: ")
        return move


class ComputerPlayer(Player):
    def take_turn(self):
        if self.score > 20:
            return "hold"
        else:
            return "roll"


class PlayerFactory:
    def create_player(self, player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)


class Game:
    def _init_(self, player1_type, player2_type):
        self.player_factory = PlayerFactory()
        self.player1 = self.player_factory.create_player(player1_type, "Player 1")
        self.player2 = self.player_factory.create_player(player2_type, "Player 2")
        self.current_player = self.player1
        self.dice = [1, 2, 3, 4, 5, 6]
        self.score_target = 100
        self.turn_score = 0

    def roll_dice(self):
        return random.choice(self.dice)

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def play_turn(self):
        print(f"{self.current_player.name}'s turn")
        move = self.current_player.take_turn()
        if move == "roll":
            roll = self.roll_dice()
            print(f"{self.current_player.name} rolled a {roll}")
            if roll == 1:
                self.turn_score = 0
                print(f"{self.current_player.name} scored 0 points this turn.")
                self.switch_player()
                return
            else:
                self.turn_score += roll
                print(f"{self.current_player.name}'s turn score: {self.turn_score}")
                if self.current_player.score + self.turn_score >= self.score_target:
                    self.current_player.add_score(self.turn_score)
                    print(f"{self.current_player.name} wins the game with {self.current_player.score} points!")
                    exit()
        elif move == "hold":
            self.current_player.add_score(self.turn_score)
            print(f"{self.current_player.name} holds and scores {self.turn_score} points this turn.")
            print(f"{self.current_player.name}'s total score: {self.current_player.score}")
            if self.current_player.score >= self.score_target:
                print(f"{self.current_player.name} wins the game with {self.current_player.score} points!")
                exit()
        self.turn_score = 0
        self.switch_player()

class TimedGameProxy(Game):
    def __init__(self, player1_type, player2_type, duration):
        super().__init__(player1_type, player2_type)
        self.duration = duration

    def play_turn(self):
        if time.time() - self.start_time > self.duration:
            print("Time's up!")
            if self.player1.score > self.player2.score:
                print(f"{self.player1.name} wins the game with {self.player1.score} points!")
            elif self.player1.score < self.player2.score:
                print(f"{self.player2.name} wins the game with {self.player2.score} points!")
            else:
                print("It's a tie!")
            sys.exit()
        super().play_turn()

    def play_game(self):
        print("Let's play Pig!")
        self.start_time = time.time()
        while True:
            print("")
            print(f"Current scores: {self.player1.name} ({self.player1.score}) - {self.player2.name} ({self.player2.score})")
            self.play_turn()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play Pig game with human and computer players.')
    parser.add_argument('--player1', type=str, default='human', help='Type of player 1: human or computer')
    parser.add_argument('--player2', type=str, default='computer', help='Type of player 2: human or computer')
    parser.add_argument('--timed', type=int, default=0, help='Time limit for the game in seconds. If 0, the game is not timed.')
    args = parser.parse_args()

    player1_type = args.player1.lower()
    player2_type = args.player2.lower()
    timed_duration = args.timed

    if timed_duration > 0:
        game = TimedGameProxy(player1_type, player2_type, timed_duration)
    else:
        game = Game(player1_type, player2_type)

    game.play_game()

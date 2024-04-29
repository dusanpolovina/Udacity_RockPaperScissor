#!/usr/bin/env python3
# checked with pycodestyle 2.10.0
import random
import time

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']  # move definitions
cvc_limiter = 50  # this variuable limits number of comp v comp rounds

"""The Player class is the parent class for all of the Players
in this game"""


class Player:

    def move(self):
        return 'rock'

    def learn(self, p_move, op_move):  # p=player, op=other player
        pass


class RandomPlayer(Player):
    def move(self, round):
        ranmove = random.choice(moves)
        return ranmove


# this auto player only plays rock
class RockPlayer(Player):
    def move(self, round):
        return 'rock'


# this player only plays paper
class PaperPlayer(Player):
    def move(self, round):
        return 'paper'


# this player only plays scissors
class ScissorPlayer(Player):
    def move(self, round):
        return 'scissors'


# this auto player mirrors opponent previous round moves
class MirrorPlayer(Player):
    def move(self, round):
        if round == 0:
            return random.choice(moves)
        elif round > 0:
            return self.prev_move

    def learn(self, p_move, op_move):  # p=player, op=other player
        self.prev_move = op_move


# this auto player cycle through r-p-s
class CyclePlayer(Player):
    def move(self, round):
        if round == 0:
            return random.choice(moves)
        elif round > 0:
            index = 0
            while index < len(moves):
                if moves[index] == self.prev_move:
                    return moves[(index + 1) % 3]
                index += 1

    def learn(self, p_move, op_move):  # p=player, op=other player
        self.prev_move = p_move


# this auto player cycle through s-p-r
class RevCyclePlayer(Player):
    def move(self, round):
        if round == 0:
            return random.choice(moves)
        elif round > 0:
            index = 0
            while index < len(moves):
                if moves[index] == self.prev_move:
                    return moves[(index + 2) % 3]
                index += 1

    def learn(self, p_move, op_move):  # p=player, op=other player
        self.prev_move = p_move


# this is a human player with human input required
class HumanPlayer(Player):
    def move(self, round):
        while True:
            hum_move = input(
                            "What would you like to play"
                            " (rock, paper, or scissors?): "
                            ).lower()
            for response in moves:
                if hum_move == response:
                    return hum_move
                elif hum_move == 'quit':
                    # this quit feature works all the time
                    # regardless if finite rounds chosen
                    return 'quit'
            print("I'm sorry, I don't understand that")
            # if human input not in responses options (moves[])
            # or if it isn't the 'quit' string,
            # then we just loop back up and try again


def beats(one, two):
    index = 0
    winner = (False, False)
    # this while loop determines who won round and outputs a boolean tuple
    while index < len(moves):
        if one == moves[index] and two == moves[index]:
            print_pause(f"{one.upper()} vs {two.upper()} - TIE!")
            # default value for winner is (False, False)
            # so that passes through here
        elif one == moves[index] and two == moves[index - 1]:
            print_pause(
                    f"{one.upper()} beats {two.upper()} "
                    f"- Player One wins!")
            winner = (True, False)
            # if P1 is the winner of the round, return the above tuple
        elif one == moves[index] and two == moves[(index + 1) % 3]:
            print_pause(
                    f"{one.upper()} loses to "
                    f"{two.upper()} - Player Two wins!"
                    )
            winner = (False, True)
            # if P2 is the winner of the round, return the above tuple
        index += 1
    return winner


# startup function for choosing player, human or automated
# and randomizes automated player choice as well
def player_choice():
    import random
    print_pause("\n--Rock--")
    print_pause("--Paper--")
    print_pause("--Scissors--\n")
    # added a feature here to randomize the choice of automated player
    comp_players = [
            RandomPlayer(), RockPlayer(), ScissorPlayer(),
            MirrorPlayer(), CyclePlayer(), RevCyclePlayer()
            ]
    while True:
        # this validates human vs computer player input
        player_choice = input(
                        "Player One - "
                        "Type 'Human' or 'Computer': "
                        ).lower()
        if player_choice == 'human':
            return Game(
                        HumanPlayer(),
                        random.choice(comp_players)
                        ), True
        elif player_choice == 'computer':
            print_pause(
                f"Note: computer simulation limited "
                f"to {cvc_limiter} rounds"
                )
            return Game(
                        random.choice(comp_players),
                        random.choice(comp_players)
                        ), False
        else:
            print_pause("I'm sorry I don't understand that")


def print_pause(message):
    print(message)
    time.sleep(0.8)


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def spec_rounds(self, state):
        # using state arg to limit number of rounds in comp vs comp mode
        while True:
            # this try/except validates numerical input
            # for conversion to int() value
            # and protects against a string input (ValueError)
            try:
                num_rounds = abs(int(input(
                                "How many rounds would "
                                "you like to play?\n"
                                "Enter number (n > 0) or "
                                "infinite (enter 0): "
                                )))
                if num_rounds > 0 and state is True:
                    # human mode w rounds specified
                    # only positive integers allowed here
                    # if negative value input, will assume abs value
                    print_pause(f"Ok you entered {num_rounds} rounds")
                    print_pause(f"So let's play {num_rounds} rounds!")
                    print_pause("Enter 'quit' at any round to end game")
                elif num_rounds == 0 and state is True:
                    # condition allows for endless rounds in  human mode
                    print_pause(f"Ok type 'quit' to end at any time")
                elif num_rounds > cvc_limiter and state is False:
                    # condition limits comp v comp mode to 100 round
                    print_pause(
                        f"Computer simulation mode "
                        f"limited to {cvc_limiter} rounds"
                        )
                    num_rounds = cvc_limiter
                    print_pause(
                        f"Computer players will "
                        f"simulate {num_rounds} rounds!"
                        )
                elif num_rounds == 0 and state is False:
                    # endless mode not allowed in comp v comp
                    # limited to 100 rounds
                    print_pause(
                        f"Computer simulation mode "
                        f"limited to {cvc_limiter} rounds"
                        )
                    num_rounds = cvc_limiter
                    print_pause(
                        f"Computer players will "
                        f"simulate {num_rounds} rounds!"
                        )
                else:
                    # condition for comp v comp with 0 > rounds > 100
                    print_pause(
                        f"Computer players will "
                        f"simulate {num_rounds} rounds!"
                        )
                return num_rounds
            except ValueError:
                # if string input that can't be converted w int()
                print_pause("I'm sorry I don't understand that")

    def play_round(self, round):
        move1 = self.p1.move(round)
        move2 = self.p2.move(round)
        if move1 == 'quit':
            return 'quit'
        else:
            print_pause(f"Player One plays {move1.upper()}")
            print_pause(f"Player Two plays {move2.upper()}")
            round_win = beats(move1, move2)
            # beats() arbitrates the winner
            self.p1.learn(move1, move2)
            self.p2.learn(move2, move1)
            # above two lines feed back for learning if applicable
            return round_win

    def scoring_round(self, num_rounds, score):
        round = 0
        while round < num_rounds or num_rounds == 0:
            # human player: if round == 0 then loop forever until 'quit'
            # comp vs comp: limited to 100 rounds
            print_pause(f"Round {round + 1}:")
            round_res = self.play_round(round)
            if round_res == (False, False):
                score[2] += 1
            elif round_res == (True, False):
                score[0] += 1
            elif round_res == (False, True):
                score[1] += 1
            elif round_res == 'quit':
                print_pause("Looks like you want to quit")
                break
            print_pause(
                    f"Round {round + 1} results\nPlayer One: {score[0]} -  "
                    f"Player Two: {score[1]} - Ties: {score[2]}\n\n"
                    )
            round += 1
        return score

    def play_game(self, state):
        num_rounds = self.spec_rounds(state)
        print_pause("GAME START\n")
        score = [0, 0, 0]  # initialize score list = [p1 wins, p2 wins, ties]
        score = self.scoring_round(num_rounds, score)
        print_pause(
                f"FINAL SCORE Player One: {score[0]} -  "
                f"Player Two: {score[1]} - Ties: {score[2]}"
                )
        if score[0] > score[1]:
            print_pause("Player One Wins!")
        elif score[1] > score[0]:
            print_pause("Player Two Wins!")
        else:
            print_pause("It's a TIED game!")
        print_pause("GAME OVER")
        return score


if __name__ == '__main__':
    game, state = player_choice()
    # state variable returns whether human mode (True) or comp (False)
    game.play_game(state)

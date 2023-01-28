# TRUE VERSION
OPPONENT_ROCK = ROCK = 'A'
OPPONENT_PAPER = PAPER = 'B'
OPPONENT_SCISSORS = SCISSORS = 'C'

MEANS_LOSE = 'X'
MEANS_DRAW = 'Y'
MEANS_WIN = 'Z'

WIN_POINTS = 6
DRAW_POINTS = 3
LOSE_POINTS = 0

ROCK_POINTS = 1
PAPER_POINTS = 2
SCISSORS_POINTS = 3

# PLAYER VERSION
PLAYER_ROCK = 'X'
PLAYER_PAPER = 'Y'
PLAYER_SCISSORS = 'Z'
SHAPE_BEATING_SCORE_SCHEMA_PLAYER_VERSION = {
    (OPPONENT_ROCK, PLAYER_PAPER): PAPER_POINTS + WIN_POINTS,
    (OPPONENT_ROCK, PLAYER_SCISSORS): SCISSORS_POINTS + LOSE_POINTS,

    (OPPONENT_PAPER, PLAYER_ROCK): ROCK_POINTS + LOSE_POINTS,
    (OPPONENT_PAPER, PLAYER_SCISSORS): SCISSORS_POINTS + WIN_POINTS,

    (OPPONENT_SCISSORS, PLAYER_ROCK): ROCK_POINTS + WIN_POINTS,
    (OPPONENT_SCISSORS, PLAYER_PAPER): PAPER_POINTS + LOSE_POINTS,

    (OPPONENT_ROCK, PLAYER_ROCK): ROCK_POINTS + DRAW_POINTS,
    (OPPONENT_PAPER, PLAYER_PAPER): PAPER_POINTS + DRAW_POINTS,
    (OPPONENT_SCISSORS, PLAYER_SCISSORS): SCISSORS_POINTS + DRAW_POINTS
}
#

SHAPE_BEATING_SCORE_SCHEMA_TRUE_VERSION = {
    (OPPONENT_ROCK, MEANS_WIN): PAPER_POINTS + WIN_POINTS,
    (OPPONENT_ROCK, MEANS_DRAW): ROCK_POINTS + DRAW_POINTS,
    (OPPONENT_ROCK, MEANS_LOSE): SCISSORS_POINTS + LOSE_POINTS,

    (OPPONENT_PAPER, MEANS_WIN): SCISSORS_POINTS + WIN_POINTS,
    (OPPONENT_PAPER, MEANS_DRAW): PAPER_POINTS + DRAW_POINTS,
    (OPPONENT_PAPER, MEANS_LOSE): ROCK_POINTS + LOSE_POINTS,

    (OPPONENT_SCISSORS, MEANS_WIN): ROCK_POINTS + WIN_POINTS,
    (OPPONENT_SCISSORS, MEANS_DRAW): SCISSORS_POINTS + DRAW_POINTS,
    (OPPONENT_SCISSORS, MEANS_LOSE): PAPER_POINTS + LOSE_POINTS,
}


def play_player_version_round(opponent_shape, player_shape):
    score = SHAPE_BEATING_SCORE_SCHEMA_PLAYER_VERSION[(opponent_shape, player_shape)]
    return score


def play_normal_round(opponent_shape, player_action):
    score = SHAPE_BEATING_SCORE_SCHEMA_TRUE_VERSION[(opponent_shape, player_action)]
    return score


if __name__ == '__main__':
    player_version_score = 0
    player_actual_score = 0
    with open('inputs/2_rock_paper_scissors.txt') as file:
        for line in file.readlines():
            round_ = line.strip()
            player_version_score += play_player_version_round(*round_.split())
            player_actual_score += play_normal_round(*round_.split())

    print(f"Player version score is {player_version_score} points")
    print(f"Player actual score is {player_actual_score} points")


'''
--- Day 2: Rock Paper Scissors ---
The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.
Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors 
using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. 
If both players choose the same shape, the round instead ends in a draw. Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) 
that they say will be sure to help you win. "The first column is what your opponent is going to play: 
A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. 
Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. 
The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus 
the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z
This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). 
This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). 
This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?
'''
'''
--- Part Two ---
The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: 
X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"
The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. 

The example above now goes like this:

In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
'''
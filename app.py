#
# Copyright 2020-2021 AdventureWorks, Inc. or its affiliates. All Rights Reserved.
# This file is licensed under the Crowdblink License, Version 1.0 (the "License").
# You may not use this file except in compliance with the License. A copy of
# the License is located at http://aws.adventureworks.com/license/
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
"""
Module to handle tennis scoring
"""
import random
from enum import Enum


class Player(Enum):
    ONE = 1
    TWO = 2

    def __str__(self):
        if self == Player.ONE:
            return "Player-ONE"
        elif self == Player.TWO:
            return "Player-TWO"

    @staticmethod
    def to_string(value):
        for member in Player:
            if member.value == value:
                return str(member)
        raise ValueError("Invalid Player!")


class TennisScoringBoard:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0
        self.player1_games = 0
        self.player2_games = 0
        self.player1_sets = 0
        self.player2_sets = 0
        self.game_over = False

    def update_score(self, point_winner):
        if point_winner == 1:
            self.player1_points += 1
        else:
            self.player2_points += 1
        # REQ-1 Player with 4 points wins the game
        # REQ-2 Player needs to win by 2 points.
        if self.player1_points >= 4 and self.player1_points - self.player2_points >= 2:
            self.player1_games += 1
            self.reset_points()
        elif self.player2_points >= 4 and self.player2_points - self.player1_points >= 2:
            self.player2_games += 1
            self.reset_points()

        if self.player1_games >= 6 and self.player1_games - self.player2_games >= 2:
            self.player1_sets += 1
            self.reset_games()
        elif self.player2_games >= 6 and self.player2_games - self.player1_games >= 2:
            self.player2_sets += 1
            self.reset_games()

        # REQ-3 Three set contest
        if self.player1_sets == 2 or self.player2_sets == 2:
            self.game_over = True

    def reset_points(self):
        self.player1_points = 0
        self.player2_points = 0

    def reset_games(self):
        self.player1_games = 0
        self.player2_games = 0

    def display_score(self):
        print("--------------")
        print("Score:")
        print(f"{self.player1_name}: Sets - {self.player1_sets} | Games - {self.player1_games} | Points - {self.points_to_string(self.player1_points)}")
        print(f"{self.player2_name}: Sets - {self.player2_sets} | Games - {self.player2_games} | Points - {self.points_to_string(self.player2_points)}")
        print("--------------")

    @staticmethod
    def points_to_string(points):
        if points == 0:
            return "0"
        elif points == 1:
            return "15"
        elif points == 2:
            return "30"
        elif points == 3:
            return "40"
        elif points == 4:
            return "Game"
        else:
            return ""


# Example usage:
player1_name = "Player One"
player2_name = "Player Two"
scoring_board = TennisScoringBoard(player1_name, player2_name)

while not scoring_board.game_over:
    print("--Starting new game--.")
    point_winner = random.choice([Player.ONE, Player.TWO])
    print(f"{str(point_winner)} won a point...")
    scoring_board.update_score(point_winner)
    scoring_board.display_score()

print("--Game finished--")

# Celebrate the winner
if scoring_board.player1_sets == 2:
    print(f"{player1_name} wins the match!")
else:
    print(f"{player2_name} wins the match!")

#
# Copyright 2020-2021 AdventureWorks, Inc. or its affiliates. All Rights Reserved.
# This file is licensed under the AdventureWorks License, Version 1.0 (the "License").
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
    """
        Represents a player in a game.
        Each player is assigned a unique identifier and is represented as a string.

        Raises:
            ValueError: Raies when the player identifier is not valid value

        Returns:
            Player: The player.
    """
    ONE = 1
    TWO = 2

    def __str__(self):
        """
        Returns the string representation of the player.

        Returns:
            str: The string representation of the player.
        """
        if self == Player.ONE:
            return "Player-ONE"
        elif self == Player.TWO:
            return "Player-TWO"

    @staticmethod
    def to_string(value):
        """
        Converts the given player's numeric value to its corresponding string representation.

        Args:
            value (int): The value of the player.

        Returns:
            str: The string representation of the player.

        Raises:
            ValueError: If the value is invalid.
        """
        for member in Player:
            if member.value == value:
                return str(member)
        raise ValueError("Invalid Player!")


class TennisScoringBoard:

    """
    Represents the tennis scoring board for tracking the progress of a tennis match.
    """

    def __init__(self, player1_name, player2_name):
        """
        Initializes the TennisScoringBoard with the names of the two players.

        Args:
            player1_name (str): The name of player one.
            player2_name (str): The name of player two.
        """
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
        """
        Updates the score based on the winner of a point.

        Args:
            point_winner (int): The value representing the winner of the point (1 or 2).
        """

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
        """
        Resets the points for both players to zero.
        """
        self.player1_points = 0
        self.player2_points = 0

    def reset_games(self):
        """
        Resets the games for both players to zero.
        """
        self.player1_games = 0
        self.player2_games = 0

    def display_score(self):
        """
        Displays the current score board.
        """
        print("--------------")
        print("Score:")
        print(f"{self.player1_name}: Sets - {self.player1_sets} | Games - {self.player1_games} | Points - {self.points_to_string(self.player1_points)}")
        print(f"{self.player2_name}: Sets - {self.player2_sets} | Games - {self.player2_games} | Points - {self.points_to_string(self.player2_points)}")
        print("--------------")

    @staticmethod
    def points_to_string(points):
        """
        Converts the given points to their corresponding string representation.

        Args:
            points (int): The points to be converted.

        Returns:
            str: The string representation of the points.
        """
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
            raise ValueError("Invalid value!")


# Example usage: Start with two player, assuming singles; later onto doubles.
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

# Player won 2/3 sets.
# Celebrate the winner
if scoring_board.player1_sets == 2:
    print(f"{player1_name} wins the match!")
else:
    print(f"{player2_name} wins the match!")

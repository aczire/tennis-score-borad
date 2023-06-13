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
Player Module: Represents a player in the game.
"""
# Generated file, disable docstrings, casing, module length requirements.
# pylint: disable=C0115,C0116,C0103,C0302

import logging
import random

from dataclasses import dataclass
from models.player import Player

log = logging.getLogger(__name__)


@dataclass
class Game:
    """Represents a game between two players."""
    player1: Player
    player2: Player
    game_winner: Player = None
    game_over: bool = False

    def play_point(self) -> Player:
        """Simulates a point being played and updates the game status."""
        point_winner = random.choice([self.player1, self.player2])
        point_winner.win_point()
        self.check_game_status()
        return point_winner

    def check_game_status(self):
        """Checks if the game is over based on the point scores.
        Requires: 
        1.Player wins if he scores 4 points.
        2.Only if there is a 2 point lead.

        """
        # REQ-1 Player with 4 points wins the game
        # REQ-2 Player needs to win by 2 points.
        if max(self.player1.points, self.player2.points) >= 4 and \
                abs(self.player1.points - self.player2.points) >= 2:
            self.game_over = True

        if self.player1.points >= 4 and self.player1.points - self.player2.points >= 2:
            self.game_winner = self.player1
        elif self.player2.points >= 4 and self.player2.points - self.player1.points >= 2:
            self.game_winner = self.player2
        # else // demontrates why `always else`` is not always a good idea!

    def reset_points(self):
        """Resets the players' points to 0 for a new game."""
        self.player1.reset_points()
        self.player2.reset_points()

    def get_score(self):
        """Returns the current score of the players."""
        return f"{self.player1.points}-{self.player2.points}\n"

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
            return "-"  # TODO: Handle Deuce.

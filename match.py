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
# pylint: disable=C0115,C0116,C0103,C0302,W1203

import logging
from typing import Optional, Union, cast

from dataclasses import dataclass
from models.player import Player
from models.game import Game


log = logging.getLogger(__name__)


@dataclass
class Match:
    """Represents a tournament between two players."""
    player1: Player
    player2: Player
    player1_games: int = 0
    player2_games: int = 0
    player1_sets: int = 0
    player2_sets: int = 0
    match_over: bool = False

    def play_match(self):
        """Simulates a match between the players, consisting of multiple games."""
        # TODO: Separate out game point check and game ##spearation_of_concern
        while not self.match_over:
            game = Game(self.player1, self.player2)
            log.info("-- starting new game --")
            while not game.game_over:
                player_game = game.play_point()
                log.debug(f"{player_game.name} won a point")

            log.info(f"Game: Point status: {game.get_score()}")
            player_set, p1, p2 = self.update_score(game)
            if player_set:
                log.info(
                    f"{cast(Player, player_set).name} won the set. ({p1}-{p2})")
            self.check_match_status()

    def update_score(self, game: Game) -> Union[Optional[Player], int, int]:
        """Updates the score of the match based on the result of a game."""
        if game.player1.points > game.player2.points:
            self.player1_games += 1
        else:
            self.player2_games += 1

        _set: Player = None
        _p1 = 0
        _p2 = 0
        if self.player1_games >= 6 and self.player1_games - self.player2_games >= 2:
            self.player1_sets += 1
            _set, _p1, _p2 = (
                self.player1, self.player1_games, self.player2_games)
            self.reset_games()
        elif self.player2_games >= 6 and self.player2_games - self.player1_games >= 2:
            self.player2_sets += 1
            _set, _p1, _p2 = (
                self.player2, self.player1_games, self.player2_games)
            self.reset_games()

        self.reset_points(game)

        return _set, _p1, _p2

    def reset_points(self, game: Game):
        """Resets the players' points for a new game."""
        game.reset_points()

    def get_score(self):
        """Returns the current score of the games."""
        return f"Player-1 Games: {self.player1_games} - Player-2 Games: {self.player2_games}\n"

    def check_match_status(self):
        """Checks if the match is over based on the game scores."""

        if self.player1_sets == 2 or self.player2_sets == 2:
            self.match_over = True

        return self.match_over

    def reset_games(self):
        """Resets the game scores for a new set."""
        self.player1_games = 0
        self.player2_games = 0

    def celebrate_winner(self):
        """Returns the message announcing the winner of the match."""
        if self.player1_sets > self.player2_sets:
            return f"{self.player1.name} wins the match!"
        else:
            return f"{self.player2.name} wins the match!"

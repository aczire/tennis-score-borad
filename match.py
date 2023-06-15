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
from typing import List, Optional, Union, cast

from dataclasses import dataclass
from models.player import Player
from models.game import Game


log = logging.getLogger(__name__)


@dataclass
class Set:
    """
    Represents a set in a match between two players.
    """

    games: List[Game] = []

    def __post_init__(self):
        if self.games is None:
            self.games = []

    def update_score(self, game: Game) -> Union[Optional[Player], int, int]:
        """
        Updates the score of the set based on the result of a game.

        Args:
            game: The game played within the set.

        Returns:
            A tuple containing the winning player, and the game scores.

        """
        _player: Player
        _p1 = 0
        _p2 = 0

        if game.player1.points > game.player2.points:
            _player, _p1, _p2 = game.player1, game.player1.points, game.player2.points
        else:
            _player, _p1, _p2 = game.player2, game.player1.points, game.player2.points

        self.games.append(game)

        return _player, _p1, _p2

    def is_set_over(self) -> bool:
        """
        Checks if the set is over.

        Returns:
            True if the set is over, False otherwise.
        """
        if len(self.games) < 6:
            return False

        player1_games = sum(
            1 for game in self.games if game.player1.points > game.player2.points)
        player2_games = sum(
            1 for game in self.games if game.player2.points > game.player1.points)

        return abs(player1_games - player2_games) >= 2 and (player1_games >= 6 or player2_games >= 6)


@dataclass
class Match:
    """
    Represents a tournament between two players.
    """

    player1: Player
    player2: Player
    sets: List[Set] = []

    def __post_init__(self):
        if self.sets is None:
            self.sets = []

    def play_match(self):
        """
        Simulates a match between the players, consisting of multiple sets.
        """
        while not self.is_match_over():
            _set = Set()
            log.info("-- starting new set --")
            self.play_set(_set)
            self.sets.append(_set)

    def play_set(self, _set: Set):
        """
        Plays a set within the match, consisting of multiple games.

        Args:
            _set: The set to be played.
        """
        while not _set.is_set_over():
            game = Game(self.player1, self.player2)
            log.info("-- starting new game --")
            self.play_game(game, _set)

    def play_game(self, game: Game, _set: Set):
        """
        Plays a game within a set.

        Args:
            game: The game to be played.
            _set: The set containing the game.
        """
        while not game.is_game_over():
            player_game = game.play_point()
            log.debug(f"{player_game.name} won a point")

        log.info(f"Game: Point status: {game.get_score()}")
        player_set, p1, p2 = _set.update_score(game)
        if player_set:
            log.info(
                f"{cast(Player, player_set).name} won the set. ({p1}-{p2})")

    def is_match_over(self) -> bool:
        """
        Checks if the match is over based on the sets won by each player.

        Returns:
            True if the match is over, False otherwise.
        """
        return len(self.sets) >= 2 or \
            (len(self.sets) == 1 and self.sets[0].is_set_over())

    def celebrate_winner(self) -> str:
        """
        Returns the message announcing the winner of the match.

        Returns:
            The message announcing the winner of the match.
        """
        player1_sets = sum(
            1 for _set in self.sets if _set.games and _set.games[-1].player1.points > _set.games[-1].player2.points)
        player2_sets = sum(
            1 for _set in self.sets if _set.games and _set.games[-1].player2.points > _set.games[-1].player1.points)

        if player1_sets > player2_sets:
            return f"{self.player1.name} wins the match!"
        elif player2_sets > player1_sets:
            return f"{self.player2.name} wins the match!"
        else:
            return "The match ended in a draw."

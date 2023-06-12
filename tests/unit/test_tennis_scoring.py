"""
### Tests

Run `python -m pytest ./tests/ -v ` to run tests
Requirements:
# pynamodb 5.3.0-1
# botocore-1.29.41
# moto-4.0.12
Ref: https://github.com/pynamodb/PynamoDB/pull/1083
"""

# pylint: disable=C0116

from enum import Enum
import json
import logging


from functools import wraps
from pathlib import Path

import pytest


try:
    import os.path
    import sys

    sys.path.insert(
        1,
        os.path.dirname(  # workspace
            os.path.dirname(  # workspace/tests
                os.path.dirname(  # workspace/tests/unit
                    os.path.abspath(__file__)  # this file
                )
            )
        ),
    )
    from app import Player, TennisScoringBoard
    from rellib.order import Order as dboOrder
except ModuleNotFoundError as ex:
    print(ex)

logger = logging.getLogger(__name__)


# Test Player Enum


def test_player_to_string():
    assert str(Player.ONE) == "Player-ONE"
    assert str(Player.TWO) == "Player-TWO"


def test_player_to_string_invalid():
    with pytest.raises(ValueError):
        Player.to_string(3)


def test_player_to_string_valid():
    assert Player.to_string(1) == "Player-ONE"
    assert Player.to_string(2) == "Player-TWO"

# Test TennisScoringBoard Class


def test_tennis_scoring_board_initialization():
    scoring_board = TennisScoringBoard("Player One", "Player Two")
    assert scoring_board.player1_name == "Player One"
    assert scoring_board.player2_name == "Player Two"
    assert scoring_board.player1_points == 0
    assert scoring_board.player2_points == 0
    assert scoring_board.player1_games == 0
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 0
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == False


def test_tennis_scoring_board_update_score():
    """Simulate a 2 set game
    """
    scoring_board = TennisScoringBoard("Player One", "Player Two")

    scoring_board.update_score(1)
    assert scoring_board.player1_points == 1
    assert scoring_board.player2_points == 0
    assert scoring_board.player1_games == 0
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 0
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == False

    scoring_board.update_score(2)
    assert scoring_board.player1_points == 1
    assert scoring_board.player2_points == 1
    assert scoring_board.player1_games == 0
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 0
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == False

    scoring_board.update_score(1)
    scoring_board.update_score(1)
    scoring_board.update_score(1)  # game point, score reset
    assert scoring_board.player1_points == 0
    assert scoring_board.player2_points == 0
    assert scoring_board.player1_games == 1
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 0
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == False

    scoring_board.update_score(1)
    scoring_board.update_score(1)
    scoring_board.update_score(1)
    scoring_board.update_score(1)  # game point, won the set, score reset
    assert scoring_board.player1_points == 0
    assert scoring_board.player2_points == 0
    assert scoring_board.player1_games == 2
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 0
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == False

    scoring_board.update_score(1)
    assert scoring_board.player1_points == 1
    assert scoring_board.player2_points == 0
    assert scoring_board.player1_games == 2
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 0
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == False

    scoring_board.update_score(1)
    scoring_board.update_score(1)
    # Player 2 wins the next 3 points
    scoring_board.update_score(2)
    scoring_board.update_score(2)
    scoring_board.update_score(2)
    # Player 1 recaptures the game
    scoring_board.update_score(1)
    assert scoring_board.player1_points == 4
    assert scoring_board.player2_points == 3
    assert scoring_board.player1_games == 2
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 0
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == False

    scoring_board.update_score(1)  # game point, won the set.

    # Player 1 wins the next round
    for i in range(0, 3):
        scoring_board.update_score(1)
        scoring_board.update_score(1)
        scoring_board.update_score(1)
        scoring_board.update_score(1)
    assert scoring_board.player1_points == 0
    assert scoring_board.player2_points == 0
    assert scoring_board.player1_games == 0
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 1
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == False

    for set_number in range(6):
        print("Set", set_number + 1)
        for game_number in range(4):
            print("Game", game_number + 1)
            scoring_board.update_score(1)

    assert scoring_board.player1_points == 0
    assert scoring_board.player2_points == 0
    assert scoring_board.player1_games == 0
    assert scoring_board.player2_games == 0
    assert scoring_board.player1_sets == 2
    assert scoring_board.player2_sets == 0
    assert scoring_board.game_over == True


def test_tennis_scoring_board_reset_points():
    """Tests points reset
    """
    scoring_board = TennisScoringBoard("Player One", "Player Two")

    scoring_board.player1_points = 3
    scoring_board.player2_points = 2
    scoring_board.reset_points()
    assert scoring_board.player1_points == 0
    assert scoring_board.player2_points == 0


def test_tennis_scoring_board_reset_games():
    """Tests resetting games
    """
    scoring_board = TennisScoringBoard("Player One", "Player Two")

    scoring_board.player1_games = 4
    scoring_board.player2_games = 3
    scoring_board.reset_games()
    assert scoring_board.player1_games == 0
    assert scoring_board.player2_games == 0


def test_tennis_scoring_board_points_to_string():
    """Tests score to point conversion
    """
    assert TennisScoringBoard.points_to_string(0) == "0"
    assert TennisScoringBoard.points_to_string(1) == "15"
    assert TennisScoringBoard.points_to_string(2) == "30"
    assert TennisScoringBoard.points_to_string(3) == "40"
    assert TennisScoringBoard.points_to_string(4) == "Game"
    with pytest.raises(ValueError):
        TennisScoringBoard.points_to_string(5)


# Run the tests
if __name__ == "__main__":
    pytest.main()

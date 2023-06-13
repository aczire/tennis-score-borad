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

import logging
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
    from models.player import Player
    from models.game import Game
except ModuleNotFoundError as ex:
    print(ex)

logger = logging.getLogger(__name__)


@pytest.fixture
def game():
    """Creates the fixture with two players

    Returns:
        Game: Return Game with Players
    """
    player1 = Player("John")
    player2 = Player("Jane")
    return Game(player1, player2)


def test_play_point(game: Game):  # pylint:disable=W0621
    """Tests play point.

    Args:
        game (Game): The game
    """
    initial_points1 = game.player1.points
    initial_points2 = game.player2.points

    winner = game.play_point()

    assert (game.player1.points != initial_points1) or (
        game.player2.points != initial_points2)
    assert winner in [game.player1, game.player2]


def test_check_game_status(game: Game):  # pylint:disable=W0621
    """Check the game status after game

    Args:
        game (Game): _description_
    """
    game.player1.points = 2
    game.player2.points = 4
    game.check_game_status()
    assert game.game_over
    assert game.game_winner is not None
    assert game.game_winner is game.player2

    game.player1.points = 4
    game.player2.points = 2
    game.check_game_status()
    assert game.game_over
    assert game.game_winner == game.player1

    game.player1.points = 3
    game.player2.points = 5
    game.check_game_status()
    assert game.game_over
    assert game.game_winner == game.player2


def test_reset_points(game: Game):  # pylint:disable=W0621
    game.player1.points = 3
    game.player2.points = 2
    game.reset_points()
    assert game.player1.points == 0
    assert game.player2.points == 0


def test_get_score(game: Game):  # pylint:disable=W0621
    game.player1.points = 2
    game.player2.points = 3
    score = game.get_score()
    assert score == "2-3\n"


def test_points_to_string():
    assert Game.points_to_string(0) == "0"
    assert Game.points_to_string(1) == "15"
    assert Game.points_to_string(2) == "30"
    assert Game.points_to_string(3) == "40"
    assert Game.points_to_string(4) == "Game"
    with pytest.raises(ValueError):
        Game.points_to_string(5)

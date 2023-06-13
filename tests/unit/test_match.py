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

import itertools
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
    from match import Match
except ModuleNotFoundError as ex:
    print(ex)

logger = logging.getLogger(__name__)


@pytest.fixture
def match():
    player1 = Player("John")
    player2 = Player("Jane")
    return Match(player1, player2)


def test_play_match(match: Match, mocker):  # pylint:disable=W0621
    # Mock the Game class to simulate a game with predefined results
    # TODO: Reduce play_match complexit so that we can test it independantly.
    mocker.patch.object(Game, 'play_point')
    game = Game(match.player1, match.player2)
    game.play_point.side_effect = itertools.cycle([match.player1])
    mocker.patch.object(match, 'update_score')

    match.play_match()

    assert match.player1_games == 2
    assert match.player2_games == 2
    assert match.player1_sets == 0
    assert match.player2_sets == 0
    assert match.match_over


def test_update_score(match: Match):  # pylint:disable=W0621
    game = Game(match.player1, match.player2)
    game.player1.points = 4
    game.player2.points = 2

    player_set, p1, p2 = match.update_score(game)

    assert player_set is None
    assert p1 == 0
    assert p2 == 0
    assert match.player1_games == 1
    assert match.player2_games == 0
    assert match.player1_sets == 0
    assert match.player2_sets == 0

    game.player1.points = 4
    game.player2.points = 6

    player_set, p1, p2 = match.update_score(game)

    assert player_set is None
    assert p1 == 0
    assert p2 == 0
    assert match.player1_games == 1
    assert match.player2_games == 1
    assert match.player1_sets == 0
    assert match.player2_sets == 0

    match.player1_games = 5
    match.player2_games = 6
    # Player 2 wins next game
    game.player1.points = 4
    game.player2.points = 6

    player_set, p1, p2 = match.update_score(game)

    assert player_set == match.player2
    assert p1 == 5
    assert p2 == 7
    assert match.player1_games == 0
    assert match.player2_games == 0
    assert match.player1_sets == 0
    assert match.player2_sets == 1


def test_reset_points(match: Match):  # pylint:disable=W0621
    game = Game(match.player1, match.player2)
    game.player1.points = 3
    game.player2.points = 2

    match.reset_points(game)

    assert game.player1.points == 0
    assert game.player2.points == 0


def test_get_score(match: Match):  # pylint:disable=W0621
    match.player1_games = 2
    match.player2_games = 3

    score = match.get_score()

    assert score == "Player-1 Games: 2 - Player-2 Games: 3\n"


def test_check_match_status(match: Match):  # pylint:disable=W0621
    match.player1_sets = 1

    match_over = match.check_match_status()

    assert not match_over

    match.player1_sets = 2

    match_over = match.check_match_status()

    assert match_over


def test_reset_games(match: Match):  # pylint:disable=W0621
    match.player1_games = 5
    match.player2_games = 3

    match.reset_games()

    assert match.player1_games == 0
    assert match.player2_games == 0


def test_celebrate_winner(match: Match):  # pylint:disable=W0621
    match.player1_sets = 2
    winner_message = match.celebrate_winner()
    assert winner_message == "John wins the match!"

    match.player2_sets = 2
    winner_message = match.celebrate_winner()
    assert winner_message == "Jane wins the match!"

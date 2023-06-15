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
import logging

from models.player import Player
from match import Match

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

PLAYER_ONE = "Player One"
PLAYER_TWO = "Player Two"
player1 = Player(PLAYER_ONE)
player2 = Player(PLAYER_TWO)

match = Match(player1, player2)
log.info("-- Starting the match --")
match.play_match()
log.info(match.celebrate_winner())

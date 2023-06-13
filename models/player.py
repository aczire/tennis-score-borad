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
Represents a player in the game.
"""
# Generated file, disable docstrings, casing, module length requirements.
# pylint: disable=C0115,C0116,C0103,C0302

from dataclasses import dataclass


@dataclass
class Player:
    """Represents a player in the game."""
    name: str
    points: int = 0

    def win_point(self):
        """Increments the player's point by 1."""
        self.points += 1

    def reset_points(self):
        """Resets the player's points to 0."""
        self.points = 0

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from runner.koan import *
from koans.about_scoring_project import score
from koans.about_dice_project import DiceSet

    # 2 or more players - start w/ 2 hardcoded

    # i can roll single or multiple dice
    # rolls dont know about one another

    # DiceSet class
        # scoring dice should be removed for non scoring dice
        # if no dice are left in 1 roll, then roll all dice again

    # turn's accumulated score is kept and added to the players
        # accumulated total if they don't have a zero
        # point roll

    # a player can choose to roll again after each roll unless
        # it is a 0 point roll

    # start
    # if no points, then must roll 300 min to get started

    # end
    # 3000+ points sends to final round

    # final round
        # one more roll
        # highest score after roll wins
class Player:

    # player has game points
    # player has a turn

    pass

class Game:
    # game has num of players

    # game should know when time for final round
    pass

class Turn:
    def __init__(self):
        self._dice = DiceSet()
        self._active_dice = []
        self._current_score = 0

    @property
    def active_dice(self):
        return self._active_dice

    @active_dice.setter
    def active_dice(self, dice):
        self._active_dice = dice

    @property
    def current_score(self):
        return self._current_score

    def roll(self):
        if len(self._active_dice) == 0:
            self._dice.roll(5)
        else:
            self._dice.roll(len(self._active_dice))

        self.active_dice = self._dice.values

    def calculate_score(self, dice):
        if len(dice) == 0:
            return 0

        self.active_dice = []
        score = 0
        count_dict = {}
        scoring_rules = {
            1: 100,
            5: 50,
            '3_1': 1000,
            '3_5': 500
        }

        # create a dict of dice count
        for die in dice:
            if die in count_dict.keys():
                count_dict[die] += 1
            else:
                count_dict[die] = 1

        # calc score using dict
        for key, value in count_dict.items():
            if key == 1 or key == 5:
                if value >= 3:
                    score += scoring_rules["3_%s" %(key)]
                    value -= 3
                if value > 0:
                    score += (value * scoring_rules[key])
            elif value >= 3:
                score += (100 * key)
            else:
                self._active_dice.extend([key] * value)

        self._current_score += score

        return score


class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py

    def test_score_of_an_empty_list_is_zero(self):
        turn = Turn()
        turn.calculate_score([])
        self.assertEqual(0, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_a_single_roll_of_5_is_50(self):
        turn = Turn()
        turn.calculate_score([5])
        self.assertEqual(50, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_a_single_roll_of_1_is_100(self):
        turn = Turn()
        turn.calculate_score([1])
        self.assertEqual(100, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_multiple_1s_and_5s_is_the_sum_of_individual_scores(self):
        turn = Turn()
        turn.calculate_score([1,5,5,1])
        self.assertEqual(300, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_single_2s_3s_4s_and_6s_are_zero(self):
        ### FEATURE ###
        # if active_dice same after scoring, then
        # turn is over
        turn = Turn()
        turn.calculate_score([2,3,4,6])
        self.assertEqual(0, turn.current_score)
        self.assertEqual([2,3,4,6], turn.active_dice)

    def test_score_of_a_triple_1_is_1000(self):
        turn = Turn()
        turn.calculate_score([1,1,1])
        self.assertEqual(1000, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_other_triples_is_100x(self):
        turn = Turn()
        turn.calculate_score([2,2,2])
        self.assertEqual(200, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.calculate_score([3,3,3])
        self.assertEqual(500, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.calculate_score([4,4,4])
        self.assertEqual(900, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.calculate_score([5,5,5])
        self.assertEqual(1400, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.calculate_score([6,6,6])
        self.assertEqual(2000, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_mixed_is_sum(self):
        turn = Turn()
        turn.calculate_score([2,5,2,2,3])
        self.assertEqual(250, turn.current_score)
        self.assertEqual([3], turn.active_dice)

        ### FEATURE
        # this would turn the corner and have a fresh 5!!
        turn.calculate_score([5,5,5,5])
        self.assertEqual(800, turn.current_score)
        self.assertEqual([], turn.active_dice)

        ### FEATURE
        # this would turn the corner and have a fresh 5!!
        turn.calculate_score([1,1,1,5,1])
        self.assertEqual(1950, turn.current_score)
        self.assertEqual([], turn.active_dice)


    def test_ones_not_left_out(self):
        turn = Turn()
        turn.calculate_score([1,2,2,2])
        self.assertEqual(300, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.calculate_score([1,5,2,2,2])
        self.assertEqual(650, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_first_roll_returns_5_dice(self):
        turn = Turn()
        turn.roll()
        self.assertEqual(5, len(turn.active_dice))

    def test_first_roll_calc_increases_score(self):
        turn = Turn()
        turn.roll()
        turn.calculate_score(turn.active_dice)
        self.assertGreater(turn.current_score, 0)

    def test_a_roll_removes_scoring_dice_from_next_roll(self):
        turn = Turn()
        # first roll
        turn.calculate_score([1,1,5,3,4])
        dice_count = len(turn.active_dice)
        self.assertEqual([3,4], turn.active_dice)

        # second roll before scoring
        turn.roll()
        self.assertEqual(2, len(turn.active_dice))


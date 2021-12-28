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

from typing import List
from operator import attrgetter
from runner.koan import *
from koans.about_scoring_project import score
from koans.about_dice_project import DiceSet
class Turn:
    def __init__(self):
        self._dice = DiceSet()
        self._active_dice = []
        self._current_score = 0
        self._turn_over = True

    @property
    def active_dice(self):
        return self._active_dice

    @active_dice.setter
    def active_dice(self, dice):
        self._active_dice = dice

    @property
    def current_score(self):
        return self._current_score

    @property
    def turn_over(self):
        return self._turn_over

    @turn_over.setter
    def turn_over(self, is_over):
        self._turn_over = is_over

    def roll(self):
        if self.turn_over:
            raise TurnError('It must be your turn to roll.')

        if len(self._active_dice) == 0:
            self._dice.roll(5)
        else:
            self._dice.roll(len(self._active_dice))

        self.active_dice = self._dice.values
        return self.active_dice

    def calculate_score(self):
        if self.turn_over:
            raise TurnError('It must be your turn to score.')

        if len(self.active_dice) == 0:
            return 0

        calculating_dice = self.active_dice.copy()
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
        for die in calculating_dice:
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
                self.active_dice.extend([key] * value)

        self.handle_zero_score(score)

        self._current_score += score

        return score

    def handle_zero_score(self, score):
        if score != 0:
            return
        self.clean_up_after_turn()

    def clean_up_after_turn(self):
        self._current_score = 0
        self._turn_over = True
        self.active_dice = []

class Player(Turn):
    def __init__(self, name):
        self._name = name
        self._total_points = 0
        self._is_winner = False
        super().__init__()

    @property
    def name(self):
        return self._name

    @property
    def total_points(self):
        return self._total_points

    @total_points.setter
    def total_points(self, new_total):
        self._total_points = new_total

    @property
    def is_winner(self):
        return self._is_winner

    @is_winner.setter
    def is_winner(self, new_boolean: bool):
        self._is_winner = new_boolean

    def end_turn(self):
        if self.total_points + self.current_score < 300:
            raise ScoreError('You need a minimum of 300 points to end your turn.')
        self.total_points += self.current_score
        self.clean_up_after_turn()
        return 'Total points after turn: ' + str(self.total_points)

class Game():
    def __init__(self):
        self._players = []
        self._active_player_index = None
        self._final_round = False
        self._final_round_turns = 0
        self._game_over = False

    @property
    def players(self):
        return self._players

    @property
    def active_player_index(self):
        return self._active_player_index

    @active_player_index.setter
    def active_player_index(self, new_index):
        self._active_player_index = new_index

    @property
    def final_round(self):
        return self._final_round

    @final_round.setter
    def final_round(self, is_final):
        self._final_round = is_final

    def add_player(self, name):
        player = Player(name)
        self._players.append(player)
        return player

    def new_turn(self):
        if self._game_over == True:
            raise GameError('The game is over!')

        self.set_active_player_index()
        active_player = self.players[self.active_player_index]

        a_player_has_3000 = len([player for player in self.players if player.total_points >= 3000]) == 1

        if a_player_has_3000:
            self.final_round = True

        if self.final_round == True and active_player.total_points < 3000:
            self._final_round_turns += 1

        self.allow_player_to_roll(active_player)

        if self._final_round_turns >= len(self.players) - 1:
            self._game_over = True

        return active_player

    def set_active_player_index(self):
        if self.active_player_index == None:
            self.active_player_index = 0
        elif self.active_player_index + 1 >= len(self.players):
            self.active_player_index = 0
        else:
            self.active_player_index += 1

    def set_winner(self):
        if self._game_over == False:
            raise GameError('There can only be a winner when the game is over!')
        winning_player = max(self.players, key=attrgetter('total_points'))
        winning_player.is_winner = True

        return winning_player.name + ' is the winner!'

    def allow_player_to_roll(self, player):
        player.turn_over = False

class TurnError(Exception):
    pass

class ScoreError(Exception):
    pass

class GameError(Exception):
    pass

class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py

    def test_score_of_an_empty_list_is_zero(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = []
        turn.calculate_score()
        self.assertEqual(0, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_a_single_roll_of_5_is_50(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [5]
        turn.calculate_score()
        self.assertEqual(50, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_a_single_roll_of_1_is_100(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [1]
        turn.calculate_score()
        self.assertEqual(100, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_multiple_1s_and_5s_is_the_sum_of_individual_scores(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [1,5,5,1]
        turn.calculate_score()
        self.assertEqual(300, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_single_2s_3s_4s_and_6s_are_zero(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [2,3,4,6]
        turn.calculate_score()
        self.assertEqual(0, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_a_triple_1_is_1000(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [1,1,1]
        turn.calculate_score()
        self.assertEqual(1000, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_other_triples_is_100x(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [2,2,2]
        turn.calculate_score()
        self.assertEqual(200, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.active_dice = [3,3,3]
        turn.calculate_score()
        self.assertEqual(500, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.active_dice = [4,4,4]
        turn.calculate_score()
        self.assertEqual(900, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.active_dice = [5,5,5]
        turn.calculate_score()
        self.assertEqual(1400, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.active_dice = [6,6,6]
        turn.calculate_score()
        self.assertEqual(2000, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_score_of_mixed_is_sum(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [2,5,2,2,3]
        turn.calculate_score()
        self.assertEqual(250, turn.current_score)
        self.assertEqual([3], turn.active_dice)

        turn.active_dice = [5,5,5,5]
        turn.calculate_score()
        self.assertEqual(800, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.active_dice = [1,1,1,5,1]
        turn.calculate_score()
        self.assertEqual(1950, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_ones_not_left_out(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [1,2,2,2]
        turn.calculate_score()
        self.assertEqual(300, turn.current_score)
        self.assertEqual([], turn.active_dice)

        turn.active_dice = [1,5,2,2,2]
        turn.calculate_score()
        self.assertEqual(650, turn.current_score)
        self.assertEqual([], turn.active_dice)

    def test_first_roll_returns_5_dice(self):
        turn = Turn()
        turn.turn_over = False
        dice_return = turn.roll()

        self.assertEqual(5, len(turn.active_dice))
        self.assertEqual(5, len(dice_return))
        self.assertEqual(dice_return, turn.active_dice)

    def test_a_roll_removes_scoring_dice_from_next_roll(self):
        turn = Turn()
        turn.turn_over = False
        # first roll
        turn.active_dice = [1,1,5,3,4]
        turn.calculate_score()
        self.assertEqual([3,4], turn.active_dice)

        # second roll before scoring
        return_roll = turn.roll()
        self.assertEqual(2, len(turn.active_dice))
        self.assertEqual(2, len(return_roll))
        self.assertEqual(return_roll, turn.active_dice)

    def test_turn_ends_when_no_scoring_dice(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [3,3,4]
        turn.calculate_score()
        self.assertEqual(True, turn.turn_over)

    def test_non_scoring_roll_zeroes_current_turn_score(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [3,3,4]
        turn.calculate_score()
        self.assertEqual(0, turn.current_score)

    def test_non_scoring_roll_empties_dice_in_hand(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [3,3,4]
        turn.calculate_score()
        self.assertEqual([], turn.active_dice)

    def test_turn_does_not_end_with_scoring_dice(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [1,1,5,3,4]
        turn.calculate_score()
        self.assertEqual(False, turn.turn_over)

    def test_depleting_available_dice_with_scoring_roll_will_replenish_five_dice(self):
        turn = Turn()
        turn.turn_over = False
        turn.active_dice = [5,5,5,5]
        turn.calculate_score()
        self.assertEqual([], turn.active_dice)

        return_roll = turn.roll()
        self.assertEqual(5, len(turn.active_dice))
        self.assertEqual(5, len(return_roll))
        self.assertEqual(turn.active_dice, turn.active_dice)

    def test_no_roll_or_calc_score_when_not_turn(self):
        turn = Turn()
        with self.assertRaises(TurnError):
            turn.roll()
        with self.assertRaises(TurnError):
            turn.calculate_score()

    def test_new_player_has_name_and_points(self):
        player = Player('player 1')
        self.assertEqual(player.name, 'player 1')
        self.assertEqual(player.total_points, 0)
        self.assertEqual(player.turn_over, True)

    def test_ending_player_turn_cleans_up_and_banks_current_score(self):
        player = Player('one')
        player.turn_over = False
        player.active_dice = [1,1,1,5,3]
        player.calculate_score()
        end_turn_return = player.end_turn()
        self.assertEqual(1050, player.total_points)
        self.assertEqual(True, player.turn_over)
        self.assertEqual([], player.active_dice)
        self.assertEqual(0, player.current_score)
        self.assertEqual('Total points after turn: 1050', end_turn_return)

    def test_player_non_scoring_roll_ends_turn_and_total_score_does_not_change(self):
        player = Player('one')
        player.turn_over = False
        player._total_points = 500
        player.active_dice = [3,3,4,4]
        player.calculate_score()
        self.assertEqual(500, player.total_points)
        self.assertEqual(True, player.turn_over)
        self.assertEqual([], player.active_dice)
        self.assertEqual(0, player.current_score)

    def test_minimum_initial_score_of_300(self):
        player = Player('one')
        player.turn_over = False
        player.active_dice = [1,1,3,4,5]
        player.calculate_score()
        with self.assertRaises(ScoreError):
            player.end_turn()
        self.assertEqual(0, player.total_points)
        self.assertEqual(False, player.turn_over)
        self.assertEqual([3,4], player.active_dice)
        self.assertEqual(250, player.current_score)

    def test_new_game_has_empty_players_list(self):
        game = Game()
        self.assertEqual([], game.players)

    def test_adding_players(self):
        game = Game()

        p1 = game.add_player('player 1')
        self.assertEqual('player 1', p1.name)
        self.assertEqual(p1, game.players[0])
        self.assertEqual(1, len(game.players))
        self.assertEqual('player 1', game.players[0].name)

        p2 = game.add_player('player 2')
        self.assertEqual('player 2', p2.name)
        self.assertEqual(p2, game.players[1])
        self.assertEqual(2, len(game.players))
        self.assertEqual('player 2', game.players[1].name)

    def test_new_turn_activates_player_and_checks_for_final_round(self):
        game = Game()
        game.add_player('player 1')
        game.add_player('player 2')
        self.assertEqual(True, game.players[0].turn_over)
        self.assertEqual(True, game.players[1].turn_over)

        player_with_turn = game.new_turn()
        self.assertEqual(False, game.players[0].turn_over)
        self.assertEqual(True, game.players[1].turn_over)
        self.assertEqual(game.players[0], player_with_turn)
        self.assertEqual(0, game.active_player_index)
        self.assertEqual(False, game.final_round)

    def test_final_round_initiation_gives_players_one_more_turn(self):
        game = Game()
        game.add_player('player 1')
        game.add_player('player 2')
        game.active_player_index = 1

        game.players[0].total_points = 2800
        game.players[1].total_points = 3000

        game.new_turn()

        self.assertEqual(0, game.active_player_index)
        self.assertEqual(True, game.final_round)
        self.assertEqual(1, game._final_round_turns)
        self.assertEqual(True, game._game_over)

    def test_end_of_final_round_ends_the_game(self):
        game = Game()
        game.add_player('player 1')
        game.add_player('player 2')
        game.add_player('player 3')
        game.active_player_index = 1

        game.players[0].total_points = 2800
        game.players[1].total_points = 3000
        game.players[2].total_points = 2400

        # first player after 3000 is hit
        player_with_turn = game.new_turn()
        self.assertEqual(2, game.active_player_index)
        self.assertEqual(game.players[2], player_with_turn)
        self.assertEqual(1, game._final_round_turns)
        game.players[2].turn_over = True

        # last roll for trailing player
        player_with_turn = game.new_turn()
        self.assertEqual(0, game.active_player_index)
        self.assertEqual(game.players[0], player_with_turn)
        self.assertEqual(2, game._final_round_turns)
        self.assertEqual(True, game._game_over)

    def test_new_turn_raises_error_when_game_over(self):
        game = Game()
        game.add_player('player 1')
        game.add_player('player 2')

        game.players[0].total_points = 2800
        game.players[1].total_points = 3000

        game._game_over = True

        with self.assertRaises(GameError):
            game.new_turn()

    def test_winner_set_when_game_over(self):
        game = Game()
        game.add_player('player 1')
        game.add_player('player 2')
        game.add_player('player 3')
        game.active_player_index = 1

        game.players[0].total_points = 2800
        game.players[1].total_points = 3000
        game.players[2].total_points = 2400

        self.assertEqual(False, game.players[0].is_winner)
        self.assertEqual(False, game.players[1].is_winner)
        self.assertEqual(False, game.players[2].is_winner)

        game._game_over = True
        winner_return = game.set_winner()

        self.assertEqual(False, game.players[0].is_winner)
        self.assertEqual(True, game.players[1].is_winner)
        self.assertEqual(False, game.players[2].is_winner)
        self.assertEqual('player 2 is the winner!', winner_return)

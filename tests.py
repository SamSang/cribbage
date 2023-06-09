"""
Tests for the cribbage module
"""
import logging
import unittest

import cribbage
import logger

logger.logger.setLevel(logging.ERROR)
logger.awarder.setLevel(logging.ERROR)
logger.hand.setLevel(logging.ERROR)


class TestStrategyHuman(unittest.TestCase):
    """Human strategy elements work as intended"""

    def setUp(self) -> None:
        return super().setUp()

    def test_validate_index(self):
        """indecies are available to select"""
        examples = [
            (["1", "2"], ["a", "b", "c"], True),
            ([0, 2], ["a", "b", "c"], True),
            ([1, 3], ["a", "b", "c"], False),
            ([-1], ["a", "b", "c"], False),
            (["x"], ["a", "b", "c"], False),
        ]
        for indices, values, result in examples:
            with self.subTest(indices=indices, values=values, result=result):
                self.assertEqual(cribbage.validate_index(indices, values), result)

    def test_exit(self):
        """
        type 'exit' raises KeyboardInterrupt
        even when index is invalid
        """
        with self.assertRaises(KeyboardInterrupt):
            cribbage.validate_index([0, "exit"], [])

    def test_convert_index(self):
        """convert list of strings to list of integers"""
        values = ["1", "2", "3", "4", "5"]
        result = [1, 2, 3, 4, 5]
        self.assertEqual(cribbage.convert_indices(values), result)
        self.assertEqual(cribbage.convert_indices(result), result)

    def test_input_split(self):
        """convert arbitrary sequences to lists of strings"""
        examples = [
            ("1 2", ["1", "2"]),
            ("1  2", ["1", "2"]),
            # ("1,2", ["1", "2"]),
            # ("1;2", ["1", "2"]),
        ]
        for value, result in examples:
            with self.subTest(value=value, result=result):
                self.assertEqual(cribbage.split_input(value), result)

    def test_input(self):
        """wrapper around picking cards"""

        def static_input(prommpt: str) -> None:
            return "2 5"

        hand_strings = ["KD", "QD", "1D", "9D", "AC", "3D"]
        player_hand = [cribbage.card_from_string(s) for s in hand_strings]
        hand, crib = cribbage.pick_input(static_input, logger.default_level)(
            player_hand, [], 2
        )
        result_crib_strings = ["1D", "3D"]
        restult_hand_strings = ["KD", "QD", "9D", "AC"]
        self.assertCountEqual([card.name for card in hand], restult_hand_strings)
        self.assertCountEqual([card.name for card in crib], result_crib_strings)
        self.assertEqual([card.name for card in player_hand], restult_hand_strings)

    def test_input_exit(self):
        """generic input raises end of game error"""

        def static_input(prommpt: str) -> None:
            return "exit"

        hand_strings = ["KD", "QD", "1D", "9D", "AC", "3D"]
        player_hand = [cribbage.card_from_string(s) for s in hand_strings]
        with self.assertRaises(cribbage.WinCondition):
            hand, crib = cribbage.pick_input(static_input, logger.default_level)(
                player_hand, [], 2
            )


class TestStrategySequence(unittest.TestCase):
    """Sequence Strategy works as intended"""

    def setUp(self) -> None:
        self.hand_strings = ["KD", "8C", "4H", "QS", "3C"]
        self.hand = [cribbage.card_from_string(s) for s in self.hand_strings]
        return super().setUp()

    def test_pick_sequence(self):
        self.hand, played = cribbage.pick_sequence(self.hand, [], 5)
        self.assertEqual(self.hand, [])  # hand is empty
        played_values = [card.name for card in played]
        self.assertEqual(
            self.hand_strings, played_values
        )  # all cards were played in sequence

    def test_play_sequence(self):
        card = cribbage.play_sequence(self.hand, [], [])
        self.assertEqual(card.name, self.hand_strings[0])

    def test_pegs_play(self):
        """Play first card at or below stack_max"""
        self.hand, card = cribbage.pegs(self.hand, [], [], stack_max=8)
        self.assertEqual(len(self.hand), 4)
        self.assertEqual("8C", card.name)

    def test_pegs_no_play(self):
        """Return None when no card can be played"""
        self.hand, card = cribbage.pegs(self.hand, [], [], stack_max=0)
        self.assertEqual(len(self.hand), 5)
        self.assertIsNone(card)


class TestCribbageScore(unittest.TestCase):
    """Test suite for possible hands"""

    def test_zero(self):
        hand = ["KD", "8C", "AH", "QS", "3C"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(0, cribbage.score(cards))

    def test_fifteen(self):
        hand = ["8H", "7H", "KS", "QH", "1H"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(2, cribbage.score(cards))

    def test_pair(self):
        hand = ["AH", "1D", "1H", "6H", "2C"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(2, cribbage.score(cards))

    def test_tripple(self):
        hand = ["1S", "1D", "1H", "6H", "2C"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(6, cribbage.score(cards))

    def test_quad(self):
        hand = ["1S", "1D", "1H", "6H", "1C"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(12, cribbage.score(cards))

    def test_run_3(self):
        hand = ["4S", "8D", "JH", "QH", "KC"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(3, cribbage.score(cards))

    def test_run_4(self):
        hand = ["7S", "1D", "JH", "QH", "KC"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(4, cribbage.score(cards))

    def test_run_5(self):
        hand = ["9S", "1D", "JH", "QH", "KC"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(5, cribbage.score(cards))

    def test_flush_4(self):
        hand = ["9S", "1S", "QS", "KS"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(4, cribbage.score(cards))

    def test_flush_5(self):
        hand = ["9S", "1S", "QS", "KS", "7S"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        cut = cards.pop(-1)
        self.assertEqual(5, cribbage.score(cards, cut))

    def test_his_knobs(self):
        hand = ["JC", "8C", "AH", "QS", "3C"]
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        cut = cards.pop(-1)
        self.assertEqual(1, cribbage.score(cards, cut))


class TestCribbagePegs(unittest.TestCase):
    def test_fifteen_2(self):
        """Two cards fifteen returns 2"""
        stack = [cribbage.card_from_string(s) for s in ["1S", "5D"]]
        self.assertEqual(cribbage.peg_fifteen(stack), 2)

    def test_fifteen_3(self):
        """Three cards fifteen returns 2"""
        stack = [cribbage.card_from_string(s) for s in ["7S", "7D", "AH"]]
        self.assertEqual(cribbage.peg_fifteen(stack), 2)

    def test_fifteen_0(self):
        """Two cards 16 returns 0"""
        stack = [cribbage.card_from_string(s) for s in ["8S", "8D"]]
        self.assertEqual(cribbage.peg_fifteen(stack), 0)

    def test_pairs_0(self):
        """Stacks of 0-4 non-matching cards"""
        stacks_strings = [
            ["7S"],
            ["7S", "AH"],
            ["7S", "7D", "AH"],
            ["8D", "9H", "3C", "2D"],
        ]
        for stack_string in stacks_strings:
            with self.subTest(stack_string=stack_string):
                hand = [cribbage.card_from_string(s) for s in stack_string]
                self.assertEqual(0, cribbage.peg_pairs(hand))

    def test_pairs(self):
        """Stacks of 0-4 matching cards"""
        stacks_strings = [
            (["7S"], 0),
            (["7S", "7H"], 2),
            (["7S", "7D", "7H"], 6),
            (["7S", "7D", "7H", "7C"], 12),
        ]
        for i in range(len(stacks_strings)):
            with self.subTest(i=i):
                hand = [cribbage.card_from_string(s) for s in stacks_strings[i][0]]
                self.assertEqual(stacks_strings[i][1], cribbage.peg_pairs(hand))

    def test_seq(self):
        """Stacks of sequences"""
        stacks_strings = [
            (["7S"], 0),
            (["7S", "8H"], 0),
            (["7S", "7D", "7H"], 0),
            (["6S", "7D", "8H"], 3),
            (["6S", "7D", "8H", "9C"], 4),
            (["6S", "8H", "7D", "9C"], 4),
        ]
        for i in range(len(stacks_strings)):
            with self.subTest(i=i):
                hand = [cribbage.card_from_string(s) for s in stacks_strings[i][0]]
                self.assertEqual(stacks_strings[i][1], cribbage.peg_seq(hand))

    def test_pegs_packs(self):
        """Produce expected lists"""
        stack = ["6S", "8H", "7D", "9C", "AH"]
        expected = [
            ["6S", "8H", "7D", "9C", "AH"],
            ["8H", "7D", "9C", "AH"],
            ["7D", "9C", "AH"],
            ["9C", "AH"],
        ]
        result = cribbage.pegs_packs(stack)
        self.assertEqual(expected, result)

    def test_score_pegs(self):
        """Counts pegs of various stacks"""
        stacks_strings = [
            (["7S"], 0),
            (["7S", "8H"], 2),
            (["7S", "7D", "7H"], 6),
            (["7S", "4D", "2H"], 0),
            (["6S", "8H", "7D"], 3),
            (["6S", "8H", "7D", "9C"], 4),
            (["7S", "8H", "6D", "9C"], 4),
            (["7S", "8H", "6D", "JC"], 1),
        ]
        for i in range(len(stacks_strings)):
            with self.subTest(i=i):
                hand = [cribbage.card_from_string(s) for s in stacks_strings[i][0]]
                self.assertEqual(stacks_strings[i][1], cribbage.score_pegs(hand))


class TestCribbagePlayer(unittest.TestCase):
    """Test suite for Player class"""

    def setUp(self) -> None:
        self.player = cribbage.Player()
        return super().setUp()

    def test_attrs(self):
        """Has all given attributes"""
        player = cribbage.Player()
        attributes = {
            "name": str,
            "score": int,
            "hand": list,
            "seen": list,
            "_seen": set,
            "strategy_hand": "function",
            "strategy_pegs": "function",
            "count_hand": list,
            "logging_level": int,
        }
        for key in attributes:
            val = getattr(player, key)
            if attributes[key] == "function":
                assert callable(val)
            else:
                self.assertIsInstance(val, attributes[key])

    def test_name(self):
        name = "Player 1"
        player = cribbage.Player(name=name)
        self.assertEqual(name, player.name)

    def test_score(self):
        score = 42
        player = cribbage.Player()
        player.score += score  # score initiates at zero
        self.assertEqual(score, player.score)

    def test_hand(self):
        deck = cribbage.build_deck()
        hand = cribbage.draw_hand(deck, 4)

        player = cribbage.Player()
        player.hand = hand
        self.assertEqual(player.hand, hand)
        # player should also have hand added to seen
        self.assertCountEqual(player.seen, hand)  # order differs

    def test_see(self):
        deck = cribbage.build_deck()
        seen = cribbage.draw_hand(deck, 1)

        player = cribbage.Player()
        player.see(seen[0])  # also tests that seen is instantiated blank
        self.assertEqual(player.seen, seen)

    def test_reshuffle(self):
        deck = cribbage.build_deck()
        seen = cribbage.draw_hand(deck, 1)
        hand = cribbage.draw_hand(deck, 1)

        player = cribbage.Player(hand=hand)
        player.see(seen[0])

        player.reshuffle()
        self.assertEqual(player.hand, hand)
        self.assertEqual(len(player.seen), 1)
        self.assertEqual(player.seen[0].name, hand[0].name)

    def test_toss(self):
        # hand_size + (crib_size // player_count) = 4 + (4 // [2, 3, 4])
        for n in range(5, 6):
            with self.subTest(n=n):
                deck = cribbage.build_deck()
                hand = cribbage.draw_hand(deck, n)

                player = cribbage.Player()
                player.hand = hand

                crib = player.toss()

                self.assertEqual(len(player.hand), 4)
                self.assertEqual(len(crib), n - 4)
                for card in crib:
                    self.assertIsInstance(card, cribbage.Card)

    def test_play(self):
        hand_size = 1

        deck = cribbage.build_deck()
        hand = cribbage.draw_hand(deck, hand_size)

        player = cribbage.Player()
        player.hand = hand

        stack = []
        stack.append(player.play(stack))

        self.assertEqual(len(stack), 1)
        self.assertEqual(len(player.hand), hand_size - 1)

    def test_logging_level(self):
        self.assertEqual(self.player.logging_level, logger.default_level)

    def test_human(self):
        player = cribbage.Player(
            strategy_hand=cribbage.pick_human, strategy_pegs=cribbage.play_human
        )
        self.assertEqual(player.logging_level, logger.console_level)


class TestCribbageHand(unittest.TestCase):
    """Test suite for Hand class"""

    def setUp(self) -> None:
        # add players to hand
        self.players = [
            cribbage.Player("Player 1"),
            cribbage.Player("Player 2"),
            cribbage.Player("Player 3"),
        ]
        self.hand = cribbage.Hand(self.players)

    def test_attrs(self):
        """Has all given attributes"""
        attributes = {
            "seq": int,
            "players": list,
            "deck": list,
            "crib": list,
            # "the_cut": None, # not instantiated on init
            "stack": list,
            "stack_total": int,
            "scores": list,
            "turn_number": int,
            "game_name": str,
        }
        for key in attributes:
            with self.subTest(key=key):
                val = getattr(self.hand, key)
                self.assertIsInstance(val, attributes[key])

    def test_seq(self):
        self.assertEqual(self.hand.seq, 0)

    def test_players(self):
        self.assertCountEqual(self.hand.players, self.players)

    def test_deck(self):
        """There are 52 cards including deck"""
        self.assertIsNone(self.hand.the_cut)
        self.assertEqual(len(self.hand.deck), 52)

    def test_show(self):
        """Show each player one card"""
        card = cribbage.card_from_string("8S")
        self.hand.show(card)
        for player in self.hand.players:
            self.assertIn(card, player.seen)

    def test_cut(self):
        """The cut starts empty, then one card is taken out to be the cut."""
        n = 11
        knobs = [cribbage.card_from_string("JH") for i in range(n)]
        self.assertIsNone(self.hand.the_cut)
        self.hand.deck = knobs
        self.hand.cut()
        self.assertIsInstance(self.hand.the_cut, cribbage.Card)
        self.assertEqual(len(self.hand.deck), n - 1)
        for player in self.hand.players:
            self.assertIn(self.hand.the_cut, player.seen)
        # two points awarded to last player
        self.assertEqual(self.hand.players[len(self.hand.players) - 1].score, 2)

    def test_count(self):
        """
        Correctly count hands and award points in the crib
        """
        crib_strings = ["2H", "AD"]
        crib = [cribbage.card_from_string(s) for s in crib_strings]
        player_1_strings = ["2D", "3H"]
        player_1_hand = [cribbage.card_from_string(s) for s in player_1_strings]
        player_2_strings = ["6S", "6C", "6D"]
        player_2_hand = [cribbage.card_from_string(s) for s in player_2_strings]
        player_3_strings = ["AS", "AC"]
        player_3_hand = [cribbage.card_from_string(s) for s in player_3_strings]

        self.hand.the_cut = cribbage.card_from_string("AH")
        self.hand.crib = crib
        self.hand.players[0].count_hand = player_1_hand
        self.hand.players[1].count_hand = player_2_hand
        self.hand.players[2].count_hand = player_3_hand

        self.hand.count()

        # results with cut
        result = [3, 6, 8]

        for i in range(0, 3):
            with self.subTest(i=i):
                self.assertEqual(self.hand.players[i].score, result[i])

    def test_deal(self):
        """
        All hands have original number of cards
        4 + (4 // n)
        """
        for n in range(2, 5):
            with self.subTest(n=n):
                hand_size = 4 + (4 // n)
                players = []
                for i in range(n):
                    players.append(cribbage.Player(f"Player {i + 1}"))
                local_hand = cribbage.Hand(players=players)
                local_hand.deal()
                for player in local_hand.players:
                    self.assertEqual(len(player.hand), hand_size)

    def test_collect(self):
        """After collecting crib, all hands and the crib have 4 cards"""
        for n in range(2, 5):
            with self.subTest(n=n):
                players = []
                for i in range(1, n):
                    players.append(cribbage.Player(f"Player {i}"))
                local_hand = cribbage.Hand(players=players)
                local_hand.deal()
                local_hand.collect()
                for player in local_hand.players:
                    self.assertEqual(len(player.hand), 4)  # each player has 4 cards
                self.assertEqual(len(local_hand.crib), 4)  # the crib has 4 cards
                self.assertEqual(
                    len(local_hand.deck), 52 - (len(local_hand.players) + 1) * 4
                )  # the rest of the cards are in the deck

    def test_award(self):
        player = self.hand.players[0]
        self.hand.award(player, 1, "testing")
        self.assertEqual(self.hand.players[0].score, 1)

    def test_award_win(self):
        """Default win score raises win exception"""
        player = self.hand.players[0]
        with self.assertRaises(cribbage.WinCondition):
            self.hand.award(player, 121, "testing")

    def test_turn(self):
        """Player puts a card on the stack"""
        # build players' hands
        hand_strings = [
            ["KD", "QD", "1D", "9D"],
            ["JH", "1S", "2H", "3S"],
        ]
        players = []
        for i, hand_string in enumerate(hand_strings):
            player_hand = [cribbage.card_from_string(s) for s in hand_string]
            player = cribbage.Player(name=f"Player {i + 1}", hand=player_hand)
            players.append(player)
        # build a hand using these players
        local_hand = cribbage.Hand(players=players)
        local_hand.turn(0)
        self.assertEqual(
            str(local_hand.stack), "[KD]"
        )  # the first player plays their first card

    def test_turn_go(self):
        """Player is awarded a point for the go"""
        # build players' hands
        hand_strings = [
            ["KD", "QD", "1D", "9D"],
            ["JH", "1S", "2H", "3S"],
        ]
        players = []
        for i, hand_string in enumerate(hand_strings):
            player_hand = [cribbage.card_from_string(s) for s in hand_string]
            player = cribbage.Player(name=f"Player {i + 1}", hand=player_hand)
            players.append(player)
        # build a hand using these players
        local_hand = cribbage.Hand(players=players)
        local_hand.go = 1  # one player has already said go
        stack = [cribbage.card_from_string(s) for s in ["JD", "1S", "KC"]]
        local_hand.stack = stack
        i = 0
        local_hand.turn(i)
        self.assertEqual(local_hand.stack, stack)  # no card was played
        self.assertEqual(
            local_hand.players[i].score, 1
        )  # but the player was awarded one point

    def test_turn_no_play(self):
        """Player is awarded a point for the go"""
        # build players' hands
        hand_strings = [
            ["KD", "QD", "1D", "9D"],
            ["JH", "1S", "2H", "3S"],
        ]
        players = []
        for i, hand_string in enumerate(hand_strings):
            player_hand = [cribbage.card_from_string(s) for s in hand_string]
            player = cribbage.Player(name=f"Player {i + 1}", hand=player_hand)
            players.append(player)
        # build a hand using these players
        local_hand = cribbage.Hand(players=players)
        stack = [cribbage.card_from_string(s) for s in ["JD", "1S", "KC"]]
        local_hand.stack = stack
        i = 0
        local_hand.turn(i)
        self.assertEqual(local_hand.stack, stack)  # no card was played
        self.assertEqual(local_hand.players[i].score, 0)  # No points awarded

    def test_count(self):
        """Points in hands and the crib are awarded for two players"""
        # Note that testing 3 players would involve a random card
        # set the hands for each player
        hand_strings = [
            ["KD", "QD", "1D", "9D", "4S", "AD"],
            ["JH", "1S", "2H", "3S", "4D", "6H"],
        ]
        players = []
        for i, hand_string in enumerate(hand_strings):
            player_hand = [cribbage.card_from_string(s) for s in hand_string]
            player = cribbage.Player(name=f"Player {i + 1}", hand=player_hand)
            players.append(player)

        # build a hand using these players
        local_hand = cribbage.Hand(players=players)
        local_hand.the_cut = cribbage.card_from_string("5S")
        local_hand.collect()
        local_hand.count()

        # validate the resulting scores
        # last player to count gets the crib
        scores = [6, 9 + 12]
        for i in range(len(local_hand.players)):
            with self.subTest(i=i):
                self.assertEqual(local_hand.players[i].score, scores[i])

    def test_trick_go_1(self):
        """Cards get played on the stack
        One player plays three cards on the stack and is awarded one point for the go.
        """
        hand_strings = ["KD", "QD", "1D", "9D"]
        player_hand = [cribbage.card_from_string(s) for s in hand_strings]
        players = [cribbage.Player(hand=player_hand)]
        hand = cribbage.Hand(players=players)
        hand.trick()
        stack_strings = [card.name for card in hand.stack]
        self.assertEqual(
            stack_strings, hand_strings[0:3]
        )  # stack has just first three cards
        end_hand_strings = [card.name for card in hand.players[0].hand]
        self.assertEqual(
            end_hand_strings, [hand_strings[3]]
        )  # hand has only one card remaining
        self.assertEqual(
            hand.players[0].score, 1
        )  # player was awarded one point for the go

    def test_trick_go_2(self):
        """Player is awarded 2 points for exactly 31"""
        hand_strings = ["KD", "QD", "1D", "AS"]
        player_hand = [cribbage.card_from_string(s) for s in hand_strings]
        players = [cribbage.Player(hand=player_hand)]
        hand = cribbage.Hand(players=players)
        hand.trick()
        self.assertEqual(
            hand.players[0].score, 2
        )  # player was awarded two points for the go + 31

    def test_trick_2(self):
        """Two players put down cards in sequence"""
        # build two players' hands
        hand_strings = [
            ["JD", "6D", "1D", "AS"],
            ["5S", "QD", "6D", "2S"],
        ]
        players = []
        for hand_string in hand_strings:
            player = cribbage.Player(
                hand=[cribbage.card_from_string(s) for s in hand_string]
            )
            players.append(player)
        hand = cribbage.Hand(players)
        # play a trick with both players
        hand.trick()
        # assess the order is what is expected
        stack_strings = [card.name for card in hand.stack]
        expected_strings = ["5S", "JD", "QD", "6D"]
        self.assertEqual(stack_strings, expected_strings)

    def test_trick_2x(self):
        """Second hand between two players is in sequence"""
        # build two players' hands
        hand_strings = [
            ["JD", "6D", "1D", "AS"],
            ["5S", "QD", "6D", "2S"],
        ]
        players = []
        for hand_string in hand_strings:
            player = cribbage.Player(
                hand=[cribbage.card_from_string(s) for s in hand_string]
            )
            players.append(player)
        hand = cribbage.Hand(players)
        # play a trick with both players
        hand.trick()
        # reset the stack and play the second trick
        hand.stack = []
        hand.trick()
        # assess the order is what is expected
        stack_strings = [card.name for card in hand.stack]
        expected_strings = ["6D", "1D", "2S", "AS"]
        self.assertEqual(stack_strings, expected_strings)

    def test_tricks(self):
        """Test that all tricks get played out"""
        # build two players' hands
        hand_strings = [
            ["JD", "6D", "1D", "AS"],
            ["5S", "QD", "6D", "2S"],
        ]
        players = []
        for hand_string in hand_strings:
            player = cribbage.Player(
                hand=[cribbage.card_from_string(s) for s in hand_string]
            )
            players.append(player)
        hand = cribbage.Hand(players)
        # play out both trick with both players
        hand.tricks()
        # assess the order is what is expected
        stack_strings = [card.name for card in hand.stack]
        expected_strings = ["6D", "1D", "2S", "AS"]
        self.assertEqual(stack_strings, expected_strings)


class TestCribbageGame(unittest.TestCase):
    def setUp(self) -> None:
        self.n = 4
        self.game = cribbage.Game(n=self.n)
        return super().setUp()

    def test_attrs(self):
        """Has all given attributes"""
        attributes = {
            "name": str,
            "players": list,
            "n": int,
            "deck": list,
            "dealer_index": int,
            "win": int,
            "results": dict,
        }
        for key in attributes:
            val = getattr(self.game, key)
            self.assertIsInstance(val, attributes[key])

    def test_no_players(self):
        configs = [
            {"n": 0},
            {"players": []},
        ]
        for params in configs:
            with self.subTest(params=params):
                with self.assertRaises(ValueError):
                    game = cribbage.Game(**params)

    def test_n_players(self):
        self.assertEqual(self.game.n, self.n)
        players = [
            cribbage.Player("1"),
            cribbage.Player("2"),
        ]
        game = cribbage.Game(players=players)
        self.assertEqual(game.n, len(players))

    def test_shuffle(self):
        """Deck is replentished"""
        self.game.shuffle()
        self.assertEqual(len(self.game.deck), 52)

    @unittest.SkipTest
    def test_skunk(self):
        """Check if any player got skunked"""
        pass

    def test_advance(self):
        """Validate how the deal is passed to next player"""
        self.game.advance()
        player_names = [player.name for player in self.game.players]
        self.assertEqual(player_names, ["4", "1", "2", "3"])

    def test_play(self):
        """Play a sequence of hands with the set of players"""
        self.game.play()
        self.assertIsInstance(self.game.results, dict)
        self.assertIsNotNone(self.game.results)


if __name__ == "__main__":
    unittest.main()

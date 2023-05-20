"""
Tests for the cribbage module
"""
import typing
import unittest

import cribbage

class TestCribbageScore(unittest.TestCase):
    '''Test suite for possible hands'''

    def test_zero(self):
        hand = ['KD', '8C', 'AH', 'QS', '3C']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(0, cribbage.score(cards))

    def test_fifteen(self):
        hand = ['8H', '7H', 'KS', 'QH', '1H']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(2, cribbage.score(cards))

    def test_pair(self):
        hand = ['AH', '1D', '1H', '6H', '2C']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(2, cribbage.score(cards))

    def test_tripple(self):
        hand = ['1S', '1D', '1H', '6H', '2C']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(6, cribbage.score(cards))

    def test_quad(self):
        hand = ['1S', '1D', '1H', '6H', '1C']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(12, cribbage.score(cards))
    
    def test_run_3(self):
        hand = ['4S', '8D', 'JH', 'QH', 'KC']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(3, cribbage.score(cards))
    
    def test_run_4(self):
        hand = ['7S', '1D', 'JH', 'QH', 'KC']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(4, cribbage.score(cards))
    
    def test_run_5(self):
        hand = ['9S', '1D', 'JH', 'QH', 'KC']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(5, cribbage.score(cards))
    
    def test_flush_4(self):
        hand = ['9S', '1S', 'QS', 'KS']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        self.assertEqual(4, cribbage.score(cards))
    
    def test_flush_5(self):
        hand = ['9S', '1S', 'QS', 'KS', '7S']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        cut = cards.pop(-1)
        self.assertEqual(5, cribbage.score(cards, cut))

    def test_his_knobs(self):
        hand = ['JC', '8C', 'AH', 'QS', '3C']
        cards = []
        for card in hand:
            cards.append(cribbage.card_from_string(card))
        cut = cards.pop(-1)
        self.assertEqual(1, cribbage.score(cards, cut))

class TestCribbagePlayer(unittest.TestCase):
    """Test suite for Player class"""

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
        player.score += score # score initiates at zero
        self.assertEqual(score, player.score)

    def test_hand(self):
        deck = cribbage.build_deck()
        hand = cribbage.draw_hand(deck, 4)

        player = cribbage.Player()
        player.hand = hand
        self.assertEqual(player.hand, hand)
        # player should also have hand added to seen
        self.assertCountEqual(player.seen, hand) # order differs

    def test_see(self):
        deck = cribbage.build_deck()
        seen = cribbage.draw_hand(deck, 1)

        player = cribbage.Player()
        player.see(seen[0]) # also tests that seen is instantiated blank
        self.assertEqual(player.seen, seen)

    def test_reshuffle(self):
        deck = cribbage.build_deck()
        seen = cribbage.draw_hand(deck, 1)

        player = cribbage.Player()
        player.see(seen[0])

        player.reshuffle()
        self.assertEqual(player.hand, [])
        self.assertEqual(len(player.seen), 0)

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

        self.assertEqual(len(stack) , 1)
        self.assertEqual(len(player.hand) , hand_size - 1)

class TestCribbageHand(unittest.TestCase):
    """Test suite for Hand class"""

    def setUp(self) -> None:
        # add players to hand
        self.deck = cribbage.build_deck()
        self.players = [
            cribbage.Player("Player 1"),
            cribbage.Player("Player 2"),
            cribbage.Player("Player 3"),
        ]
        self.hand = cribbage.Hand(self.players, self.deck)

    def test_attrs(self):
        """Has all given attributes"""
        # Maybe instantiate the Hand
        attributes = {
            "seq": int,
            "players": list,
            "deck": list,
            "crib": list,
            "the_cut": cribbage.Card,
            "stack": list,
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
        # there are 52 cards including deck, crib and hands
        self.assertEqual(len([self.hand.the_cut]), 1)

    def test_cut(self):
        self.assertIsInstance(self.hand.the_cut, cribbage.Card)

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

        # clear out the cut for ease
        #self.hand.the_cut = cribbage.card_from_string("AH")
        self.hand.the_cut = None # TODO Implement counting the cut
        self.hand.crib = crib
        self.hand.players[0].count_hand = player_1_hand
        self.hand.players[1].count_hand = player_2_hand
        self.hand.players[2].count_hand = player_3_hand

        self.hand.count()

        # results with cut
        #result = [3, 6, 8]

        # results without cut
        result = [0, 6, 2]

        for i in range(0, 3):
            with self.subTest(i=i):
                self.assertEqual(self.hand.players[i].score, result[i])

    def test_deal(self):
        """
        All hands have four cards
        """
        for n in range(2, 5):
            with self.subTest(n=n):
                local_deck = cribbage.build_deck()
                players = []
                for i in range(1, n):
                    players.append(cribbage.Player(f"Player {i}"))
                local_hand = cribbage.Hand(players, local_deck)
                for player in local_hand.players:
                    self.assertEqual(len(player.hand), 4)

        in_hand = 0
        for player in self.hand.players:
            self.assertEqual(len(player.hand), 4)
            in_hand += 4

        self.assertEqual(len(self.hand.crib), 4)

        in_play = 1 + in_hand + 4
        self.assertEqual(len(self.hand.deck) + in_play, 52)

    @unittest.SkipTest
    def test_play(self):
        pass

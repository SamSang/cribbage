"""
Tests for the cribbage module
"""
import unittest

import cribbage

class TestCribbagecribbageScore(unittest.TestCase):
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
        hand = ['9S', '1S', 'QS', 'KS', '6S']
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
"""
Collection of objects to represent possible cribbage hands
"""

import random
from itertools import combinations
from itertools import permutations
import unittest

faces = {
        '10': {
            'seq': 1,
            'value': 1,
            'letter': '1',
        },
        'Jack': {
            'seq': 11,
            'value': 10,
            'letter': 'J',
        },
        'Queen': {
            'seq': 12,
            'value': 10,
            'letter': 'Q',
        },
        'King': {
            'seq': 13,
            'value': 10,
            'letter': 'K',
        },
        'Ace': {
            'seq': 1,
            'value': 1,
            'letter': 'A',
        },
    }

suits = {
    'Spade': {
        'letter': 'S',
    },
    'Heart': {
        'letter': 'H',
    },
    'Diamond': {
        'letter': 'D',
    },
    'Club': {
        'letter': 'C',
    },
}

class Card:
    def __init__(self, rank: str, suit: str, seq: int, value: int):
        self.rank = rank
        self.suit = suit
        self.seq = seq
        self.value = value
        self.name = self.rank[0] + self.suit[0]
    def __repr__(self):
        return self.name

def build_deck() -> list:
    """
    Build a deck of standard playing cards
    Return a list of the 52 class objects
    """
    deck = list()

    suits = ['Spade', 'Heart', 'Diamond', 'Club']

    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

    for suit in suits:
        for rank in ranks:
            card = build_card(rank, suit)
            deck.append(card)
    return deck

def build_card(rank: str, suit: str) -> Card:
    """Make a card from the rank and suit"""
    try:
        seq = int(rank)
        value = int(rank)
    except ValueError:
        seq = faces[rank]['seq']
        value = faces[rank]['value']
    return Card(rank, suit, seq, value)

def build_letter_function(letter):
    def get_letter(pair) -> bool:
        """function to filter a dict by the child key `letter`"""
        key, value = pair
        try:
            if value['letter'] == letter:
                return True
        except:
            return False
    return get_letter

def card_from_string(card_string) -> Card:
    """Make a card given the two letter abbreviation"""
    rank_letter = card_string[0]
    suit_letter = card_string[1]
    rank_filter_function = build_letter_function(rank_letter)
    suit_filter_function = build_letter_function(suit_letter)
    suit_dict = dict(filter(suit_filter_function, suits.items()))
    suit = list(suit_dict.keys())[0]
    try:
        rank_dict = dict(filter(rank_filter_function, faces.items()))
        rank = list(rank_dict.keys())[0]
    except:
        rank = rank_letter
    return build_card(rank, suit)

def build_hand() -> list:
    """Build a list of card objects given user input"""
    cards_text = input('Enter cards: ')
    cards_split = cards_text.split(' ')
    cards = list()
    for card in cards_split:
        cards.append(card_from_string(card))
    return cards
# TODO build a logger for scoring a hand

def draw_hand(deck: list, n=5) -> list:
    """Choose n random cards from the deck"""
    hand = list()
    i = 0
    while i < n:
        hand.append(deck.pop())
        i += 1
    return hand

def add_cards(cards: list) -> int:
    """
    return sum of values of passed cards
    """
    values = list()
    for card in cards:
        values.append(card.value)
    return sum(values)

def seq_card(card: Card):
    return card.seq

def consecutive_cards(cards: list) -> bool:
    """returns true if all cards in the list are consecutive"""
    is_consecutive = False
    sequence = [card.seq for card in cards]
    lowest_card = min(sequence)
    correct_sequence = range(lowest_card, lowest_card + len(cards))
    if list(sequence) == list(correct_sequence):
        is_consecutive = True
    return is_consecutive

def check_fifteen(cards) -> int:
    points = 0
    if add_cards(cards) == 15:
        print('15 two!')
        print(cards)
        points = 2
    return points

def check_pair(cards) -> int:
    points = 0
    if len(cards) == 2 and cards[0].rank == cards[1].rank:
        print('A pair in there!')
        print(cards)
        points = 2
    return points

def score(hand, cut: Card = None) -> None:
    """
    Count a cribbage hand
    TODO
        logger
        separate each of the subset analyzers to their own function
    """
    score = 0
    sequences = list()
    for cards in range(len(hand) + 1):
        for subset in combinations(hand, cards):
            # two points for any combination of cards whose sum is 15
            score += check_fifteen(subset)
            # two points for each matching card
            score += check_pair(subset)
        # get all consecutive sets
        for subset in permutations(hand, cards):
            # one point for each unique set of sequential cards
            run = list(subset)
            if len(subset) >= 3 and consecutive_cards(run):
                sequences.append(run)
    # reconcile overlapping sets
    unique_sequences = list()
    for sequence in sequences:
        unique = True
        for i in range(len(unique_sequences)):
            #print('compare', sequence, 'to', unique_sequences[i])
            if set(sequence).issuperset(unique_sequences[i]): # run is inside this sequence
                # add the difference between the two to the existing sequence
                #print('add', set(sequence), 'to', unique_sequences[i])
                values_to_add = list(set(sequence).difference(unique_sequences[i]))
                for value_to_add in values_to_add:
                    unique_sequences[i].add(value_to_add)
            if not unique_sequences[i].issubset(set(sequence)):
                unique = False
        if unique:
            #print('add sequence', set(sequence))
            unique_sequences.append(set(sequence))
    # tally points from sequential sets
    unique_sequences_set = set(frozenset(s) for s in unique_sequences)
    for unique_sequence in unique_sequences_set:
        points = len(unique_sequence)
        print(list(unique_sequence), 'for', points, 'points')
        score += points
    # check for a flush
    suits = list()
    for i in range(len(hand)):
        suits.append(hand[i].suit)
    if len(list(set(suits))) == 1:
        print('Flush!')
        score += len(hand)
        # check if we get an extra point for the cut matching the flush
        if cut:
            if cut.suit == suits[0]:
                print('(including the cut)')
                score += 1
    # check if the hand has a jack matching the suit of the card in the cut
    if cut:
        for card in hand:
            if card.rank == 'Jack' and card.suit == cut.suit:
                print('Jack in the suit!')
                score += 1
    return score

class TestCribbageScore(unittest.TestCase):
    '''Test suite for possible hands'''

    def test_zero(self):
        hand = ['KD', '8C', 'AH', 'QS', '3C']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(0, score(cards))

    def test_fifteen(self):
        hand = ['8H', '7H', 'KS', 'QH', '1H']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(2, score(cards))

    def test_pair(self):
        hand = ['AH', '1D', '1H', '6H', '2C']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(2, score(cards))

    def test_tripple(self):
        hand = ['1S', '1D', '1H', '6H', '2C']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(6, score(cards))

    def test_quad(self):
        hand = ['1S', '1D', '1H', '6H', '1C']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(12, score(cards))
    
    def test_run_3(self):
        hand = ['4S', '8D', 'JH', 'QH', 'KC']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(3, score(cards))
    
    def test_run_4(self):
        hand = ['7S', '1D', 'JH', 'QH', 'KC']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(4, score(cards))
    
    def test_run_5(self):
        hand = ['9S', '1D', 'JH', 'QH', 'KC']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(5, score(cards))
    
    def test_flush_4(self):
        hand = ['9S', '1S', 'QS', 'KS']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        self.assertEqual(4, score(cards))
    
    def test_flush_5(self):
        hand = ['9S', '1S', 'QS', 'KS', '6S']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        cut = cards.pop(-1)
        self.assertEqual(5, score(cards, cut))

    def test_his_knobs(self):
        hand = ['JC', '8C', 'AH', 'QS', '3C']
        cards = []
        for card in hand:
            cards.append(card_from_string(card))
        cut = cards.pop(-1)
        self.assertEqual(1, score(cards, cut))

def main():
    deck = build_deck()
    random.shuffle(deck)
    hand = draw_hand(deck)
    print(hand)
    points = score(hand)
    print(points)

if __name__ == '__main__':
    main()

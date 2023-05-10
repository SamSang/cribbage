"""
Collection of objects to represent possible cribbage hands
"""

import random
from itertools import combinations
from itertools import permutations
from logger import logger
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

def score_fifteen(cards) -> int:
    """
    Score when a set of cards = 15
    """
    points = 0
    for count_cards in range(len(cards) + 1):
        for subset in combinations(cards, count_cards):
            if add_cards(subset) == 15:
                logger.info(f'15 two! {subset}')
                points += 2
    return points

def score_pair(cards) -> int:
    """
    Score when a pair of cards has the same rank
    """
    points = 0
    for subset in combinations(cards, 2):
        if len(subset) == 2 and subset[0].rank == subset[1].rank:
            logger.info(f'A pair in there! {subset}')
            points += 2
    return points

def score_seq(cards) -> int:
    """
    Score when a the ranks of cards in a set are in sequence
    """
    points = 0
    sequences = []
    for count_cards in range(len(cards) + 1):
        for subset in permutations(cards, count_cards):
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
        points += len(unique_sequence)
        logger.info(f"{list(unique_sequence)} for {points} points")
    return points

def score_flush(hand: list, cut: Card) -> int:
    # check for a flush
    points = 0
    suits = list()
    for i in range(len(hand)):
        suits.append(hand[i].suit)
    if len(list(set(suits))) == 1:
        logger.info('Flush!')
        points += len(hand)
        # check if we get an extra point for the cut matching the flush
        if cut:
            if cut.suit == suits[0]:
                logger.info('(including the cut)')
                points += 1
    return points

def score_cut(hand: list, cut: Card) -> int:
    # check if the hand has a jack matching the suit of the card in the cut
    if cut:
        for card in hand:
            if card.rank == 'Jack' and card.suit == cut.suit:
                logger.info('Jack in the suit!')
                return 1
    return 0

def score(hand: list, cut: Card = None) -> None:
    """
    Count a cribbage hand
    """
    score = 0
    full_hand = hand
    if cut:
        full_hand = hand + [cut]
    score += score_fifteen(full_hand)
    score += score_pair(full_hand)
    score += score_seq(full_hand)
    score += score_flush(hand, cut)
    score += score_cut(hand, cut)
    return score

class TestCribbageScore(unittest.TestCase):
    '''Test suite for possible hands'''

    def setUp(self):
        self.configs = [
            {
                'name': 'zero',
                'hand': ['KD', '8C', 'AH', 'QS', '3C'],
                'score': 0,
            },
            {
                'name': 'one fifteen',
                'hand': ['8H', '7H', 'KS', 'QH', '1H'],
                'score': 2,
            },
            {
                'name': 'one pair',
                'hand': ['AH', '1D', '1H', '6H', '2C'],
                'score': 2,
            },
            {
                'name': 'three of a kind',
                'hand': ['1S', '1D', '1H', '6H', '2C'],
                'score': 6,
            },
            {
                'name': 'four of a kind',
                'hand': ['1S', '1D', '1H', '6H', '1C'],
                'score': 12,
            },
            {
                'name': 'run of three',
                'hand': ['4S', '8D', 'JH', 'QH', 'KC'],
                'score': 3,
            },
            {
                'name': 'run of four',
                'hand': ['7S', '1D', 'JH', 'QH', 'KC'],
                'score': 4,
            },
            {
                'name': 'run of five',
                'hand': ['9S', '1D', 'JH', 'QH', 'KC'],
                'score': 5,
            },
            {
                'name': 'flush of four',
                'hand': ['9S', '1S', 'QS', 'KS', '7D'],
                'score': 4,
            },
            {
                'name': 'flush of five',
                'hand': ['9S', '1S', 'QS', 'KS', '2S'],
                'score': 5,
            },
            {
                'name': 'only his knobs',
                'hand': ['JC', '8C', 'AH', 'QS', '3C'],
                'score': 1,
            },
        ]

    def test_hands(self):
        for config in self.configs:
            with self.subTest(config['name'], config=config):
                hand = config['hand']
                expected_score = config['score']
                cards = []
                for card in hand:
                    cards.append(card_from_string(card))
                cut = cards.pop(-1)
                self.assertEqual(expected_score, score(cards, cut))

def main():
    deck = build_deck()
    random.shuffle(deck)
    hand = draw_hand(deck)
    points = score(hand)
    logger.info(points)

if __name__ == '__main__':
    main()

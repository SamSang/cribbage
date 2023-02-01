"""
Collection of objects to represent possible cribbage hands
"""

import random
from itertools import combinations
from itertools import permutations

class Card:
    def __init__(self, card: str, suit: str, seq: int, value: int):
        self.card = card
        self.suit = suit
        self.seq = seq
        self.value = value
        self.name = self.card[0] + self.suit[0]
    def __repr__(self):
        return self.name

def build_deck() -> list:
    """
    Build a deck of standard playing cards
    Return a list of the 52 class objects
    """
    deck = list()

    suits = ['Spade', 'Heart', 'Diamond', 'Club']

    cards = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

    rules = {
        'Jack': {
            'seq': 11,
            'value': 10,
        },
        'Queen': {
            'seq': 12,
            'value': 10,
        },
        'King': {
            'seq': 13,
            'value': 10,
        },
        'Ace': {
            'seq': 1,
            'value': 1,
        }
    }
    for suit in suits:
        for card in cards:
            try:
                seq = int(card)
                value = int(card)
            except ValueError:
                seq = rules[card]['seq']
                value = rules[card]['value']
            deck.append(Card(card, suit, seq, value))
    return deck

# TODO a helper function to quickly build a hand (for testing)
def build_card(card_str: str) -> Card:
    """Make a card object using a two-letter text"""
    faces = {
        'A': {
            'card': 'Ace',
            'seq': 1,
            'value': 1
        },
        '1': {
            'card': '10',
            'seq': 10,
            'value': 10
        },
        'J': {
            'card': 'Jack',
            'seq': 11,
            'value': 10
        },
        'Q': {
            'card': 'Queen',
            'seq': 12,
            'value': 10
        },
        'K': {
            'card': 'King',
            'seq': 13,
            'value': 10
        },
    }
    suits = {
        'S': 'Spade',
        'H': 'Heart',
        'D': 'Diamond',
        'C': 'Club'
    }
    card_letter = card_str[0]
    card_suit = card_str[1]
    suit = suits[card_suit]
    if card_letter in faces:
        card = faces[card_letter]['card']
        seq = faces[card_letter]['seq']
        value = faces[card_letter]['value']
    else:
        card = str(card_letter)
        seq = int(card_letter)
        value = int(card_letter)
    return Card(card, suit, seq, value)

def build_hand() -> list:
    """Build a list of card objects given user input"""
    cards_text = input('Enter cards: ')
    cards_split = cards_text.split(' ')
    cards = list()
    for card in cards_split:
        cards.append(build_card(card))
    return cards
# TODO organize some test hands (for flush, 4 of a kind, weird runs)
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

def score(hand, cut: Card = None) -> None:
    """
    Count a cribbage hand
    TODO
        runs - fix broken issue
        flush - build a test
        jack in suit, his knobs
        logger
        separate each of the subset analyzers to their own function
    """
    score = 0
    sequences = list()
    for cards in range(len(hand) + 1):
        for subset in combinations(hand, cards):
            # two points for any combination of cards whose sum is 15
            if add_cards(subset) == 15:
                print('15 two!')
                score += 2
                print(subset)
            # two points for each matching card
            if len(subset) == 2:
                if subset[0].card == subset[1].card:
                    print('A pair in there!')
                    score += 2
                    print(subset)
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
            if card.card == 'Jack' and card.suit == cut.suit:
                print('Jack in the suit!')
                score += 1
    return score


def main():
    deck = build_deck()
    random.shuffle(deck)
    hand = draw_hand(deck)
    print(hand)
    points = score(hand)
    print(points)

if __name__ == '__main__':
    main()

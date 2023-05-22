"""
Collection of objects to represent possible cribbage hands
"""

import random
import typing
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
                logger.debug(f'15 two! {subset}')
                points += 2
    return points

def score_pair(cards) -> int:
    """
    Score when a pair of cards has the same rank
    """
    points = 0
    for subset in combinations(cards, 2):
        if len(subset) == 2 and subset[0].rank == subset[1].rank:
            logger.debug(f'A pair in there! {subset}')
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
        logger.debug(f"{list(unique_sequence)} for {points} points")
    return points

def score_flush(hand: list, cut: Card) -> int:
    # check for a flush
    points = 0
    suits = list()
    for i in range(len(hand)):
        suits.append(hand[i].suit)
    if len(list(set(suits))) == 1:
        logger.debug('Flush!')
        points += len(hand)
        # check if we get an extra point for the cut matching the flush
        if cut:
            if cut.suit == suits[0]:
                logger.debug('(including the cut)')
                points += 1
    return points

def score_cut(hand: list, cut: Card) -> int:
    # check if the hand has a jack matching the suit of the card in the cut
    if cut:
        for card in hand:
            if card.rank == 'Jack' and card.suit == cut.suit:
                logger.debug('Jack in the suit!')
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

def determine_possible(
        hand: typing.List[Card],
        stack: typing.List[Card],
        maximum: int = 31
    ) -> typing.List[Card]:
    """
    Determine which cards in hand are possible to play
    """
    possible = []
    total = 0
    for card in stack:
        total += card.value
    diff = maximum - total
    for card in hand:
        if card.value <= diff:
            possible.append(card)
    return possible

def strategy_random(
        hand: typing.List[Card],
        seen: typing.List[Card],
        stack: typing.List[Card] = None,
        n = 1
    ):
    """
    Randomly choose a card to play
    """
    possible = []
    if stack:
        possible = determine_possible(hand, stack)
    else:
        possible = hand
    # choose n random cards from the possible selections
    random.shuffle(possible)
    chosen = []
    for i in range(n):
        chosen.append(possible.pop(len(possible) - 1 - i))

    return hand, chosen

def strategy_sequence(
        hand: typing.List[Card],
        seen: typing.List[Card],
        stack: typing.List[Card] = None,
        n = 1
    ):
    """
    Choose the next card in the sequence to play
    """
    possible = []
    if stack:
        possible = determine_possible(hand, stack)
    else:
        possible = hand
    # choose The next card to play
    chosen = []
    for i in range(n):
        chosen.append(possible.pop(0))

    return hand, chosen

class Player(object):
    def __init__(self, name = "Player 0", strategy_hand = strategy_random, strategy_pegs = strategy_random) -> None:
        self.name = name
        self.score = 0
        self._hand: typing.List[Card] = []
        self._seen = set()
        self.strategy_hand = strategy_hand
        self.strategy_pegs = strategy_pegs

        self.count_hand: typing.List[Card] = []

    def see(self, card: Card) -> None:
        """
        Add card to list of cards player has seen
        """
        self._seen.add(card)

    @property
    def hand(self):
        return self._hand
    
    @hand.setter
    def hand(self, value):
        self._hand = value
        for card in self._hand:
            self.see(card)

    @property
    def seen(self):
        return list(self._seen)

    def reshuffle(self):
        """
        Clear memory of cards seen
        """
        self._seen = set()
        for card in self._hand:
            if isinstance(card, Card):
                self.see(card)

    def toss(self):
        """
        Hold on to four cards, put the rest in the crib
        """
        crib = []
        n = len(self.hand) - 4
        self.hand, crib = self.strategy_hand(hand=self.hand, seen=self.seen, n=n)
        return crib

    def play(self, stack):
        """
        Add a card to the stack
        """
        self.hand, selection = self.strategy_pegs(self.hand, self.seen, stack)
        return selection[0]

class WinCondition(Exception):
    """Raised when a player has won"""
    # Using this exception to halt the program whenever a player wins
    def __init__(self, players: typing.List[Player], *args: object) -> None:
        super().__init__(*args)
        self.players = players

class Hand(object):
    """
    Playing out one hand of cribbage
    """
    def __init__(self, players: typing.List[Player], deck: typing.List[Card], seq = 0, win = 121) -> None:
        self.players = players
        self.deck = deck
        self.seq = seq
        self.win = win
        self.the_cut: Card = None
        self.deal()
        self.crib: typing.List[Card] = self.collect()
        self.stack: typing.List[Card] = []

    def cut(self) -> Card:
        """
        Select a cut for the cut
        """
        # Cut must not be in the top 5 or bottom five cards
        i = random.randint(5, len(self.deck) - (1 + 5))
        return self.deck.pop(i)

    def deal(self) -> None:
        """
        Deal cards to each player
        """
        hand_size = 4 + (4 // len(self.players))
        for i in range(0, hand_size):
            for player in self.players:
                player.hand += [self.deck.pop()]
        for player in self.players:
            player.count_hand = player.hand
        self.the_cut = self.cut()
        if self.the_cut.rank == "J":
            self.award(self.players[len(self.players) - 1], 2)

    def collect(self) -> typing.List[Card]:
        """
        Collect cards for the crib
        """
        the_crib = []
        # each player tosses card(s) to the crib
        for player in self.players:
            the_crib += player.toss()

        # add cards to the crib to bring the crib size to 4
        # (only needed for three-player games)
        more_cards = max(4 - len(the_crib), 0)
        for i in range(0, more_cards):
            the_crib += [self.deck.pop()]

        return the_crib

    def award(self, player: Player, points: int) -> bool:
        """
        Award a player points
        """
        player.score += points
        if player.score >= self.win:
            raise WinCondition(self.players)
    
    def trick(self) -> bool:
        """
        Players play cards on the stack until no player can play
        """
        # The last player to say go gets one point
        go = 0
        while go < len(self.players):
            for player in self.players:
                if go < len(self.players):
                    card_to_play = player.play(self.stack)
                    if not card_to_play:
                        go += 1
                        if go == len(self.players):
                            self.award(player, 1)
                    else:
                        go = 0
                        self.stack += card_to_play
                        # TODO check stack for points and award those points

    def count(self) -> None:
        """
        Count the points in each player's hand and
        award those points
        """
        for player in self.players:
            self.award(player, score(player.count_hand, self.the_cut))

        self.award(self.players[len(self.players) - 1], score(self.crib, self.the_cut))

def main():
    deck = build_deck()
    random.shuffle(deck)
    hand = draw_hand(deck)
    points = score(hand)
    logger.debug(points)

if __name__ == '__main__':
    main()

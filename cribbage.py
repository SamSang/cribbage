"""
Collection of objects to represent possible cribbage hands
"""

import random
import typing
from itertools import combinations
from itertools import permutations

from logger import logger

faces = {
    "10": {
        "seq": 1,
        "value": 1,
        "letter": "1",
    },
    "Jack": {
        "seq": 11,
        "value": 10,
        "letter": "J",
    },
    "Queen": {
        "seq": 12,
        "value": 10,
        "letter": "Q",
    },
    "King": {
        "seq": 13,
        "value": 10,
        "letter": "K",
    },
    "Ace": {
        "seq": 1,
        "value": 1,
        "letter": "A",
    },
}

suits = {
    "Spade": {
        "letter": "S",
    },
    "Heart": {
        "letter": "H",
    },
    "Diamond": {
        "letter": "D",
    },
    "Club": {
        "letter": "C",
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

    suits = ["Spade", "Heart", "Diamond", "Club"]

    ranks = [
        "Ace",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
    ]

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
        seq = faces[rank]["seq"]
        value = faces[rank]["value"]
    return Card(rank, suit, seq, value)


def build_letter_function(letter):
    def get_letter(pair) -> bool:
        """function to filter a dict by the child key `letter`"""
        key, value = pair
        try:
            if value["letter"] == letter:
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
    cards_text = input("Enter cards: ")
    cards_split = cards_text.split(" ")
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


"""
Constituent functions of scoring a cribbage hand
"""


def add_cards(cards: typing.List[Card]) -> int:
    """
    return sum of values of passed cards
    """
    values = list()
    for card in cards:
        values.append(card.value)
    return sum(values)


def consecutive_cards(cards: typing.List[Card]) -> bool:
    """returns true if all cards in the list are consecutive"""
    is_consecutive = False
    sequence = [card.seq for card in cards]
    lowest_card = min(sequence)
    correct_sequence = range(lowest_card, lowest_card + len(cards))
    if list(sequence) == list(correct_sequence):
        is_consecutive = True
    return is_consecutive


def score_fifteen(cards: typing.List[Card]) -> int:
    """
    Score when a set of cards = 15
    """
    points = 0
    for count_cards in range(len(cards) + 1):
        for subset in combinations(cards, count_cards):
            if add_cards(subset) == 15:
                logger.debug(f"15 two! {subset}")
                points += 2
    return points


def score_pair(cards: typing.List[Card]) -> int:
    """
    Score when a pair of cards has the same rank
    """
    points = 0
    for subset in combinations(cards, 2):
        if len(subset) == 2 and subset[0].rank == subset[1].rank:
            logger.debug(f"A pair in there! {subset}")
            points += 2
    return points


def score_seq(cards: typing.List[Card]) -> int:
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
            # print('compare', sequence, 'to', unique_sequences[i])
            if set(sequence).issuperset(
                unique_sequences[i]
            ):  # run is inside this sequence
                # add the difference between the two to the existing sequence
                # print('add', set(sequence), 'to', unique_sequences[i])
                values_to_add = list(set(sequence).difference(unique_sequences[i]))
                for value_to_add in values_to_add:
                    unique_sequences[i].add(value_to_add)
            if not unique_sequences[i].issubset(set(sequence)):
                unique = False
        if unique:
            # print('add sequence', set(sequence))
            unique_sequences.append(set(sequence))
    # tally points from sequential sets
    unique_sequences_set = set(frozenset(s) for s in unique_sequences)
    for unique_sequence in unique_sequences_set:
        points += len(unique_sequence)
        logger.debug(f"{list(unique_sequence)} for {points} points")
    return points


def score_flush(hand: typing.List[Card], cut: Card) -> int:
    # check for a flush
    points = 0
    suits = list()
    for i in range(len(hand)):
        suits.append(hand[i].suit)
    if len(list(set(suits))) == 1:
        logger.debug("Flush!")
        points += len(hand)
        # check if we get an extra point for the cut matching the flush
        if cut:
            if cut.suit == suits[0]:
                logger.debug("(including the cut)")
                points += 1
    return points


def score_cut(hand: typing.List[Card], cut: Card) -> int:
    # check if the hand has a jack matching the suit of the card in the cut
    if cut:
        for card in hand:
            if card.rank == "Jack" and card.suit == cut.suit:
                logger.debug("Jack in the suit!")
                return 1
    return 0


def score(hand: typing.List[Card], cut: Card = None) -> int:
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


def peg_fifteen(stack: typing.List[Card]) -> int:
    """If the stack totals 15, return 2, else 0"""
    points = 0
    total = 0
    for card in stack:
        total += card.value
    if total == 15:
        points = 2
    return points


def peg_pairs(stack: typing.List[Card]) -> int:
    """
    Return n(n-1) for n > 1 where n is the number of matching ranks
    """
    points = 0
    n = len(stack)
    matching = True
    for i in range(1, n):  # doesn't interate for 1
        if stack[i - 1].rank != stack[i].rank:
            matching = False
    if matching:
        points = n * (n - 1)
    return points


def get_seq(card: Card):
    """Helper function to sort a list of cards"""
    return card.seq


def peg_seq(stack: typing.List[Card]) -> int:
    """
    return the length of the stack if all cards are in sequence
    """
    points = 0
    stack.sort(key=get_seq)
    if consecutive_cards(stack) and len(stack) >= 3:
        points = len(stack)
    return points


def pegs_packs(stack: list) -> list:
    """
    Return the sets of cards to consider in the pegs
    """
    n = max(len(stack), 0)
    packs = []
    for i in range(n - 1):
        packs.append(stack[i:n])
    return packs


def peg_31(stack: typing.List[Card]) -> int:
    """Return 1 if stack totals 31"""
    points = 0
    if sum(card.value for card in stack) == 31:
        points = 1
    return points


def score_pegs(stack: typing.List[Card]) -> int:
    """
    Scoring the pegs

    stack is the stack played, including the latest card

    Scoring pegs looks at the stack,
    confirms the set to score contains the latest card, then
    returns the total points awarded.
    """
    # fifteen, pairs, sequence
    points = 0
    checks = [
        peg_fifteen,
        peg_pairs,
        peg_seq,
    ]
    for check in checks:
        result = [0]
        for pack in pegs_packs(stack):
            result.append(check(pack))
        points += max(result)
    points += peg_31(stack)
    return points


"""
Strategies for the Player class to use

Player can
pick n cards for the crib and
play 1 card to the stack

In each case, we have to return the hand
so Player knows their new hand.

pegs will be a wrapper that screens possible cards
for the pegs strategy
"""


def pick_sequence(
    hand: typing.List[Card], seen: typing.List[Card], n: int
) -> typing.Tuple[typing.List[Card], typing.List[Card]]:
    """Choose next sequence cards"""
    chosen = []
    for i in range(n):
        chosen.append(hand.pop(0))
    return hand, chosen


def play_sequence(
    possible: typing.List[Card], seen: typing.List[Card], stack: typing.List[Card]
) -> Card:
    """Choose next card in sequence, or return an empty list"""
    possible, card = pick_sequence(possible, None, 1)
    return card[0]


def pegs(
    hand: typing.List[Card],
    seen: typing.List[Card],
    stack: typing.List[Card],
    choose=play_sequence,
    stack_max=31,
) -> typing.Tuple[typing.List[Card], Card]:
    """Select a card to play on the stack"""
    stack_total = sum([card.value for card in stack])
    diff = stack_max - stack_total
    possible = []
    for card in hand:
        if card.value <= diff:
            possible.append(card)
    try:
        card = choose(possible, seen, stack)
        hand.remove(card)
        return hand, card
    except IndexError:
        return hand, None


class Player(object):
    def __init__(
        self,
        name="Player 0",
        hand: typing.List[Card] = None,
        strategy_hand=pick_sequence,
        strategy_pegs=play_sequence,
    ) -> None:
        self.name = name
        self.score = 0
        if not hand:
            self._hand: typing.List[Card] = []
            self.count_hand: typing.List[Card] = []
        else:
            self._hand: typing.List[Card] = hand
            self.count_hand: typing.List[Card] = hand
        self._seen = set()
        self.strategy_hand = strategy_hand
        self.strategy_pegs = strategy_pegs

    def __repr__(self):
        return str(
            {
                "name": self.name,
                "score": self.score,
                "hand": self.hand,
                # "seen": self.seen,
                "strat_hand": self.strategy_hand.__name__,
                "strat_pegs": self.strategy_pegs.__name__,
            }
        )

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

    def play(self, stack: typing.List[Card]):
        """
        Add a card to the stack
        """
        self.hand, card = pegs(self.hand, self.seen, stack, self.strategy_pegs)
        return card


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

    def __init__(
        self, players: typing.List[Player], deck: typing.List[Card] = [], seq=0, win=121
    ) -> None:
        self.players = players
        self.deck = deck
        if not deck:
            self.deck = build_deck()
        self.seq = seq
        self.win = win
        self.turn_number = 0
        self.go = 0
        self.the_cut: Card = None
        self.crib: typing.List[Card] = []
        self.stack: typing.List[Card] = []

    def show(self, card: Card) -> None:
        """
        Show each player one card
        """
        for player in self.players:
            player.see(card)

    def cut(self) -> None:
        """
        Select a card from the deck and place it in the cut
        """
        # Cut must not be in the top 5 or bottom five cards
        i = random.randint(5, len(self.deck) - (1 + 5))
        self.the_cut = self.deck.pop(i)
        self.show(self.the_cut)
        if self.the_cut.rank == "Jack":
            self.award(self.players[0], 2)  # first player is dealer and gets the cut

    def deal(self) -> None:
        """
        Deal cards to each player
        """
        hand_size = 4 + (4 // len(self.players))
        for i in range(0, hand_size):
            for player in self.players:
                player.hand += [self.deck.pop()]

    def collect(self) -> None:
        """
        Collect cards for the crib
        """
        the_crib = []
        # each player tosses card(s) to the crib then
        # make a shallow copy of the hand to count later
        for player in self.players:
            the_crib += player.toss()
            player.count_hand = list(player.hand)

        # add cards to the crib to bring the crib size to 4
        # (only needed for three-player games)
        more_cards = max(4 - len(the_crib), 0)
        for i in range(0, more_cards):
            the_crib += [self.deck.pop()]

        self.crib = the_crib

    def award(self, player: Player, points: int) -> None:
        """
        Award a player points and check if they've won
        """
        if points < 1:
            return
        logger.info(f"Award player {player.name} {points} points")
        player.score += points
        if player.score >= self.win:
            logger.info(f"Player {player.name} wins!")
            raise WinCondition(self.players)

    def turn(self, i: int) -> None:
        """
        Player at index i adds a card to the stack
        """
        player = self.players[i]
        points = 0
        card_to_play = player.play(self.stack)
        if not card_to_play:
            self.go += 1
            # The last player to say go gets one point
            if self.go == len(self.players):
                points = 1
        else:
            self.go = 0
            self.stack.append(card_to_play)
            points = score_pegs(self.stack)
        self.award(player, points)

    def trick(self) -> None:
        """Play turns until all players have said go"""
        self.go = 0
        n = len(self.players)
        while self.go < n:
            # dealer is first in the list
            # but dealer plays last
            self.turn_number += 1
            player_index = self.turn_number % n
            self.turn(
                player_index
            )  # player takes a turn, which (re)sets the go counter

    def tricks(self) -> None:
        """
        Play tricks until there are not cards left in hands
        """
        while sum([len(player.hand) for player in self.players]) > 0:
            self.stack = []
            self.trick()

    def count(self) -> None:
        """
        Count the points in each player's hand and
        award those points
        """
        for player in self.players:
            self.award(player, score(player.count_hand, self.the_cut))

        self.award(self.players[len(self.players) - 1], score(self.crib, self.the_cut))


class Game(object):
    def __init__(
        self,
        name: str = "",
        n: int = 0,
        players: typing.List[Player] = [],
        win: int = 121,
    ) -> None:
        self.name = name

        self.players: typing.List[Player] = []
        if n:
            for i in range(n):
                self.players.append(Player(f"{i+1}"))
        if players:
            self.players = players
        self.n = len(self.players)

        self.dealer_index: int = 0
        self.deck: typing.List[Card] = []
        self.win = win
        self.results: dict = {}

    def shuffle(self):
        """Rebuild the deck of cards"""
        for player in self.players:
            player.reshuffle()
        self.deck = build_deck()
        # doing this randomly, for now
        random.shuffle(self.deck)

    def advance(self):
        """Change list of players to reflect the dealer"""
        self.players.insert(0, self.players.pop())

    def play(self):
        """
        Play hands until one player wins
        """
        try:
            i = 0
            while True:
                i += 1
                self.advance()
                self.shuffle()
                hand = Hand(players=self.players, deck=self.deck, seq=i, win=self.win)
                hand.deal()
                hand.collect()
                hand.cut()
                hand.tricks()
                hand.count()
        except WinCondition as e:
            self.results = {
                "players": e.players,
                "hands": i,
            }

def main():
    game = Game(n=2)
    # print(game.players)
    game.play()
    print(game.results)


if __name__ == "__main__":
    main()

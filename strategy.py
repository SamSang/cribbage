"""
Collection of strategies for
the Player class to use

Player can
pick n cards for the crib and
play 1 card to the stack

In each case, we have to return the hand
so Player knows their new hand.

pegs will be a wrapper that screens possible cards
for the pegs strategy
"""

import typing

from cribbage import Card

def pick_sequence(
        hand: typing.List[Card],
        seen: typing.List[Card],
        n: int
    ) -> typing.Tuple[typing.List[Card], typing.List[Card]]:
    """Choose next sequence cards"""
    chosen = []
    for i in range(n):
        chosen.append(hand.pop(0))
    return hand, chosen

def play_sequence(
        possible: typing.List[Card],
        seen: typing.List[Card],
        stack: typing.List[Card]
    ) -> Card:
    """Choose next card in sequence, or return an empty list"""
    possible, card = pick_sequence(possible, None, 1)
    return card[0]

def pegs(
        hand: typing.List[Card],
        seen: typing.List[Card],
        stack: typing.List[Card],
        choose = play_sequence,
        stack_max = 31
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

# Cribbage!
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](coverage.svg)

I love cribbage. But no one will play with me, so I'm writing a silly vanity project to build lots of classes.

## Setup

Run `cribbage.py` for an example of using a `Game` class to build results.

The plan is for this project to work without installing additional dependencies.

## Description

When making a `Game` instance, provide either `n` for the number of default players or a list of 1-4 `Player`s. Those players will participate in the required number of `Hand`s until one player wins, at which point the `results` of the `Game` will be available.

`Player`s use different strategies to determine what cards to play. The default is to play cards in sequence from the hand (as randomly as the deck was shuffled, essentially). Take a look at `pick_sequence` and `play_sequence` for the signatures of "pick"ing cards for the crib and "play"ing a card on the stack.

## Development

What's the point of writing anything if the code isn't tested?

Run tests:

```shell
python3 tests.py
```

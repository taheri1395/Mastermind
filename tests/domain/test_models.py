from mastermind.domain.models import Mastermind, Color
from typing import Sequence
from pytest import raises
import re


def test_starting_a_new_game() -> None:
    # Arrange (empty)

    # Act
    game = Mastermind()

    # Assert (empty)


def test_getting_trials_of_a_new_game() -> None:
    # Arrange
    game = Mastermind()

    # Act
    trials = game.trials

    # Assert
    assert isinstance(trials, Sequence)
    assert not trials


def test_state_of_a_new_game() -> None:
    # Arrange
    game = Mastermind()

    # Act
    state = game.state

    # Assert
    assert state == 'playing'


def test_making_a_guess_on_a_new_game() -> None:
    # Arrange
    game = Mastermind()

    # Act
    game.guess([Color.RED] * 4)

    # Assert (empty)


def test_making_a_guess_with_more_than_sufficient_number_of_colors() -> None:
    # Arrange
    game = Mastermind()

    # Act, Assert
    with raises(ValueError, match='number of colors'):
        game.guess([Color.RED] * 5)


def test_making_a_guess_with_less_than_sufficient_number_of_colors() -> None:
    # Arrange
    game = Mastermind()

    # Act, Assert
    with raises(ValueError, match='number of colors'):
        game.guess([Color.RED] * 3)

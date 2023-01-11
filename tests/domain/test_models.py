from mastermind.domain.models import Mastermind, CodePeg
from typing import Sequence
from pytest import raises
import re
from unittest.mock import Mock


def test_starting_a_new_game() -> None:
    # Arrange (empty)

    # Act
    game = Mastermind(code_maker=Mock())

    # Assert (empty)


def test_getting_trials_of_a_new_game() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act
    trials = game.trials

    # Assert
    assert isinstance(trials, Sequence)
    assert not trials


def test_state_of_a_new_game() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act
    state = game.state

    # Assert
    assert state == 'playing'


def test_making_a_guess_on_a_new_game() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act
    game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)

    # Assert (empty)


def test_making_a_guess_with_more_than_sufficient_number_of_code_pegs() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act, Assert
    with raises(ValueError, match='number of code-pegs'):
        game.guess([CodePeg.RED] * (Mastermind.MAXIMUM_NUMBER_OF_GUESSES + 1))


def test_making_a_guess_with_less_than_sufficient_number_of_code_pegs() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act, Assert
    with raises(ValueError, match='number of code-pegs'):
        game.guess([CodePeg.RED] * (Mastermind.MAXIMUM_NUMBER_OF_GUESSES - 1))


def test_making_a_guess_should_add_a_new_trial() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act
    game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)

    # Assert
    assert len(game.trials) == 1


def test_state_after_maximum_number_of_wrong_guesses() -> None:
    # Arrange
    code_maker = Mock(make=Mock(return_value=[CodePeg.BLUE] * Mastermind.NUMBER_OF_CODE_PEGS))
    game = Mastermind(code_maker=code_maker)
    for i in range(Mastermind.MAXIMUM_NUMBER_OF_GUESSES):
        game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)

    # Act
    state = game.state
    
    # Assert
    assert state == "lost"

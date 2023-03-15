import re
from typing import Sequence
from unittest.mock import Mock

from pytest import raises

from mastermind.domain.models import CodeMaker, CodePeg, KeyPeg, Mastermind


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
    assert state == "playing"


def test_making_a_guess_on_a_new_game() -> None:
    # Arrange
    game = Mastermind(
        code_maker=Mock(
            make=Mock(return_value=[Mock()] * Mastermind.NUMBER_OF_CODE_PEGS)
        )
    )

    # Act
    game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)

    # Assert (empty)


def test_making_a_guess_with_more_than_sufficient_number_of_code_pegs() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act, Assert
    with raises(ValueError, match="number of code-pegs"):
        game.guess([CodePeg.RED] * (Mastermind.MAXIMUM_NUMBER_OF_GUESSES + 1))


def test_making_a_guess_with_less_than_sufficient_number_of_code_pegs() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act, Assert
    with raises(ValueError, match="number of code-pegs"):
        game.guess([CodePeg.RED] * (Mastermind.MAXIMUM_NUMBER_OF_GUESSES - 1))


def test_making_a_guess_should_add_a_new_trial() -> None:
    # Arrange
    game = Mastermind(
        code_maker=Mock(
            make=Mock(return_value=[Mock()] * Mastermind.NUMBER_OF_CODE_PEGS)
        )
    )

    # Act
    game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)

    # Assert
    assert len(game.trials) == 1


def test_state_after_maximum_number_of_wrong_guesses() -> None:
    # Arrange
    code_maker = Mock(
        make=Mock(return_value=[CodePeg.BLUE] * Mastermind.NUMBER_OF_CODE_PEGS)
    )
    game = Mastermind(code_maker=code_maker)
    for _ in range(Mastermind.MAXIMUM_NUMBER_OF_GUESSES):
        game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)

    # Act
    state = game.state

    # Assert
    assert state == "lost"


def test_making_a_guess_should_raise_error_when_state_is_lost() -> None:
    # Arrange
    code_maker = Mock(
        make=Mock(return_value=[CodePeg.BLUE] * Mastermind.NUMBER_OF_CODE_PEGS)
    )
    game = Mastermind(code_maker=code_maker)
    for _ in range(Mastermind.MAXIMUM_NUMBER_OF_GUESSES):
        game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)

    # Act
    state = game.state

    # Assume
    assert state == "lost"

    # Assert
    with raises(AssertionError):
        game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)


def test_making_a_correct_guess_should_change_the_state_to_won() -> None:
    # Arrange
    secret_pegs = guess_pegs = [CodePeg.BLUE] * Mastermind.NUMBER_OF_CODE_PEGS
    code_maker = Mock(make=Mock(return_value=secret_pegs))
    game = Mastermind(code_maker=code_maker)
    game.guess(guess_pegs)

    # Act
    state = game.state

    # Assert
    assert state == "won"


def test_making_a_guess_should_raise_error_when_state_is_won() -> None:
    # Arrange
    secret_pegs = guess_pegs = [CodePeg.BLUE] * Mastermind.NUMBER_OF_CODE_PEGS
    code_maker = Mock(make=Mock(return_value=secret_pegs))
    game = Mastermind(code_maker=code_maker)
    game.guess(guess_pegs)

    # Act
    state = game.state

    # Assume
    assert state == "won"

    # Assert
    with raises(AssertionError):
        game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)


def test_guess_peg_with_incorrect_color_and_position_should_generate_no_key_peg() -> (
    None
):
    # Assert
    code_maker = Mock(
        make=Mock(return_value=[CodePeg.BLUE] * Mastermind.NUMBER_OF_CODE_PEGS)
    )
    game = Mastermind(code_maker=code_maker)
    game.guess([CodePeg.RED] * Mastermind.NUMBER_OF_CODE_PEGS)

    # Act
    last_trial = game.trials[-1]
    response = last_trial.response_pegs

    # Assert
    assert not response


def test_guess_peg_with_correct_color_and_incorrect_position_should_generate_black_key_peg() -> (
    None
):
    # Assert
    secret_pegs = [CodePeg.BLUE] * (Mastermind.NUMBER_OF_CODE_PEGS - 1) + [
        CodePeg.BROWN
    ]
    guess_pegs = [CodePeg.BROWN] + [CodePeg.RED] * (Mastermind.NUMBER_OF_CODE_PEGS - 1)
    code_maker = Mock(make=Mock(return_value=secret_pegs))
    game = Mastermind(code_maker=code_maker)
    game.guess(guess_pegs)

    # Act
    last_trial = game.trials[-1]
    response = list(last_trial.response_pegs)

    # Assert
    assert response == [KeyPeg.BLACK]


def test_guess_peg_with_correct_color_and_position_should_generate_white_key_peg() -> (
    None
):
    # Assert
    secret_pegs = [CodePeg.BLUE] * (Mastermind.NUMBER_OF_CODE_PEGS - 1) + [
        CodePeg.BROWN
    ]
    guess_pegs = [CodePeg.RED] * (Mastermind.NUMBER_OF_CODE_PEGS - 1) + [CodePeg.BROWN]
    code_maker = Mock(make=Mock(return_value=secret_pegs))
    game = Mastermind(code_maker=code_maker)
    game.guess(guess_pegs)

    # Act
    last_trial = game.trials[-1]
    response = list(last_trial.response_pegs)

    # Assert
    assert response == [KeyPeg.WHITE]


def test_a_guess_peg_should_only_affect_response_once() -> None:
    # Assert
    secret_pegs = [CodePeg.BLUE] * (Mastermind.NUMBER_OF_CODE_PEGS - 1) + [
        CodePeg.BROWN
    ]
    guess_pegs = [CodePeg.RED] * (Mastermind.NUMBER_OF_CODE_PEGS - 2) + [
        CodePeg.BROWN,
        CodePeg.BROWN,
    ]
    code_maker = Mock(make=Mock(return_value=secret_pegs))
    game = Mastermind(code_maker=code_maker)
    game.guess(guess_pegs)

    # Act
    last_trial = game.trials[-1]
    response = list(last_trial.response_pegs)

    # Assert
    assert response == [KeyPeg.WHITE]


def test_getting_secret_key_should_raise_error_when_state_is_playing() -> None:
    # Arrange
    game = Mastermind(code_maker=Mock())

    # Act
    state = game.state

    # Assume
    assert state == "playing"

    # Assert
    with raises(AssertionError):
        game.secret_pegs


def test_getting_secret_key_when_state_is_not_playing() -> None:
    # Arrange
    secret_pegs = guess_pegs = [CodePeg.BLUE] * Mastermind.NUMBER_OF_CODE_PEGS
    code_maker = Mock(make=Mock(return_value=secret_pegs))
    game = Mastermind(code_maker=code_maker)
    game.guess(guess_pegs)

    # Act
    state = game.state

    # Assume
    assert state == "won"

    # Assert
    assert game.secret_pegs


def test_code_maker() -> None:
    # Arrange
    code_maker = CodeMaker()
    n = 5

    # Act
    result = code_maker.make(n)

    # Assert
    assert len(result) == n

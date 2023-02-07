from __future__ import annotations

from typing import Final, Sequence, List, Iterable
from enum import Enum
from dataclasses import dataclass


class Mastermind:
    MAXIMUM_NUMBER_OF_GUESSES: Final[int] = 10
    NUMBER_OF_CODE_PEGS: Final[int] = 4

    def __init__(self, code_maker: CodeMaker):
        self._trials: List[Trial] = []
        self._secret_pegs = code_maker.make()

    @property
    def secret_pegs(self) -> Sequence[CodePeg]:
        if self.state == 'playing':
            raise AssertionError('Secret pegs are only visible when game is finished.')
        return self._secret_pegs

    @property
    def trials(self) -> Sequence[Trial]:
        return self._trials

    @property
    def state(self) -> str:
        if len(self._trials) >= self.MAXIMUM_NUMBER_OF_GUESSES:
            return 'lost'
        if self._trials and self._trials[-1].guess_pegs == self._secret_pegs:
            return 'won'
        return 'playing'

    def guess(self, guess_pegs: Sequence[CodePeg]) -> None:
        if self.state in ('lost', 'won'):
            raise AssertionError(
                'A new guess is not allowed when the state of the game is '
                '"{}".'.format(self.state)
            )
        if len(guess_pegs) != self.NUMBER_OF_CODE_PEGS:
            raise ValueError('Invalid number of code-pegs.')
        self._trials.append(Trial(guess_pegs, self._compare(guess_pegs)))

    def _compare(self, guess_pegs: Sequence[CodePeg]) -> Iterable[KeyPeg]:
        result = []
        checked_indices = []
        for i, secret_peg in enumerate(self._secret_pegs):
            if secret_peg == guess_pegs[i] and i not in checked_indices:
                result.append(KeyPeg.WHITE)
                checked_indices.append(i)
        for i, secret_peg in enumerate(self._secret_pegs):
            if secret_peg in guess_pegs and i not in checked_indices:
                result.append(KeyPeg.BLACK)
                checked_indices.append(i)
        return result


class CodeMaker:
    def make(self) -> Sequence[CodePeg]:
        pass


class CodePeg(str, Enum):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    PINK = 'pink'
    BROWN = 'brown'


class KeyPeg(str, Enum):
    WHITE = 'white'
    BLACK = 'black'


@dataclass
class Trial:
    guess_pegs: Sequence[CodePeg]
    response_pegs: Iterable[KeyPeg]

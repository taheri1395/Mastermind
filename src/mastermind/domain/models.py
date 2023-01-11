from __future__ import annotations

from typing import Final, Sequence
from enum import Enum


class Mastermind:
    MAXIMUM_NUMBER_OF_GUESSES: Final[int] = 10
    NUMBER_OF_CODE_PEGS: Final[int] = 4

    def __init__(self, code_maker: CodeMaker):
        self._trials = []
        self._code_maker = code_maker

    @property
    def trials(self) -> Sequence:
        return self._trials

    @property
    def state(self) -> str:
        if len(self._trials) >= self.MAXIMUM_NUMBER_OF_GUESSES:
            return 'lost'
        return 'playing'

    def guess(self, code_pegs: Sequence[CodePeg]) -> None:
        if len(code_pegs) != self.NUMBER_OF_CODE_PEGS:
            raise ValueError('Invalid number of code-pegs.')
        self._trials.append(code_pegs)
        


class CodePeg(str, Enum):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    WHITE = 'white'
    BLACK = 'black'


class CodeMaker:
    pass

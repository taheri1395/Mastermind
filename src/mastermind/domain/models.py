from __future__ import annotations

from typing import Sequence
from enum import Enum


class Mastermind:
    @property
    def trials(self) -> Sequence:
        return []

    @property
    def state(self) -> str:
        return 'playing'

    def guess(self, colors: Sequence[Color]) -> None:
        if len(colors) != 4:
            raise ValueError('Invalid number of colors.')


class Color(str, Enum):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    WHITE = 'white'
    BLACK = 'black'

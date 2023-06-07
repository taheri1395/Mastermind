from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum
from typing import Final, Iterable, List, Sequence, Optional, Any


class CodeMaker:
    def make(self, num: int) -> Sequence[CodePeg]:
        return random.choices(list(CodePeg), k=num)

from typing import TypeVar

class Entity(type):
    @property
    def objects(self) -> Repository:
        pass

TEntity = TypeVar("TEntity", bound=Entity)

class Repository:
    def __init__(self) -> None:
        self._items = []

    def all(self) -> Iterable[TEntity]:
        return self._items
    
    def get(self, **kwargs: Any) -> TEntity:
        result = [
            item
            for item in self._items
            if all(getattr(item, name) == value for name, value in kwargs.items())
        ]
        if not result:
            raise ValueError("No element found.")
        elif len(result) > 1:
            raise ValueError("Too many")
        return next(filter(lambda item: all(getattr(item, name) == value for name, value in kwargs.items()), self._items))


class User(Entity):
    def __init__(self, session_id: str) -> None:
        self._session_id = session_id


class Mastermind:
    MAXIMUM_NUMBER_OF_GUESSES: Final[int] = 10
    NUMBER_OF_CODE_PEGS: Final[int] = 4

    def __init__(self, code_maker: Optional[CodeMaker] = None) -> None:
        code_maker = code_maker or CodeMaker()

        self._trials: List[Trial] = []
        self._secret_pegs = code_maker.make(Mastermind.NUMBER_OF_CODE_PEGS)

    @property
    def secret_pegs(self) -> Sequence[CodePeg]:
        if self.state == GameState.PLAYING:
            raise AssertionError("Secret pegs are only visible when game is finished.")
        return self._secret_pegs

    @property
    def trials(self) -> Sequence[Trial]:
        return self._trials

    @property
    def state(self) -> str:
        # TODO: Test edge cases.
        if self._trials and self._trials[-1].guess_pegs == self._secret_pegs:
            return GameState.WON

        if len(self._trials) >= self.MAXIMUM_NUMBER_OF_GUESSES:
            return GameState.LOST

        return GameState.PLAYING

    def guess(self, guess_pegs: Sequence[CodePeg]) -> None:
        if self.state in (GameState.LOST, GameState.WON):
            raise AssertionError(
                "A new guess is not allowed when the state of the game is "
                '"{}".'.format(self.state)
            )
        if len(guess_pegs) != self.NUMBER_OF_CODE_PEGS:
            raise ValueError("Invalid number of code-pegs.")
        self._trials.append(Trial(guess_pegs, self._compare(guess_pegs)))

    def _compare(self, guess_pegs: Sequence[CodePeg]) -> Iterable[KeyPeg]:
        unsorted_result = []
        for i, guess_peg in enumerate(guess_pegs):
            if self._secret_pegs[i] == guess_peg:
                unsorted_result.append(KeyPeg.WHITE)
            elif guess_peg in self._secret_pegs:
                unsorted_result.append(KeyPeg.BLACK)
        return sorted(
            unsorted_result,
            key=lambda key_peg: key_peg == KeyPeg.BLACK
        )


class MastermindPlayer:
    def __init__(self, game: Mastermind, user: User) -> None:
        self._game = game
        self._user = user

    def guess(self, guess_pegs: Sequence[CodePeg]) -> None:
        self._game.guess(guess_pegs)


class CodePeg(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    PINK = "pink"
    BROWN = "brown"


class KeyPeg(str, Enum):
    WHITE = "white"
    BLACK = "black"


class GameState(str, Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


@dataclass
class Trial:
    guess_pegs: Sequence[CodePeg]
    response_pegs: Iterable[KeyPeg]

from dataclasses import dataclass
from enum import Enum


class History:
    """A class to manage storing the events that happened in a Logger."""

    @dataclass
    class Event:
        """Internal of an event."""

        class Semantic(Enum):
            CONSOLE = 1

        type: Semantic
        value: str

    def __init__(self):
        self._storage: list[History.Event] = []

    @property
    def storage(self) -> list[Event]:
        return self._storage

    def add(self, type: Event.Semantic, value: str):
        self._storage.append(History.Event(type, value))

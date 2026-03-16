from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class EntityList(ABC, Generic[T]):
    """A dual-indexed list-like collection.

    Supports access by integer position and by string key defined by `_key`.
    """

    def __init__(self, items: Iterable[T] | None = None):
        self._items: list[T] = []
        self._by_key: dict[str, T] = {}

        if items is not None:
            for item in items:
                self.append(item)

    @abstractmethod
    def _key(self, item: T) -> str:
        pass

    def append(self, item: T) -> None:
        self._items.append(item)
        self._by_key[self._key(item)] = item

    def __getitem__(self, key: int | str) -> T:
        if isinstance(key, int):
            return self._items[key]
        if isinstance(key, str):
            return self._by_key[key]
        raise TypeError("EntityList indices must be int or str")

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item: str | T) -> bool:
        if isinstance(item, str):
            return item in self._by_key
        return item in self._items

    def keys(self) -> list[str]:
        return list(self._by_key.keys())

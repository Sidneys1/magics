from itertools import chain
from typing import TypeVar, Type, Iterable

from .items import Item
from .props import Prop
from .knowledge import Knowledge
from .util.singleton import Singleton

TType = TypeVar('TType')


class _PlayerSingleton(metaclass=Singleton):
    knowledge: list[Type[Knowledge]] = []
    inventory: list[Type[Item]] = []

    @classmethod
    def get_of_type(cls, of_type: Type[TType]) -> Iterable[Type[TType]]:
        return (x for x in chain(cls.knowledge, cls.inventory, Prop.PROPS) if issubclass(x, of_type))


Player = _PlayerSingleton()

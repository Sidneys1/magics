from typing import Type

from .. import T
from ..base import BaseOfEverything
from ..interactions import Inspectable


class Prop(BaseOfEverything, Inspectable):
    PROPS: list[Type['Prop']] = []

    @classmethod
    def _formatted(cls) -> str:
        return T.underline + super()._formatted() + T.normal

    @classmethod
    def add(cls, clazz):
        cls.PROPS.append(clazz)
        return clazz

    @classmethod
    def __str__(cls):
        return getattr(cls, 'name', cls.__name__)

    @classmethod
    def remove(cls):
        cls.PROPS.remove(cls)


from .cauldron import *
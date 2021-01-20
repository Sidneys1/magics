
from . import Item
from .. import T
from ..essences import Essences
from ..interactions import Useable

class Ring(Item, Useable):
    NAME = "Magical Ring"
    COLOR = T.blue
    MAGICAL_PROPERTIES = {Essences.Fire: 1, Essences.Stone: 2}

    @classmethod
    def inspect(cls): 
        print(f"A {cls.fmt}, forged in fire.")

    @classmethod
    def use(cls, use_on=None):
        print(f"The {cls.fmt} does nothing.")
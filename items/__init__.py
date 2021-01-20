from ..essences import Essences
from ..interactions import Inspectable
from ..base import BaseOfEverything


class Item(BaseOfEverything, Inspectable):
    MAGICAL_PROPERTIES: dict[Essences, int] = {}

    @classmethod
    def destroy(cls):
        from ..player import Player
        Player.inventory.remove(cls)
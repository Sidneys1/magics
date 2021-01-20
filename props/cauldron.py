from random import choice, choices, shuffle
from typing import Optional, Type
from itertools import repeat

from . import Prop

from .. import T
from ..items import Item
# from ..player import Player
from ..essences import Essences, ESSENCE_COLOR, average_color
from ..interactions import Useable


@Prop.add
class Cauldron(Prop, Useable):
    COLOR = T.bright_black
    NAME = "The Cauldron"
    contents: dict[Essences, int] = {}

    @classmethod
    def use(cls, use_on: Optional[Type['Useable']] = None):
        if use_on is None:
            if not cls.contents:
                print(f'{cls.fmt} is empty, and nothing happens.')
            else:
                colors = []
                for color, amount in cls.contents.items():
                    colors.extend(repeat(ESSENCE_COLOR[color], amount))

                print(
                    f'{T.blink + T.color_rgb(*average_color(colors))}Poof{T.normal}, something happened! {cls.fmt} is now empty.'
                )
                cls.contents.clear()
            return
        if not issubclass(use_on, Item) or not use_on.MAGICAL_PROPERTIES:
            print(f'{use_on.fmt} does not have magical properties...')
            return
        message = f'You add {use_on.fmt} to {cls.fmt}.'
        k: Essences
        for k, v in use_on.MAGICAL_PROPERTIES.items():
            breakdown = k.break_down_to_tier(0)
            colors = list()
            for k2, v2 in breakdown.items():
                if k2 not in cls.contents:
                    cls.contents[k2] = v * v2
                else:
                    cls.contents[k2] += v * v2
                colors.extend(repeat(ESSENCE_COLOR[k2], v * v2))
            # if Player.knows(MagicLevel1)
            smokes = [
                '✦', '✧', '★', '✩', '✪', '✫', '✬', '✭', '✮', '✯', '✰', '✱', '✲', '✵', '✶', '✷', '✸', '✹', '✺', '✻', '✼',
                '✽'
            ]
            if True:
                message += f" A curl of {T.color_rgb(*ESSENCE_COLOR[k])}smoke{T.normal} appears: {T.color_rgb(*ESSENCE_COLOR[k])}{''.join(choices(smokes, k=v))}{T.normal}"
                if len(breakdown) > 1:
                    shuffle(colors)
                    message += ", dissolving into many colors: " + ''.join(
                        f"{T.color_rgb(*x)}{choice(smokes)}{T.normal}" for x in colors)
                message += "."
        message += " A pool of liquid remains in the bottom of the cauldron."

        print(message)
        use_on.destroy()

    @classmethod
    def can_use_on(cls, use_on: Type['Useable']):
        return issubclass(use_on, Item) and use_on.MAGICAL_PROPERTIES

    @classmethod
    def inspect(cls):
        text = f'{cls.fmt}'
        if not cls.contents:
            text += ' is empty.'
        else:
            text += ' contains: ' + ', '.join(f"{v:,} units of {k.fmt}" for k, v in cls.contents.items())
        print(text)


__all__ = []
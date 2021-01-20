from enum import Enum, auto
from typing import Optional, Any

from . import T

ESSENCE_BREAKDOWN: dict['Essences', Optional[dict['Essences', int]]]
ESSENCE_TIER: dict['Essences', int] = {}
ESSENCE_COLOR: dict['Essences', Any] = {}

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class Essences(AutoName):
    Earth = auto()
    Air = auto()
    Fire = auto()
    Water = auto()

    Mist = auto()
    Dust = auto()
    Mud = auto()
    Smoke = auto()
    Steam = auto()
    Lava = auto()

    Obsidian = auto()
    Clay = auto()

    Stone = auto()

    Sharpness = auto()

    @property
    def fmt(self) -> str:
        if self not in ESSENCE_COLOR:
            return self.name
        return f"{T.color_rgb(*ESSENCE_COLOR[self])}{self.name}{T.normal}"

    def __repr__(self) -> str:
        return self.name

    def break_down_to_tier(self, tier: int) -> dict['Essences', int]:
        if ESSENCE_TIER[self] <= tier:
            return {self: 1}

        output = {}
        for k, v in ESSENCE_BREAKDOWN[self].items():
            add = k.break_down_to_tier(tier)
            for k2, v2 in add.items():
                if k2 in output:
                    output[k2] += v * v2
                else:
                    output[k2] = v * v2
        return output

ESSENCE_COLOR = {
    Essences.Earth: (0xA0, 0x52, 0x2D),
    Essences.Air: (0x87, 0xCE, 0xEB),
    Essences.Fire: (0xFF, 0x45, 0x00),
    Essences.Water: (0x00, 0xFF, 0xFF)
}

ESSENCE_BREAKDOWN = {
    # Tier 0
    Essences.Earth: None,
    Essences.Air: None,
    Essences.Fire: None,
    Essences.Water: None,

    # Tier 1
    Essences.Mist: {Essences.Air: 1, Essences.Water: 1},
    Essences.Dust: {Essences.Air: 1, Essences.Earth: 1},
    Essences.Mud: {Essences.Water: 1, Essences.Earth: 1},
    Essences.Smoke: {Essences.Air: 1, Essences.Fire: 1},
    Essences.Steam: {Essences.Water: 1, Essences.Fire: 1},
    Essences.Lava: {Essences.Earth: 1, Essences.Fire: 1},

    # Tier 2
    Essences.Obsidian: {Essences.Lava: 1, Essences.Water: 1},
    Essences.Clay: {Essences.Mud: 1, Essences.Fire: 1},

    # Tier 3
    Essences.Stone: {Essences.Clay: 1, Essences.Fire: 1},

    # Tier 4
    Essences.Sharpness: {Essences.Obsidian: 1, Essences.Stone: 1}
}

def _get_cost_of(essence: Essences) -> int:
    contents = ESSENCE_BREAKDOWN[essence]
    if contents is None:
        ESSENCE_TIER[essence] = 0
        return 0
    max_cost = 0
    for content in contents.keys():
        value = ESSENCE_TIER[content] if content in ESSENCE_TIER else _get_cost_of(content)
        if value > max_cost:
            max_cost = value
    ESSENCE_TIER[essence] = max_cost + 1
    return max_cost + 1

for essence in Essences:
    _get_cost_of(essence)

def average_color(colors: list[tuple[int, int, int]]):
    r = sum(color[0] for color in colors) / len(colors)
    g = sum(color[1] for color in colors) / len(colors)
    b = sum(color[2] for color in colors) / len(colors)
    return int(r), int(g), int(b)

def _get_color_of(essence: Essences) -> tuple[int, int, int]:
    if essence in ESSENCE_COLOR:
        return ESSENCE_COLOR[essence]

    contents = ESSENCE_BREAKDOWN[essence]
    colors = []
    for content in contents.keys():
        colors.append(ESSENCE_COLOR[content] if content in ESSENCE_COLOR else _get_color_of(content))
    color = ESSENCE_COLOR[essence] = average_color(colors)
    return color

for essence in Essences:
    _get_color_of(essence)
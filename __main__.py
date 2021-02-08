from sys import exit
from typing import Callable, Iterable, TypeVar, Optional

from . import T
from .player import Player
from .items.ring import Ring
from .interactions import Inspectable, Useable

TType = TypeVar('TType')

NAME = ''' _       __    __    _   __    __
| |\/|  / /\  / /`_ | | / /`  ( (`
|_|  | /_/--\ \_\_/ |_| \_\_, _)_)
'''

def _find_item(name: str, pool: Iterable[TType]) -> Optional[TType]:
    for item in pool:
        if name == item.__name__.lower() or name == item.name.lower():
            return item


def _do_inspect(rest: list[str]):
    all_inspectable = list(Player.get_of_type(Inspectable))
    if rest:
        search = ' '.join(rest).lower()
        inspectable = _find_item(search, all_inspectable)
        if inspectable is not None:
            inspectable.inspect()
            return
        print(f'Nothing found named {search!r}')
    print("You can inspect: " + ", ".join(x.fmt for x in all_inspectable))


def _do_use(rest: list[str]):
    all_useable = list(Player.get_of_type(Useable))
    if rest:
        on_pos = -1
        try:
            on_pos = rest.index('on')
        except ValueError:
            pass

        search = ' '.join(rest[:on_pos] if on_pos != -1 else rest).lower()
        use = _find_item(search, all_useable)
        if use is not None:
            on_item = None
            if on_pos != -1:
                search = ' '.join(rest[on_pos + 1:]).lower()
                if search:
                    on_item = _find_item(search, all_useable)
                if on_item is not None:
                    if not use.can_use_on(on_item):
                        all_useable = [x.fmt for x in all_useable if x != use and use.can_use_on(x)]
                        message = f'{use.fmt} cannot be used on {on_item.fmt}.'
                        if all_useable:
                            message += ' It can be used on: ' + ', '.join(all_useable)
                        else:
                            message += ' It cannot be used on any item.'
                        print(message)
                        return
                    use.use(on_item)
                    return
                else:
                    if search:
                        print(f'Nothing found named {search!r}')
                    all_useable = [x for x in all_useable if x != use and use.can_use_on(x)]
            else:
                use.use()
                return
        else:
            print(f'Nothing found named {search!r}')
    print("You can use: " + ", ".join(x.fmt for x in all_useable))

VERB_HELP = {
    'help': ('Display this help content', None),
    'exit': ('Exits Magics', None),
    'use': (f'Use an item ({T.bright_black}use <item>{T.normal}), or use an item on another item ({T.bright_black}use <item> on <item>{T.normal})', None),
    'inspect': (f'Inspect an item closely ({T.bright_black}inspect <item>{T.normal})', f'''{T.italic}Note that the resulting description of an item may change if the item is used.{T.normal}'''),
}
VERBS: dict[str, Callable[[list[str]], None]] = {}
def _help(rest: list[str]):
    if not rest:
        print(f"  {T.underline + T.bold + T.bright_white}COMMANDS{T.normal}")
        print("  Command are the different actions you can perform. All commands and their parameters are case-insensitive.")
        for verb in VERBS:
            print(f'   * {T.bright_white(verb.capitalize())}' if verb not in VERB_HELP else f'   * {T.bright_white(verb.capitalize())} - {VERB_HELP[verb][0]}')
        return
    verb = ' '.join(rest)
    verb_help = VERB_HELP.get(verb, ("No help is provided for this command.", None))
    print(f"  {T.underline + T.bold + T.bright_white}{verb.upper()}{T.normal} - {verb_help[0]}")
    if verb_help[1] is not None:
        lines = T.wrap(verb_help[1], width=T.width - 2)
        print('\n  ' + '\n  '.join(lines) + '\n')

VERBS = {
    'help': _help,
    'exit': lambda x: exit(0),
    'use': _do_use, 
    'inspect': _do_inspect, 
}

def main():
    print(T.gold + T.bold + NAME + T.normal)
    Player.inventory.append(Ring)
    
    while True:
        command = input('Enter a command: ').strip().lower().split()
        if not command:
            break
        verb, rest = command[0], command[1:]
        do = VERBS.get(verb)
        if do is None:
            print(f'{verb} is not a valid verb. Try: {", ".join(VERBS.keys())}')
            continue
        do(rest)
    print('Exiting...')


if __name__ == "__main__":
    main()
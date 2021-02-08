from time import sleep

from .. import T

from . import Knowledge


class JournalEntry(Knowledge):
    BODY: str = ''

    @classmethod
    def learn(cls) -> None:
        print(f'You feel a surge of inspiration and hastily pull out your {T.purple}Journal{T.normal}. '
              f'The words begin flowing from your pen as if by some external force:\n')
        remaining = [x.split() for x in cls.BODY.strip().split('\n')]
        with T.cbreak():
            print(f'  ╭┤ {T.purple}Journal{T.normal} │\n  │')
            for line in remaining:
                print(f'{T.normal}  │ {T.italic}', end='', flush=True)
                while len(line):
                    T.inkey()
                    print(line.pop(0) + ' ', end='', flush=True)
                print()
            print(f'{T.normal}  │\n  ╰─')
            sleep(1)
            print(f'\n{T.normal}With the words finally comitted to your Journal, you rest.')
            while T.inkey(timeout=2): pass
        return super().learn()

class MagicAwareness(JournalEntry):
    COLOR = f'{T.orchid}'
    ID = 'magic'
    BODY = f'''

I have long felt that there is more to this world than just the mundane physical accoutrements of everyday life.

This {T.bright_black}Cauldron{T.normal} though... It calls to me.
'''
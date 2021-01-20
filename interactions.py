from typing import Optional, Type


class Useable:
    @classmethod
    def use(cls, use_on: Optional[Type['Useable']] = None): ...

    @classmethod
    def can_use_on(cls, use_on: Type['Useable']): ...


class Inspectable:
    @classmethod
    def inspect(cls): ...
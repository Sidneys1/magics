from .util.classproperty import classproperty

from . import T

class BaseOfEverything:
    COLOR = None
    NAME: str = "UNSET"

    @classproperty
    def name(cls) -> str:
        return cls.NAME

    @classproperty
    def fmt(cls) -> str:
        return cls._formatted()

    @classmethod
    def _formatted(cls) -> str:
        if cls.COLOR is not None:
            return f"{cls.COLOR}{cls.name}{T.normal}"
        return cls.name

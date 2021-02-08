from .. import T
from ..base import BaseOfEverything


class Knowledge(BaseOfEverything):
    ID: str = ''
    
    @classmethod
    def learn(cls) -> None:        
        from ..player import Player
        if cls.ID in Player.knowledge:
            return
        Player.knowledge.append(cls.ID)
        print(f"You are imbued with a knowledge of {cls.COLOR}{cls.ID}{T.normal}.")
from enum import Enum, auto

class GameStates(Enum):
    PLAYERS_TURN = auto() #1
    ENEMY_TURN = auto() #2
    PLAYER_DEAD = auto()

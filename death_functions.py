import libtcodpy as libtcod

from game_states import GameStates
from render_functions import RenderOrder

#Static functions for death of characters

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return 'you died!', GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = '{0} is dead!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
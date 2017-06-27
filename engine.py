import libtcodpy as libtcod

from input_handlers import handle_keys
from entity import Entity
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap

def main():
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50
    isFullscreen = False
    MAP_WIDTH = 80
    MAP_HEIGHT = 45

    colors = {
        'dark_wall': libtcod.Color(0,0,100),
        'dark_ground': libtcod.Color(50, 50, 150)

    }
    player = Entity(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT /2 ), '@', libtcod.white)
    npc = Entity(int(SCREEN_WIDTH / 2 - 5), int(SCREEN_HEIGHT /2 ), '@', libtcod.yellow)
    entities = [npc, player]


    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)


    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', isFullscreen) #Init window as not full screen
    con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)


        render_all(con, entities, game_map, SCREEN_WIDTH, SCREEN_HEIGHT, colors)
        libtcod.console_flush()
        clear_all(con, entities)

        #Checking input
        action = handle_keys(key) #action is a Dictionary
        move = action.get('move')
        exit = action.get('exit')
        isFullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            return True

if __name__ == '__main__':
    main()

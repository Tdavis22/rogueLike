import libtcodpy as libtcod


from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from entity import Entity,  get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from map_objects.game_map import GameMap
from game_messages import MessageLog
from game_states import GameStates
from input_handlers import handle_keys
from render_functions import clear_all, render_all, RenderOrder

def main():
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    BAR_WIDTH = 20
    PANEL_HEIGHT = 7
    PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

    message_x = BAR_WIDTH + 2
    message_width = SCREEN_WIDTH - BAR_WIDTH -2
    message_height = PANEL_HEIGHT - 1

    MAP_WIDTH = 80
    MAP_HEIGHT = 43

    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 30

    FOV_ALGORITHM = 0 #default libtcod FOV alg
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 10

    max_monsters_per_room = 3
    """
    if we were to implement custom tiles
    wall_tile = 256
    floor_tile = 257
    player_tile = 258
    orc_tile = 259
    troll_tile = 260
    scroll_tile = 261
    healingpotion_tile = 262
    sword_tile = 263
    shield_tile = 264
    stairsdown_tile = 265
    dagger_tile = 266
    """
    #BEGIN INITAILIZATION
    colors = {
        'dark_wall': libtcod.Color(0,0,100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall' : libtcod.Color(130, 110, 50),
        'light_ground' : libtcod.Color(200, 180, 50)
    }

    fighter_component = Fighter(hp = 30, defense = 2, power = 5)
    player = Entity(0, 0, '@', libtcod.white, "Player", blocks = True, render_order = RenderOrder.ACTOR, fighter = fighter_component)
    entities = [player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    #The font has 32 chars in a row, and there's a total of 10 rows. Increase the "10" when you add new rows to the sample font file

    #libtcod.console_set_custom_font("TiledFont.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD, 32, 10)
    #load_customfont();
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False) #Init window as not full screen
    con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
    panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    game_map.make_map(MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_WIDTH, MAP_HEIGHT, player, entities, max_monsters_per_room)

    fov_recompute = True # we only need to recompute every time FOV changes like moving
    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    #END INTIALIZATION
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)


        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, SCREEN_WIDTH, SCREEN_HEIGHT,
                   BAR_WIDTH, PANEL_HEIGHT, PANEL_Y, mouse, colors)
        fov_recompute = False #don't need to recopute fov until after drawing new fov
        libtcod.console_flush()
        clear_all(con, entities)

        #Checking input
        action = handle_keys(key) #action is a Dictionary
        move = action.get('move')
        exit = action.get('exit')
        isFullscreen = action.get('fullscreen')

        player_turn_results = []
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN
        if isFullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)


            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                        if game_state == GameStates.PLAYER_DEAD:
                            break
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)
        if exit:
            return True

"""
def load_customfont():
    #index of first custom tile in the file
    tileIndex = 256

    #the y is the row index, here we load the sixth row in the font file. Increase the "6" to load any new rows from the file
    for y in range(4,5):
        libtcod.console_map_ascii_codes_to_font(tileIndex, 32, 0, y)
        tileIndex+= 32
        """
if __name__ == '__main__':
    main()

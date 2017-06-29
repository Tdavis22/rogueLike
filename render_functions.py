import libtcodpy as libtcod

#Params: Con = console ref, entites = list of entity, game_map = map ref, colors = libtcod color Dictionary
def render_all(con, entites, game_map, SCREEN_WIDTH, SCREEN_HEIGHT, colors):

    #Draw all entites in the list entites
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            #Darken non visable tiles
            if wall:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    #Draw all entites
    for entity in entites:
        draw_entity(con, entity)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    #libtcod.console_put_char_ex(con, entity.x, entity.y, entity.char, libtcod.white, libtcod.BKGND_NONE)
    #libtcod.console_put_char_ex(con, entity.x, entity.y, entity.char, libtcod.white, libtcod.black)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    # erase(draw over) the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)

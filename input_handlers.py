import libtcodpy as libtcod


#Parameter = Key Pressed
#Returns a Dictionary
def handle_keys(key):
    # Movement keys
    #Should prolly refactor to case statement
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # ALT+Enter: toggle full screen
        #return {'fullscreen': (not libtcod.console_is_fullscreen())}
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        #Exit the game
        return {'exit': True}

    #base case
    return {}

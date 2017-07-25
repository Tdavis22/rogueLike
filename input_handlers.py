import libtcodpy as libtcod


#Parameter = Key Pressed
#Returns a Dictionary
def handle_keys(key):
    # Movement keys
    #Should prolly refactor to case statement
    #arrow keys or Vim keys 
    key_char = chr(key.c)
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return{'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # ALT+Enter: toggle full screen
        #return {'fullscreen': (not libtcod.console_is_fullscreen())}
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        #Exit the game
        return {'exit': True}

    #base case
    return {}

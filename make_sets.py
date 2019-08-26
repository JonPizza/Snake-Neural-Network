import curses
from curses import wrapper

import sys
import time
import random
from snake_nn import SnakeGame

thingy = {
    'KEY_RIGHT': [1, 0, 0, 0],
    'KEY_LEFT': [0, 1, 0, 0],
    'KEY_DOWN': [0, 0, 1, 0],
    'KEY_UP': [0, 0, 0, 1]
}

sg = SnakeGame([[0, 12], [1, 12]], 'r', (50, 12), 0)

def main(stdscr):
    curses.curs_set(0)

    while True:
        stdscr.clear()
        stdscr.addstr(sg.food[1], sg.food[0], '$')

        for part in sg.snake:
            stdscr.addstr(part[1], part[0], '#')

        k = stdscr.getkey()

        while k not in ('KEY_RIGHT', 'KEY_LEFT', 'KEY_DOWN', 'KEY_UP'):
            k = stdscr.getkey()

        if k == 'KEY_RIGHT':
            sg.update_snake('r')
        elif k == 'KEY_LEFT':
            sg.update_snake('l')
        elif k == 'KEY_DOWN':
            sg.update_snake('d')
        else:
            sg.update_snake('u')
        
        with open('sets.py', 'a') as sets:
            sets.write(str([sg.make_tset(), thingy[k]]) + ',\n')
        
        stdscr.refresh()
        sg.check_eaten()
        
        time.sleep(0.01)

wrapper(main)

import curses
from curses import wrapper

import sys
import time
import random
import epic_nn as epic

thingy = {
    'KEY_RIGHT': [1, 0, 0, 0],
    'KEY_LEFT': [0, 1, 0, 0],
    'KEY_DOWN': [0, 0, 1, 0],
    'KEY_UP': [0, 0, 0, 1]
}

class SnakeGame:
    def __init__(self, snake, last_move, food, eaten):
        self.snake = snake
        self.last_move = last_move
        self.food = food
        self.eaten = eaten

    def update_snake(self, move):
        self.last_move = move

        head = self.snake[-1]

        if self.eaten > 0:
            self.eaten -= 1
        else:
            self.snake.pop(0)

        if self.last_move == 'r':
            self.snake.append((head[0]+1, head[1]))
        elif self.last_move == 'l':
            self.snake.append((head[0]-1, head[1]))
        elif self.last_move == 'u':
            self.snake.append((head[0], head[1]-1))
        elif self.last_move == 'd':
            self.snake.append((head[0], head[1]+1))
        
        if self.snake[-1] in self.snake[:-1]:
            raise Exception("hehe you are bad loooooooool")

    def check_eaten(self):
        if self.food == self.snake[-1]:
            self.move_food()
            self.eaten += 3

    def move_food(self):
        while True:
            self.food = (random.randint(0, 79), random.randint(0, 23))
            if self.food not in self.snake:
                break

    def make_tset(self):
        return [
        self.snake[-1][1]/24,
        (24 - self.snake[-1][1])/24,
        self.snake[-1][0]/80,
        (80 - self.snake[0][0])/80,
        self.snake[0][1]/24,
        (24 - self.snake[0][1])/24,
        self.snake[0][0]/80,
        (80 - self.snake[-1][0])/80,
        1 if self.snake[-1][0] == self.food[0] else 0,
        1 if self.snake[-1][1] == self.food[1] else 0,
        self.food[0]/80,
        self.food[1]/24]
        


sg = SnakeGame([[0, 12], [1, 12]], 'r', (50, 12), 0)

def main(stdscr):
    curses.curs_set(0)

    while True:
        stdscr.clear()
        stdscr.addstr(sg.food[1], sg.food[0], '$')

        for part in sg.snake:
            stdscr.addstr(part[1], part[0], '#')

        k = nn.feed_forward(sg.make_tset())

        if k.index(max(k)) == 0:
            sg.update_snake('r')
        elif k.index(max(k)) == 1:
            sg.update_snake('l')
        elif k.index(max(k)) == 2:
            sg.update_snake('d')
        elif k.index(max(k)) == 3:
            sg.update_snake('u')
        
        stdscr.refresh()
        sg.check_eaten()
        
        time.sleep(0.01)

nn = epic.NeuralNetwork(12, 24, 4, epic.sets.sets, 0.01, epic.read_file(sys.argv[1]))

wrapper(main)
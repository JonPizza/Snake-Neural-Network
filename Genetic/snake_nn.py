import curses
from curses import wrapper
import signal

import json
import sys
import time
import random
import epic_nn as epic

import glob


class SnakeDied(Exception):
    pass


class SnakeGame:
    def __init__(self, snake, last_move, food, eaten, num_moves=0):
        self.snake = snake
        self.last_move = last_move
        self.food = food
        self.eaten = eaten
        self.num_moves = num_moves

    def update_snake(self, move):
        self.last_move = move
        self.num_moves += 1

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

        if self.snake[-1] in self.snake[:-1] or self.hit_wall():
            raise SnakeDied('ur bad')

    def hit_wall(self):
        return self.snake[-1][0] >= 23 or self.snake[-1][0] >= 79

    def check_eaten(self):
        if self.food == self.snake[-1]:
            self.move_food()
            self.eaten += 3

    def move_food(self):
        while True:
            self.food = (random.randint(0, 79), random.randint(0, 23))
            if self.food not in self.snake:
                break

    def make_input_data(self):
        return [
                # FOOD
                1 if self.snake[-1][0] == self.food[0] and self.snake[-1][1] > self.food[1] else 0,
                1 if self.snake[-1][0] == self.food[0] and self.snake[-1][1] < self.food[1] else 0,
                1 if self.snake[-1][1] == self.food[1] and self.snake[-1][0] > self.food[0] else 0,
                1 if self.snake[-1][1] == self.food[1] and self.snake[-1][0] < self.food[0] else 0,
                # WALL
                (self.snake[-1][0])/79,
                (self.snake[-1][1])/23,
                # BODY
                1 if len(set([self.snake[i][0] for i in range(self.snake[-1][0], len(self.snake))]) & set(self.snake)) >= 0 else 0,
                1 if len(set([self.snake[i][0] for i in range(79 - self.snake[-1][0], len(self.snake))]) & set(self.snake)) >= 0 else 0,
                1 if len(set([self.snake[i][1] for i in range(self.snake[-1][1], len(self.snake))]) & set(self.snake)) >= 0 else 0,
                1 if len(set([self.snake[i][1] for i in range(23 - self.snake[-1][1], len(self.snake))]) & set(self.snake)) >= 0 else 0,
            ]


def main(stdscr):
    curses.curs_set(0)

    sg = SnakeGame()

    while True:
        stdscr.clear()
        stdscr.addstr(sg.food[1], sg.food[0], 'π')

        for part in sg.snake:
            stdscr.addstr(part[1], part[0], '@')

        stdscr.refresh()
        sg.check_eaten()

        time.sleep(0.1)
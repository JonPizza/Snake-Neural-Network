def calc_fitness(snake):
    return len(snake.snake) ** 2 / snake.num_moves


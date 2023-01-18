# Copyright (c) 2021 José Puga. Under MIT License.
# My Conway Game of Life implementation usign a single 1d generic array (list)
# Just for fun! :)

import random # To fill the world randomly
import time # To pause between cycles
import os   # This 2 lines are required to clean the screen
from subprocess import call

# avoid magic numbers...
WORLD_WIDTH = 80
WORLD_HEIGH = 25
CYCLE_DELAY = 250 #Delay between cycles in milliseconds
START_POPULATION = 0.3 #(1.0 = 100%) % (percent) of random population at start.

class World:
    # static
    SURROUND = [(-1, -1), (0, -1), (1, -1), \
            (-1, 0), (1, 0), \
            (-1, 1), (0, 1), (1, 1)]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._wrap = False #TODO:
        self.rules = [
                    (True, False), # 0 and 1 dies for underpopulation
                    (True, False),
                    (True, True),  # 2 cell survive
                    (False, True), # 3 neighbours born new cell
                    (True, False), # >3 dies for overpopulation
                    (True, False),
                    (True, False),
                    (True, False),
                    (True, False)]
        self.size = self.height * self.width
        self.map = [False] * self.size
        self.map_next_gen = [False] * self.size

    def __str__(self):
        # No problem with reallocation. https://austinhenley.com/blog/pythonstringsaremutable.html
        result = ""
        col = 0
        for idx in range(self.size):
            result += '*' if self.map[idx] else ' '
            col += 1
            if col == self.width:
                result += '\n'
                col = 0
        return result

    def set(self, idx , cell):
        self.map[idx] = cell

    def get(self, idx):
        return self.map[idx]

    def neighbours(self, idx):
        result = 0
        col = idx % self.width
        row = int(idx / self.width) # Must be integer
        for rel_pos in self.SURROUND:
            if (rel_pos[0] == -1 and col == 0) or (rel_pos[0] == 1 and col == self.width -1):
                continue
            if (rel_pos[1] == -1 and row == 0) or (rel_pos[1] == 1 and row == self.height -1):
                continue
            new_col = col + rel_pos[0]
            new_row = row + rel_pos[1]
            if self.get(new_col + new_row * self.width):
                result += 1
        return result

    def cycle(self):
        for idx in range(self.size):
            neighbours_count = self.neighbours(idx)
            if self.map[idx] == self.rules[neighbours_count][0]:
                self.map_next_gen[idx] = self.rules[neighbours_count][1]
            else:
                self.map_next_gen[idx] = self.map[idx]
        self.map, self.map_next_gen = self.map_next_gen, self.map # Swap            


# main() function to avoid variable name conflicts
def main():
    world = World(WORLD_WIDTH, WORLD_HEIGH)

    # Start random population
    init_pop = int(world.size * START_POPULATION)
    for n in range(init_pop):
        idx = random.randrange(0,world.size) # In randrange() last value is world_size -1
        #TODO: Check if already used
        world.set(idx, True)

    # Main loop to show the world
    delay = 0.001 * CYCLE_DELAY # Convert mls to sc
    while True:
        call('clear' if os.name == 'posix' else 'cls') # Clear screen
        print(world)
        world.cycle()
        time.sleep(delay)

if __name__ == "__main__":
    main()
        

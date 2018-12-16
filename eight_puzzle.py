import sys
import math
import resource

import numpy as np
from search import Search


class PuzzleBoard:

    def __init__(self, puzzle_state, parent=None, state="Initial"):
        self.parent = parent
        self.children = []
        self.puzzle_state = np.array(puzzle_state)
        self.column_size = int(math.sqrt(len(puzzle_state)))
        self.state = state
        self.depth = 0 if parent is None else parent.depth + 1
        self.cost = self.depth + self.get_manhattan_distance

    def __lt__(self, other):
        if self.cost != other.cost:
            return self.cost < other.cost
        else:
            op = {'Up': 0, 'Down': 1, 'Left': 2, 'Right': 3}
            return op[self.state] < op[other.state]

    @property
    def goal_test(self):
        if np.array_equal(self.puzzle_state, np.arange(9)):
            return True

    @property
    def get_manhattan_distance(self):
        for index, number in enumerate(self.puzzle_state):
            return abs(index / 3 - number / 3) + abs(index % 3 + number % 3)

    def move_up(self, i):
        if i - self.column_size >= 0:
            puzzle_new, parent = self.swap(i, i - 3)
            return PuzzleBoard(puzzle_new, parent, state='Up')

    def move_down(self, i):
        if i + self.column_size <= len(self.puzzle_state) - 1:
            puzzle_new, parent = self.swap(i, i + 3)
            return PuzzleBoard(puzzle_new, parent, state='Down')

    def move_left(self, i):
        if i % self.column_size > 0:
            puzzle_new, parent = self.swap(i, i - 1)
            return PuzzleBoard(puzzle_new, parent, state='Left')

    def move_right(self, i):
        if i % self.column_size < self.column_size - 1:
            puzzle_new, parent = self.swap(i, i + 1)
            return PuzzleBoard(puzzle_new, parent, state='Right')

    def swap(self, index_one, index_two):
        puzzle_new = self.puzzle_state.copy()
        puzzle_new[index_one], puzzle_new[index_two] = puzzle_new[index_two], puzzle_new[index_one]
        return puzzle_new, self

    @property
    def print_puzzle(self):
        m = 0
        while (m < 9):
            print()
            print(str(self.puzzle_state[m]) +
                  ' ' +
                  str(self.puzzle_state[m +
                                        1]) +
                  ' ' +
                  str(self.puzzle_state[m +
                                        2]))
            m += 3
        print()

    @property
    def expand(self):
        x = list(self.puzzle_state).index(0)
        self.children.append(self.move_up(x))
        self.children.append(self.move_down(x))
        self.children.append(self.move_left(x))
        self.children.append(self.move_right(x))
        self.children = list(filter(None, self.children))
        return self.children

    def write_output(self, search_depth, states, max_depth, nodes_expanded):
        with open('output.txt', "w") as file:
            file.write('path_to_goal: ' + str(states) + '\n')
            file.write('cost_of_path: ' + str(len(states)) + '\n')
            file.write('nodes_expanded: ' + str(nodes_expanded) + '\n')
            file.write('search_depth: ' + str(search_depth) + '\n')
            file.write('max_search_depth: ' + str(max_depth) + '\n')
            file.write('running_time: ' +
                       str(resource.getrusage(resource.RUSAGE_SELF).ru_utime +
                           resource.getrusage(resource.RUSAGE_SELF).ru_stime) +
                       '\n')
            file.write('max_ram_usage: ' +
                       str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss /
                           1024))


def main():
    puzzle_state = sys.argv[2].split(",")
    puzzle_state = list(map(int, puzzle_state))
    pb = PuzzleBoard(puzzle_state)
    if sys.argv[1].lower() == 'bfs':
        search_depth, states, max_depth, nodes_expanded = Search().bfs(pb)
    elif sys.argv[1].lower() == 'dfs':
        search_depth, states, max_depth, nodes_expanded = Search().dfs(pb)
    elif sys.argv[1].lower() == 'ast':
        search_depth, states, max_depth, nodes_expanded = Search().ast(pb)
    else:
        print("Please, check the arguments!")

    pb.write_output(search_depth, states[::-1], max_depth, nodes_expanded)


if __name__ == '__main__':
    main()

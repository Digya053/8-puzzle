import sys
import math
import numpy as np
import resource
from search import Search


class PuzzleBoard:

    def __init__(self, puzzle_state, parent=None, state="Initial"):
        self.parent = parent
        self.children = []
        self.puzzle_state = np.array(puzzle_state)
        self.column_size = int(math.sqrt(len(puzzle_state)))
        self.state = state

    def goal_test(self):
        if np.array_equal(self.puzzle_state, np.arange(9)):
            return True

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

    def expand(self):
        x = list(self.puzzle_state).index(0)
        self.children.append(self.move_up(x))
        self.children.append(self.move_down(x))
        self.children.append(self.move_left(x))
        self.children.append(self.move_right(x))
        self.children = list(filter(None, self.children))
        return self.children

    def write_output(self, search_depth, states):
        with open('output.txt', "w") as file:
            file.write('path_to_goal: ' + str(states) + '\n')
            file.write('cost_of_path: ' + str(len(states)) + '\n')
            file.write('search_depth: ' + str(search_depth) + '\n')
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
        search_depth, states = Search().bfs(pb)
    elif sys.argv[1].lower() == 'dfs':
        search_depth, states = Search().dfs(pb)
    else:
        print("Please, check the arguments!")

    pb.write_output(search_depth, states[::-1])


if __name__ == '__main__':
    main()

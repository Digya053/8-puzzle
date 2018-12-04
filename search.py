from collections import deque

class Search:

    def __init__(self):
        self.path_to_solution = []
        self.states = []

    def bfs(self, puzzle_board):
        frontier = deque()
        explored = set()
        frontier.append(puzzle_board)

        while frontier:
            puzzle = frontier.popleft()
            explored.add(tuple(puzzle.puzzle_state))

            if puzzle.goal_test():
                self.path_to_solution = []
                self.path_trace(self.path_to_solution, puzzle)
                return len(self.path_to_solution), self.states

            children = puzzle.expand()

            for c in range(len(children)):
                if children[c] not in frontier and tuple(
                        children[c].puzzle_state) not in explored:
                    frontier.append(children[c])

    def dfs(self, puzzle_board):
        frontier = []
        explored = set()
        frontier.append(puzzle_board)

        while frontier:
            puzzle = frontier.pop()
            explored.add(tuple(puzzle.puzzle_state))

            if puzzle.goal_test():
                self.path_to_solution = []
                self.path_trace(self.path_to_solution, puzzle)
                return len(self.path_to_solution), self.states

            children = puzzle.expand()

            for c in range(len(children))[::-1]:
                if children[c] not in frontier and tuple(
                        children[c].puzzle_state) not in explored:
                    frontier.append(children[c])

    def path_trace(self, path_to_solution, child):
        print("Tracing path...")
        while child.parent:
            parent = child.parent
            child.print_puzzle()
            self.states.append(child.state)
            path_to_solution.append(child)
            child = parent

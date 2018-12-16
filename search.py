import numpy as np

import heapq
from queue import PriorityQueue
from collections import deque


class Search:

    def __init__(self):
        self.path_to_solution = []
        self.states = []
        self.max_search_depth = 0
        self.nodes_expanded = 0

    def bfs(self, puzzle_board):
        frontier = deque()
        explored = set()
        frontier.append(puzzle_board)

        while frontier:
            puzzle = frontier.popleft()
            explored.add(tuple(puzzle.puzzle_state))

            if puzzle.goal_test:
                self.path_to_solution = []
                self.path_trace(self.path_to_solution, puzzle)
                return len(
                    self.path_to_solution), self.states, self.max_search_depth, self.nodes_expanded

            self.nodes_expanded += 1

            children = puzzle.expand

            for c in children:
                if tuple(c.puzzle_state) not in explored:
                    frontier.append(c)
                    explored.add(tuple(c.puzzle_state))
                    self.max_search_depth = max(self.max_search_depth, c.depth)

    def dfs(self, puzzle_board):
        frontier = []
        explored = set()
        frontier.append(puzzle_board)

        while frontier:
            puzzle = frontier.pop()
            explored.add(tuple(puzzle.puzzle_state))

            if puzzle.goal_test:
                self.path_to_solution = []
                self.path_trace(self.path_to_solution, puzzle)
                return len(
                    self.path_to_solution), self.states, self.max_search_depth, self.nodes_expanded

            self.nodes_expanded += 1

            children = puzzle.expand

            for c in children[::-1]:
                if tuple(c.puzzle_state) not in explored:
                    frontier.append(c)
                    explored.add(tuple(c.puzzle_state))
                    self.max_search_depth = max(self.max_search_depth, c.depth)

    def ast(self, puzzle_board):
        frontier = []
        explored = set()
        heapq.heappush(frontier, puzzle_board)

        while frontier:
            puzzle = heapq.heappop(frontier)
            explored.add(tuple(puzzle.puzzle_state))

            if puzzle.goal_test:
                self.path_to_solution = []
                self.path_trace(self.path_to_solution, puzzle)
                return len(
                    self.path_to_solution), self.states, self.max_search_depth, self.nodes_expanded

            self.nodes_expanded += 1

            children = puzzle.expand

            for c in children:
                if tuple(c.puzzle_state) not in explored:
                    heapq.heappush(frontier, c)
                    explored.add(tuple(c.puzzle_state))
                    self.max_search_depth = max(self.max_search_depth, c.depth)

    def path_trace(self, path_to_solution, child):
        print("Tracing path...")
        child.print_puzzle
        while child.parent:
            parent = child.parent
            self.states.append(child.state)
            path_to_solution.append(child)
            child = parent
            child.print_puzzle

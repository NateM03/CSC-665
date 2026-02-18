# ============================================================
# Solvers — Backtracking (two different implementations)
#           Placeholder for BFS, DFS
# Authors: S. El Alaoui and ChatGPT 5
# ============================================================

import math
from collections import deque
import time

from the3jugs import *

"""
Depth-first backtracking with simple 'explored' pruning.
Stores the best (lowest-cost) path of states encountered to any goal.
This is a recursive implementation. 

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored 
        
"""
class BacktrackingSearch:
    def __init__(self, problem: SearchProblem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def recurse(self, state, path, cost: int):
        if self.problem.is_end(state):
       
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_path = path[:]  # copy
                # print(self.best_cost)
            return

        for action in self.problem.actions(state):
            next_state = self.problem.succ(state, action)
            key = str(next_state)
            # key = next_state
            if key not in self.explored:
                
                self.explored.add(key)
                
                self.recurse(next_state, path + [next_state], cost + self.problem.cost(state, action))

    def solve(self):
        start = self.problem.start_state()
        self.explored.add(str(start))
        self.recurse(start, [], 0)
        return dict(
            best_cost=self.best_cost,
            best_path=[self.problem.start_state()] + (self.best_path or []),
            found=(self.best_path is not None),
            expanded=len(self.explored),
        )

"""
Depth-first backtracking with simple 'explored' pruning (iterative).
Stores the best (lowest-cost) path of states encountered to any goal.
This is an iterative implementation. 

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored

"""
class BacktrackingSearchIterative:
    def __init__(self, problem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        start_key = str(start)
        self.explored.add(start_key)

        # Stack holds tuples: (state, path_from_after_start, cost_so_far)
        stack = [(start, [], 0)]

        while stack:
            state, path, cost = stack.pop()

            # Goal check
            if self.problem.is_end(state):
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_path = path[:]  # copy
                continue

            # Expand
            actions = list(self.problem.actions(state))
            # To match recursive DFS order, push in reverse so first action is explored first.
            for action in reversed(actions):
                next_state = self.problem.succ(state, action)
                key = str(next_state)
                if key not in self.explored:
                    self.explored.add(key)
                    next_cost = cost + self.problem.cost(state, action)
                    stack.append((next_state, path + [next_state], next_cost))

        return dict(
            best_cost=self.best_cost,
            best_path=[self.problem.start_state()] + (self.best_path or []),
            found=(self.best_path is not None),
            expanded=len(self.explored),
        )


"""
Add an iterative implementation of DFS.
BFS explores nodes level by leveland is guaranteed to find a goal at minimum depth (the fewest steps).

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored
"""
# ========== IMPLEMENTED: Part 1, Question 2(a) + Part 3, Question 1 (metrics tracking) ==========
class BFSSearch:
    def __init__(self, problem: SearchProblem):
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        explored = set()
        queue = deque([(start, [], 0)])  # (state, path_from_start, depth)
        explored.add(str(start))
        
        # MODIFIED: Added metrics tracking for Part 3
        total_branches = 0
        nodes_expanded = 0
        max_depth = 0
        solution_depth = None
        
        while queue:
            state, path, depth = queue.popleft()
            max_depth = max(max_depth, depth)  # Track maximum depth explored
            
            # Goal check
            if self.problem.is_end(state):
                solution_depth = depth  # Track solution depth
                # Calculate average branching factor
                avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
                return dict(
                    best_cost=len(path),
                    best_path=[start] + path,
                    found=True,
                    expanded=len(explored),
                    # MODIFIED: Added metrics for Part 3 analysis
                    branching_factor=avg_branching,
                    max_depth=max_depth,
                    solution_depth=solution_depth,
                )
            
            # Expand current state
            actions = list(self.problem.actions(state))
            nodes_expanded += 1  # Track nodes expanded
            total_branches += len(actions)  # Track total branches
            
            for action in actions:
                next_state = self.problem.succ(state, action)
                next_key = str(next_state)
                
                if next_key not in explored:
                    explored.add(next_key)
                    queue.append((next_state, path + [next_state], depth + 1))
        
        # No solution found
        avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
        return dict(
            best_cost=math.inf,
            best_path=None,
            found=False,
            expanded=len(explored),
            # MODIFIED: Added metrics even when no solution found
            branching_factor=avg_branching,
            max_depth=max_depth,
            solution_depth=None,
        )

"""
Add an iterative implementation of DFS.
DFS explores along a path as deep as possible before backtracking 
and returns the first solution found, which may not be the shortest.

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored
"""
# ========== IMPLEMENTED: Part 1, Question 2(b) + Part 3, Question 1 (metrics tracking) ==========
class DFSSearch:
    def __init__(self, problem: SearchProblem):
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        explored = set()
        stack = [(start, [], 0)]  # (state, path_from_start, depth)
        explored.add(str(start))
        
        # MODIFIED: Added metrics tracking for Part 3
        total_branches = 0
        nodes_expanded = 0
        max_depth = 0
        solution_depth = None
        
        while stack:
            state, path, depth = stack.pop()
            max_depth = max(max_depth, depth)  # Track maximum depth explored
            
            # Goal check
            if self.problem.is_end(state):
                solution_depth = depth  # Track solution depth
                # Calculate average branching factor
                avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
                return dict(
                    best_cost=len(path),
                    best_path=[start] + path,
                    found=True,
                    expanded=len(explored),
                    # MODIFIED: Added metrics for Part 3 analysis
                    branching_factor=avg_branching,
                    max_depth=max_depth,
                    solution_depth=solution_depth,
                )
            
            # Expand current state (push in reverse order to explore first action first)
            actions = list(self.problem.actions(state))
            nodes_expanded += 1  # Track nodes expanded
            total_branches += len(actions)  # Track total branches
            
            for action in reversed(actions):
                next_state = self.problem.succ(state, action)
                next_key = str(next_state)
                
                if next_key not in explored:
                    explored.add(next_key)
                    stack.append((next_state, path + [next_state], depth + 1))
        
        # No solution found
        avg_branching = total_branches / nodes_expanded if nodes_expanded > 0 else 0
        return dict(
            best_cost=math.inf,
            best_path=None,
            found=False,
            expanded=len(explored),
            # MODIFIED: Added metrics even when no solution found
            branching_factor=avg_branching,
            max_depth=max_depth,
            solution_depth=None,
        )




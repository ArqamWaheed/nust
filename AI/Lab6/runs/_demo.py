import sys
sys.path.insert(0, "/home/arqamwd/nust/AI/Lab6/pacman_project")
import os
os.chdir("/home/arqamwd/nust/AI/Lab6/pacman_project")
import pacman, layout
from searchAgents import PositionSearchProblem

lay = layout.getLayout("tinyMaze")
state = pacman.GameState()
state.initialize(lay, 0)
problem = PositionSearchProblem(state)

print("type(problem)      :", type(problem).__name__)
print()
print("problem.goal       :", problem.goal, "  <- type:", type(problem.goal).__name__)
print("problem.startState :", problem.startState)
print("problem.walls      :", type(problem.walls).__name__, "(grid of True/False)")
print()
s = problem.getStartState()
print("getStartState()    :", s, "  <- a plain (x, y) tuple")
print("isGoalState(s)     :", problem.isGoalState(s))
print("isGoalState(goal)  :", problem.isGoalState(problem.goal))
print()
print("getSuccessors(s)   :")
for succ in problem.getSuccessors(s):
    print("                    ", succ)

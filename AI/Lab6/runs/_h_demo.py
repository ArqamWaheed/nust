import sys, os
sys.path.insert(0, "/home/arqamwd/nust/AI/Lab6/pacman_project")
os.chdir("/home/arqamwd/nust/AI/Lab6/pacman_project")
import pacman, layout
from searchAgents import PositionSearchProblem, manhattanHeuristic, studentEuclideanHeuristic

lay = layout.getLayout("tinyMaze")
state = pacman.GameState()
state.initialize(lay, 0)
problem = PositionSearchProblem(state)

print("goal is at", problem.goal, "\n")
print(f"{'square':<10}{'manhattan h':>13}{'euclidean h':>14}")
for sq in [(5, 5), (5, 4), (4, 5), (3, 3), (1, 2), (1, 1)]:
    print(f"{str(sq):<10}{manhattanHeuristic(sq, problem):>13}"
          f"{studentEuclideanHeuristic(sq, problem):>14.2f}")

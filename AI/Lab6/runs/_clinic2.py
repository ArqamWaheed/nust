import sys
sys.path.insert(0, "/home/arqamwd/nust/AI/Lab6/pacman_project")
import inspect, searchAgents
with open("runs/clinic_inspect_man.txt", "w") as f:
    f.write(inspect.getsource(searchAgents.manhattanHeuristic) + "\n")

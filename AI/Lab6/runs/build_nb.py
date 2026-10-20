import json, os

BASE = "/home/arqamwd/nust/AI/Lab6"
RUNS = os.path.join(BASE, "runs")
PROJ = os.path.join(BASE, "pacman_project")

def out(name):
    with open(os.path.join(RUNS, name)) as f:
        text = f.read()
    return "".join(l for l in text.splitlines(True) if not l.startswith("### "))

def src(path, start, end=None):
    with open(os.path.join(PROJ, path)) as f:
        text = f.read()
    i = text.index(start)
    j = text.index(end, i) if end else len(text)
    return text[i:j].rstrip()

cells = []

def md(text):
    cells.append({"cell_type": "markdown", "metadata": {},
                  "source": text.strip("\n").splitlines(True)})

def code(text, output=None):
    outputs = []
    if output:
        outputs.append({"output_type": "stream", "name": "stdout",
                        "text": output.splitlines(True)})
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {},
                  "source": text.strip("\n").splitlines(True), "outputs": outputs})

md("""
# CS-272 Artificial Intelligence: Lab 6
### Informed Search - Greedy Best-First Search and Heuristics

**Name:** Arqam Waheed
**Enrollment No.:** 553514
**Class:** BSDS 2K25
**Lab:** 06
""")

md("## Part A - Upload and Run the Lab 5 Project")
code("""
from google.colab import files

uploaded = files.upload()
""")
code("""
import os, zipfile

zip_name = next(name for name in uploaded if name.endswith(".zip"))
extract_root = "/content/lab06_pacman"

with zipfile.ZipFile(zip_name, "r") as z:
    z.extractall(extract_root)

project_dir = None
for root, dirs, filenames in os.walk(extract_root):
    if "pacman.py" in filenames and "search.py" in filenames:
        project_dir = root
        break

assert project_dir is not None, "Pac-Man project folder was not found."
os.chdir(project_dir)
print("Project folder:", project_dir)
""")
code("""
!pwd
!ls
""")
md("**Checkpoint A** - sanity check before editing any file.")
code("!python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch -t --frameTime 0",
     out("tiny_sanity.txt"))

md("""
## Part B - Priority Queue and Heuristic Values

Smallest priority is removed first.
""")
code("""
import util

pq = util.PriorityQueue()

pq.push("A", 7)
pq.push("B", 2)
pq.push("C", 5)

print("First removed:", pq.pop())
print("Second removed:", pq.pop())
""", out("clinic_pq.txt"))
md("""
For Greedy Best-First Search the priority is the heuristic value:

```
priority = h(n)

smaller h(n)  -> estimated closer to goal
larger h(n)   -> estimated farther from goal
```

Manhattan: `h(n) = |x1 - x2| + |y1 - y2|`
""")
code("""
current = (2, 3)
goal = (5, 7)

manhattan = abs(current[0] - goal[0]) + abs(current[1] - goal[1])
print("Manhattan h(n):", manhattan)
""", out("clinic_man.txt"))
md("Euclidean: `h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)`")
code("""
current = (2, 3)
goal = (5, 7)

euclidean = (
    (current[0] - goal[0]) ** 2
    + (current[1] - goal[1]) ** 2
) ** 0.5

print("Euclidean h(n):", euclidean)
""", out("clinic_euc.txt"))
md("""
| Feature | Manhattan | Euclidean |
|---|---|---|
| Meaning | horizontal + vertical distance | straight-line distance |
| Natural fit | four-direction grid movement | continuous / diagonal movement |
| Value from (2,3) to (5,7) | 7 | 5.0 |
""")

md("## Part C - Existing Heuristic Interface")
code("""
import searchAgents
import inspect

print(inspect.getsource(searchAgents.manhattanHeuristic))
""", out("clinic_inspect_man.txt"))

md("""
## Activity 1 - Student Euclidean Heuristic (02 Marks)

Added in `searchAgents.py` below the existing heuristic functions.
""")
code(src("searchAgents.py", "def studentEuclideanHeuristic", "#####"))
code("!python -m py_compile searchAgents.py")

md("""
## Activity 2 - Greedy Best-First Search (04 Marks)

Added in `search.py` below `nullHeuristic()`.

```python
""" + src("search.py", "def greedyBestFirstSearch", "def aStarSearch") + """
```

Registered at the bottom of `search.py`:

```python
greedy = greedyBestFirstSearch
```
""")
code("""
!python -m py_compile search.py
!python -m py_compile searchAgents.py
""")

md("""
## Part E - Run Greedy Search

tinyMaze with Manhattan. Legend: `%` = wall, `.` = goal, `< > ^ v` = Pac-Man.
""")
code("!python pacman.py -l tinyMaze -p SearchAgent -a fn=greedy,heuristic=manhattanHeuristic -t --frameTime 0",
     out("tiny_greedy_man.txt"))
md("mediumMaze with Manhattan.")
code("!python pacman.py -l mediumMaze -p SearchAgent -a fn=greedy,heuristic=manhattanHeuristic -q",
     out("med_greedy_man.txt"))
md("mediumMaze with the student Euclidean heuristic.")
code("!python pacman.py -l mediumMaze -p SearchAgent -a fn=greedy,heuristic=studentEuclideanHeuristic -q",
     out("med_greedy_euc.txt"))

md("""
## Activity 3 - Compare Heuristics and Search Behavior (04 Marks)

Greedy Best-First Search on mediumMaze:

| Heuristic | Nodes Expanded | Solution Length / Cost | Reached Goal? | Observation |
|---|---|---|---|---|
| Manhattan | 78 | 74 | Yes | |
| Student Euclidean | 159 | 152 | Yes | |

Greedy vs BFS on mediumMaze (BFS numbers recorded in Lab 5):

| Algorithm | Information Used | Nodes Expanded | Solution Length / Cost | Optimal Here? |
|---|---|---|---|---|
| BFS | No heuristic | 269 | 68 | |
| Greedy (Manhattan) | h(n) | 78 | 74 | |

### Analysis Questions

1. What information does h(n) provide that DFS/BFS did not use?
2. Why does Greedy choose the state with the smallest h(n)?
3. Which heuristic expanded fewer nodes in your mediumMaze run? Support the answer with your table.
4. Did the heuristic that expanded fewer nodes also produce the shorter path? Explain using your results.
5. Why is Greedy Best-First Search not guaranteed to be optimal even when h(n) appears to point toward the goal?
6. State one practical advantage and one limitation of Greedy search.
7. In one sentence, explain why A* will need more than h(n) alone.
""")

md("""
## Extension Task - Uniform Cost Search (Optional / Not Graded)

```
UCS priority    = g(n) = actual path cost from Start to n
Greedy priority = h(n) = estimated remaining cost from n to Goal
```

The `uniformCostSearch(problem)` stub in `search.py` was completed.

```python
""" + src("search.py", "def uniformCostSearch", "def nullHeuristic") + """
```

The alias `ucs = uniformCostSearch` was already present.
""")
code("!python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs -q", out("med_ucs.txt"))
md("""
| Algorithm | Priority Rule | Nodes Expanded | Path Cost | Solution Length | Optimal? |
|---|---|---|---|---|---|
| UCS | g(n) | 269 | 68 | 68 | Yes, for non-negative step costs |
| Greedy | h(n) | 78 | 74 | 74 | Not guaranteed |

### Short Analysis

1. UCS and Greedy both use a Priority Queue. What exactly is different about their priority values?
2. Which algorithm expanded fewer nodes in your mediumMaze experiment?
3. Did the algorithm that expanded fewer nodes also return the lower-cost path?
4. Why can UCS guarantee the least-cost solution with non-negative step costs while Greedy cannot?
5. Which algorithm uses information about the goal location?
""")

md("## Download")
code("""
from google.colab import files

files.download("search.py")
files.download("searchAgents.py")
""")

md("""
## Reflection

What changed when search became informed? Which heuristic would you choose for this Pac-Man
movement model, and why?
""")

nb = {
    "cells": cells,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py", "mimetype": "text/x-python", "name": "python",
            "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.10.12"
        }
    },
    "nbformat": 4, "nbformat_minor": 5
}

dest = os.path.join(BASE, "553514_ArqamWaheed_Lab06_Greedy.ipynb")
with open(dest, "w") as f:
    json.dump(nb, f, indent=1)
print("wrote", dest, "cells:", len(cells))

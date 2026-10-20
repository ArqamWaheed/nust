import sys, os
sys.path.insert(0, "/home/arqamwd/nust/AI/Lab6/report")
from render import render, code, out

RUNS = "/home/arqamwd/nust/AI/Lab6/runs"
PROJ = "/home/arqamwd/nust/AI/Lab6/pacman_project"


def runout(name, keep=None):
    with open(os.path.join(RUNS, name)) as f:
        lines = [l.rstrip("\n") for l in f if not l.startswith("### ")]
    return lines if keep is None else lines[:keep]


def filesrc(path, start, end=None):
    with open(os.path.join(PROJ, path)) as f:
        text = f.read()
    i = text.index(start)
    j = text.index(end, i) if end else len(text)
    return text[i:j].rstrip().split("\n")


# ---------- Part A ----------
render("a1_setup", [code(
    "from google.colab import files",
    "",
    "uploaded = files.upload()",
    label="In [1]:",
), code(
    "import os, zipfile",
    "",
    'zip_name = next(name for name in uploaded if name.endswith(".zip"))',
    'extract_root = "/content/lab06_pacman"',
    "",
    'with zipfile.ZipFile(zip_name, "r") as z:',
    "    z.extractall(extract_root)",
    "",
    "project_dir = None",
    "for root, dirs, filenames in os.walk(extract_root):",
    '    if "pacman.py" in filenames and "search.py" in filenames:',
    "        project_dir = root",
    "        break",
    "",
    'assert project_dir is not None, "Pac-Man project folder was not found."',
    "os.chdir(project_dir)",
    'print("Project folder:", project_dir)',
    label="In [2]:",
), code(
    "!pwd",
    "!ls",
    label="In [3]:",
)])

tiny_sanity = runout("tiny_sanity.txt")
render("a2_sanity", [code(
    "!python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch -t --frameTime 0",
    label="In [4]:",
), out(*(tiny_sanity[:13] + ["..."] + tiny_sanity[-5:]))])

# ---------- Part B ----------
render("b1_pq", [code(
    "import util",
    "",
    "pq = util.PriorityQueue()",
    "",
    'pq.push("A", 7)',
    'pq.push("B", 2)',
    'pq.push("C", 5)',
    "",
    'print("First removed:", pq.pop())',
    'print("Second removed:", pq.pop())',
    label="In [5]:",
), out(*runout("clinic_pq.txt"))])

render("b2_heuristics", [code(
    "current = (2, 3)",
    "goal = (5, 7)",
    "",
    "manhattan = abs(current[0] - goal[0]) + abs(current[1] - goal[1])",
    'print("Manhattan h(n):", manhattan)',
    label="In [6]:",
), out(*runout("clinic_man.txt")), code(
    "current = (2, 3)",
    "goal = (5, 7)",
    "",
    "euclidean = (",
    "    (current[0] - goal[0]) ** 2",
    "    + (current[1] - goal[1]) ** 2",
    ") ** 0.5",
    "",
    'print("Euclidean h(n):", euclidean)',
    label="In [7]:",
), out(*runout("clinic_euc.txt"))])

# ---------- Part C ----------
render("c1_inspect", [code(
    "import searchAgents",
    "import inspect",
    "",
    "print(inspect.getsource(searchAgents.manhattanHeuristic))",
    label="In [8]:",
), out(*runout("clinic_inspect_man.txt"))])

# ---------- Activity 1 ----------
render("d1_heuristic", [code(
    *filesrc("searchAgents.py", "def studentEuclideanHeuristic", "#####"),
    label="In [9]:",
)])

render("d2_compile", [code(
    "!python -m py_compile searchAgents.py",
    label="In [10]:",
)])

# ---------- Activity 2 ----------
render("e1_greedy", [code(
    *filesrc("search.py", "def greedyBestFirstSearch", "def aStarSearch"),
    label="In [11]:",
)])

render("e2_alias", [code(
    "# Abbreviations",
    "bfs = breadthFirstSearch",
    "dfs = depthFirstSearch",
    "astar = aStarSearch",
    "ucs = uniformCostSearch",
    "greedy = greedyBestFirstSearch",
    label="In [12]:",
), code(
    "!python -m py_compile search.py",
    "!python -m py_compile searchAgents.py",
    label="In [13]:",
)])

# ---------- Part E ----------
tiny_greedy = runout("tiny_greedy_man.txt")
render("f1_tiny_greedy", [code(
    "!python pacman.py -l tinyMaze -p SearchAgent \\",
    "-a fn=greedy,heuristic=manhattanHeuristic -t --frameTime 0",
    label="In [14]:",
), out(*(tiny_greedy[:13] + ["..."] + tiny_greedy[-5:]))])

render("f2_med_manhattan", [code(
    "!python pacman.py -l mediumMaze -p SearchAgent \\",
    "-a fn=greedy,heuristic=manhattanHeuristic -q",
    label="In [15]:",
), out(*runout("med_greedy_man.txt"))])

render("f3_med_euclidean", [code(
    "!python pacman.py -l mediumMaze -p SearchAgent \\",
    "-a fn=greedy,heuristic=studentEuclideanHeuristic -q",
    label="In [16]:",
), out(*runout("med_greedy_euc.txt"))])

# ---------- Extension ----------
render("g1_ucs_code", [code(
    *filesrc("search.py", "def uniformCostSearch", "def nullHeuristic"),
    label="In [17]:",
)])

render("g2_ucs_run", [code(
    "!python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs -q",
    label="In [18]:",
), out(*runout("med_ucs.txt"))])

# ---------- Download ----------
render("h1_download", [code(
    "from google.colab import files",
    "",
    'files.download("search.py")',
    'files.download("searchAgents.py")',
    label="In [19]:",
)])

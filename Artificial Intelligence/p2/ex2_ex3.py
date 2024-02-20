import queue

walls = set()
goals = set()
crates = set()
legalSpots = set()
illegalSpots = set()
warehouseman = (-1, -1)
any_goals_on_the_edges = [False, False, False, False] # lewo, gora, prawo, dol

def load_data():
    global warehouseman, any_goals_on_the_edges, cols, rows
    data = open('zad_input.txt', 'r').read().strip().split('\n')
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == 'W': walls.add((x, y))
            elif data[y][x] == '.': legalSpots.add((x, y))
            elif data[y][x] == 'G':
                legalSpots.add((x, y))
                goals.add((x, y))
            elif data[y][x] == 'B':
                legalSpots.add((x, y))
                crates.add((x, y))
            elif data[y][x] == 'K':
                warehouseman = (x, y)
                legalSpots.add((x, y))
            elif data[y][x] == '*':
                legalSpots.add((x, y))
                goals.add((x, y))
                crates.add((x, y))
            elif data[y][x] == '*':
                legalSpots.add((x, y))
                goals.add((x, y))
                warehouseman = (x, y)
    for goal in goals:
        if goal[0] == 1: any_goals_on_the_edges[0] = True
        elif goal[0] == len(data[0]) - 1: any_goals_on_the_edges[2] = True
        if goal[1] == 1: any_goals_on_the_edges[1] = True
        elif goal[1] == len(data) - 1: any_goals_on_the_edges[3] = True
    rows = len(data)
    cols = len(data[0])

def actions():
    return ['L', 'U', 'R', 'D']

def terminal(crates_pos):
    for crate in crates_pos:
        if crate not in goals: return False
    return True

def result(warehouseman, crates_pos, action):
    if action == 'L':
        warehouseman = (warehouseman[0] - 1, warehouseman[1])
        if warehouseman in crates_pos:
            crates_pos.remove(warehouseman)
            crates_pos.add((warehouseman[0] - 1, warehouseman[1]))
    elif action == 'U':
        warehouseman = (warehouseman[0], warehouseman[1] - 1)
        if warehouseman in crates_pos:
            crates_pos.remove(warehouseman)
            crates_pos.add((warehouseman[0], warehouseman[1] - 1))
    elif action == 'R':
        warehouseman = (warehouseman[0] + 1, warehouseman[1])
        if warehouseman in crates_pos:
            crates_pos.remove(warehouseman)
            crates_pos.add((warehouseman[0] + 1, warehouseman[1]))
    elif action == 'D':
        warehouseman = (warehouseman[0], warehouseman[1] + 1)
        if warehouseman in crates_pos:
            crates_pos.remove(warehouseman)
            crates_pos.add((warehouseman[0], warehouseman[1] + 1))
    return warehouseman, crates_pos

def find_illegal_pos():
    to_make_illegal = set()

    for pos in legalSpots:
        if pos not in goals:
            illigal_dirs = list()

            for a in actions():
                if a == 'L':
                    new_pos = (pos[0] - 1, pos[1])
                    if new_pos in walls: illigal_dirs.append(a)
                elif a =='U':
                    new_pos = (pos[0], pos[1] - 1)
                    if new_pos in walls: illigal_dirs.append(a)
                elif a == 'R':
                    new_pos = (pos[0] + 1, pos[1])
                    if new_pos in walls: illigal_dirs.append(a)
                elif a == 'D':
                    new_pos = (pos[0], pos[1] + 1)
                    if new_pos in walls: illigal_dirs.append(a)

            if len(illigal_dirs) == 3: to_make_illegal.add(pos)
            elif len(illigal_dirs) == 2: # rog mapy
                if 'L' in illigal_dirs or 'R' in illigal_dirs:
                    if 'U' in illigal_dirs or 'D' in illigal_dirs:
                        to_make_illegal.add(pos)

    for pos in to_make_illegal:
        legalSpots.remove(pos)
        illegalSpots.add(pos)

def is_state_legal(warehouseman_pos, crates_pos, action):
    if action == 'L':
        pos = (warehouseman_pos[0] - 1, warehouseman_pos[1])
        sec_pos = (pos[0] - 1, pos[1])
    elif action == 'U':
        pos = (warehouseman_pos[0], warehouseman_pos[1] - 1)
        sec_pos = (pos[0], pos[1] - 1)
    elif action == 'R':
        pos = (warehouseman_pos[0] + 1, warehouseman_pos[1])
        sec_pos = (pos[0] + 1, pos[1])
    elif action == 'D':
        pos = (warehouseman_pos[0], warehouseman_pos[1] + 1)
        sec_pos = (pos[0], pos[1] + 1)

    if pos in walls: return False

    if pos in crates_pos and sec_pos in crates_pos: return False

    if pos in crates_pos and sec_pos in walls: return False

    if pos in crates_pos and sec_pos in illegalSpots: return False
    # lewo gora prawo dol
    if (pos in crates_pos) and ((sec_pos[0] == 1 and not any_goals_on_the_edges[0]) or (sec_pos[0] == cols - 1 and not any_goals_on_the_edges[2]) or (sec_pos[1] == 1 and not any_goals_on_the_edges[1]) or (sec_pos[1] == rows - 1 and not any_goals_on_the_edges[3])):
        return False
    return True

def BFS():
    q = queue.Queue()
    visited = set()
    sequence = list()
    q.put((warehouseman, crates, sequence))
    visited.add(str((warehouseman, crates))) # str

    while not q.empty():
        cur = q.get()
        warehouseman_pos = cur[0]
        crates_pos = cur[1]
        seq = list(cur[2])

        if terminal(crates_pos):
            write_data = open('zad_output.txt', 'w')
            write_data.write(''.join(seq))
            write_data.close()
            break

        for a in actions():
            if is_state_legal(warehouseman_pos, crates_pos, a):
                new_state = result(warehouseman_pos, crates_pos.copy(), a)
                if str(new_state) not in visited:
                    visited.add(str(new_state))
                    q.put((new_state[0], new_state[1], seq + [a]))

load_data()
find_illegal_pos()
BFS()

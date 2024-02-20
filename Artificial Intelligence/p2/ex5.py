from queue import PriorityQueue

walls = set()
positions_left = set()
goals = set()

def load_data():
    data = open('zad_input.txt', 'r').read().split('\n')[:-1]
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == '#': walls.add((x, y))
            elif data[y][x] == 'S': positions_left.add((x, y))
            elif data[y][x] == 'G': goals.add((x, y))
            elif data[y][x] == 'B':
                goals.add((x, y))
                positions_left.add((x, y))

def actions():
    return ['L', 'U', 'R', 'D']

def result(state, action):
    res = set()
    if action == 'L':
        for pos in state:
            x = pos[0] - 1
            y = pos[1]
            if (x, y) not in walls: res.add((x, y))
            else: res.add(pos)
    elif action == 'U':
        for pos in state:
            x = pos[0]
            y = pos[1] - 1
            if (x, y) not in walls: res.add((x, y))
            else: res.add(pos)
    elif action == 'R':
        for pos in state:
            x = pos[0] + 1
            y = pos[1]
            if (x, y) not in walls: res.add((x, y))
            else: res.add(pos)
    else:
        for pos in state:
            x = pos[0]
            y = pos[1] + 1
            if (x, y) not in walls: res.add((x, y))
            else: res.add(pos)
    return res

def terminal(state):
    for posn in state:
        if posn not in goals: return False
    return True

def heuristic(new_state, dest):
    res = max(new_state, key=lambda x: abs(x[0] - dest[0]) + abs(x[1] - dest[1]))
    return abs(res[0] - dest[0]) + abs(res[1] - dest[1])

def find_the_nearest_dest(state):
    the_neares_dest = ()
    distance = 9999
    for goal in goals:
        temp_max_distance = -1
        for posn in state:
            temp_distance = abs(posn[0] - goal[0]) + abs(posn[1] - goal[1])
            if temp_distance > temp_max_distance: temp_max_distance = temp_distance
        if temp_max_distance < distance:
            distance = temp_max_distance
            the_neares_dest = goal
    return the_neares_dest

def a_star_search(state):
    q = PriorityQueue()
    seq = list()
    visited = set()
    q.put((0, state, seq))
    visited.add(str(state))
    amount = len(state)

    dest = find_the_nearest_dest(state)

    while not q.empty():
        _, current, seq = q.get()

        if terminal(current):
            write_data = open('zad_output.txt', 'w')
            write_data.write(''.join(seq))
            write_data.close()
            break

        for a in actions():
            new_state = result(current, a)


            if str(new_state) not in visited:   
                visited.add(str(new_state))
                priority = heuristic(new_state, dest) + len(seq) # !!!
                q.put((priority, new_state, seq + [a]))



load_data()
a_star_search(positions_left)
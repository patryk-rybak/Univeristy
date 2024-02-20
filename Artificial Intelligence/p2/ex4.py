import queue

walls = set()
positions_left = set()
goals = set()

def load_data():
    data = open('zad_input.txt', 'r').read().split()
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
    for pos in state:
        if pos not in goals: return False
    return True

def does_basic_sequence(state):
    for i in range(18): state = result(state, 'L')
    for i in range(18): state = result(state, 'U')
    for i in range(18): state = result(state, 'R')
    for i in range(18): state = result(state, 'D')
    return state, list('L' * 18 + 'U' * 18 + 'R' * 18 + 'D' * 18)

def BFS(state, seq):
    q = queue.Queue()
    visited = set()
    q.put((state, seq))
    visited.add(str(state))
    amount = len(state)

    while not q.empty():
        state, seq = q.get()

        if terminal(state):
            write_data = open('zad_output.txt', 'w')
            write_data.write(''.join(seq))
            write_data.close()
            #print(len(seq))
            break

        for a in actions():
            new_state = result(state, a)
            if str(new_state) not in visited:
                if len(new_state) < amount:
                    visited = set()
                    q = queue.Queue()
                    amount = len(new_state)
                visited.add(str(new_state))
                q.put((new_state, seq + [a]))

load_data()
positions_left, sequence = does_basic_sequence(positions_left)
#print(positions_left)
BFS(positions_left, sequence)
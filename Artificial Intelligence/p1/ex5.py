import random

def is_col_ok(col_index, cols, img): # ok
    col = [img[i][col_index] for i in range(len(img))]
    counter = 0
    for i in col:
        if i == '#': counter += 1
    if counter != cols[col_index]: return False
    for i in range(col.index('#'), col.index('#') + cols[col_index]):
        if col[i] != '#': return False
    return True

def select_opt_col(row_index, cols, img): # ok
    row = img[row_index]
    stats = []
    for i in range(len(row)):
        before = is_col_ok(i, cols, img)
        if row[i] == '.': row[i] = '#'
        else: row[i] = '.'
        after = is_col_ok(i, cols, img)
        if row[i] == '.': row[i] = '#'
        else: row[i] = '.'
        stats.append((before, after))
    if (False, True) in stats: return stats.index((False, True))
    if (False, False) in stats:
        temp = [i if stats[i] == (False, False) else -1 for i in range(len(stats))]
        temp= list(filter(lambda x: x != -1, temp))
        return random.choice(temp)
    else: return stats.index((True, False))  

def is_row_ok(row_index, rows, img): # ok
    row = img[row_index]
    counter = 0
    for i in row:
        if i == '#': counter += 1
    if counter != rows[row_index]: return False
    if counter == 0 and rows[row_index] == 0: return True
    for i in range(row.index('#'), row.index('#') + rows[row_index]):
        if row[i] != '#': return False
    return True

def select_opt_row(col_index, rows, img): # ok
    stats = []
    for i in range(len(img)):
        before = is_row_ok(i, rows, img)
        if img[i][col_index] == '#': img[i][col_index] = '.'
        else: img[i][col_index] = '#'
        after = is_row_ok(i, rows, img)
        if img[i][col_index] == '#': img[i][col_index] = '.'
        else: img[i][col_index] = '#'
        stats.append((before, after))
    if (False, True) in stats: return stats.index((False, True))
    if (False, False) in stats:
        temp = [i if stats[i] == (False, False) else -1 for i in range(len(stats))]
        temp= list(filter(lambda x: x != -1, temp))
        return random.choice(temp)
    else: return stats.index((True, False))
    
def select_anything(rows, cols, img): # ok
    bad_anything = []
    for i in range(len(img)):
        if not is_row_ok(i, rows, img):
            bad_anything.append(('r', i))
    for i in range(len(img[0])):
        if not is_col_ok(i, cols, img): bad_anything.append(('c', i))
    if len(bad_anything) == 0: return False
    return random.choice(bad_anything)

def solve(rows, cols):
    img = [['.' for i in range(len(cols))] for j in range(len(rows))]
    anything = select_anything(rows, cols, img)
    timer = 0
    while type(anything) != bool and timer < 2 * pow(10, 3):
        destroy_row = random.choices([True, False], weights=(1, 5), k=1)[0]
        if destroy_row:
            good_rows = []
            for i in range(len(img)):
                if is_row_ok(i, rows, img): good_rows.append(i)
            if len(good_rows) == 0: row = random.choice([i for i in range(len(img))])
            else: row = random.choice(good_rows)
            col = select_opt_col(row, cols, img)
        else:
            if anything[0] == 'r':
                row = anything[1]
                optimal = random.choices([True, False], weights=(6, 1), k=1)[0]
                col = select_opt_col(row, cols, img) if optimal else random.choice([i for i in range(len(cols))])
            else:
                col = anything[1]
                row = select_opt_row(col, rows, img)

        if img[row][col] == '.': img[row][col] = '#'
        else: img[row][col] = '.'
        anything = select_anything(rows, cols, img)
        timer += 1
    if timer >= 2 * pow(10, 3): return False
    return img


with open('zad_input.txt', 'r') as IN, open('zad_output.txt', 'w') as OUT:
    lines = IN.readlines()
    n = int(lines[0].split(' ')[0])
    m = int(lines[0].split(' ')[1][:-1])
    r = []
    c = []
    for i in range(1, len(lines) - m):
        r.append(int(lines[i][:-1]))
    for i in range(len(lines) - m, len(lines)):
        c.append(int(lines[i][:-1]))
    res = solve(r, c)
    while res == False:
        res = solve(r, c)
    OUT.writelines((''.join(i) + '\n' for i in res))

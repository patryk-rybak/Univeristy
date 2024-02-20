from itertools import combinations

def create_possibilities(n_empty, n_groups, groups):
    # tworze wszsytkie mozliwosc wiersza lub kolumny n_empty - liczba pustych miejsc w pasku, n_groups - liczba grup, groups - opis grup np. [2, 3]

    def is_ok(c):
        # sprawdza czy skladowe blokow sa ulozone jeden po drugim
        for i in range(1, len(c)):
            if c[i] - c[i - 1] == 1: return False
        return True
    
    def normalize(c, groups, length):
        # wypelniam bloki jedynkami
        res = []
        start = 0
        for i in range(len(c)):
            while start < c[i]:
                res.append(0)
                start += 1
            res = res + [1]*groups[i]   
            start = c[i] + 1
        while length > len(res):
            res.append(0)
        return res

    length = n_empty + sum(groups)
    res = []
    for c in combinations(range(n_empty + n_groups), n_groups):
        if is_ok(c):
            res.append(normalize(c, groups, length))
    return res

with open('zad_input.txt', 'r') as IN:
        n_rows, n_cols = IN.readline().strip().split()
        n_rows = int(n_rows)
        n_cols = int(n_cols)

        gr_rows = []
        gr_cols = []
        for i in range(n_rows):
            gr_rows.append(list(map(lambda x: int(x), IN.readline().strip().split())))
        for i in range(n_cols):
            gr_cols.append(list(map(lambda x: int(x), IN.readline().strip().split())))

def create_vars(n_rows, n_cols, gr_rows, gr_cols):
    # tworzy zmienne razem z dziedzinami vars[0] to wiersze, vars[1] to klumny
    vars = [[], []]
    for r in range(n_rows):
        vars[0].append(create_possibilities(n_cols - sum(gr_rows[r]), len(gr_rows[r]), gr_rows[r]))
    for c in range(n_cols):
        vars[1].append(create_possibilities(n_rows - sum(gr_cols[c]), len(gr_cols[c]), gr_cols[c]))
    return vars

vars = create_vars(n_rows, n_cols, gr_rows, gr_cols)

def is_solved(vars): # [[rows_domains][cols_domains]]
    # sprawdza czy dziedziny sa jednoelementowe
    rows = vars[0]
    cols = vars[1]
    for r in rows:
        if len(r) != 1: return False
    for c in cols:
        if len(c) != 1: return False
    return True

def find_black_common(domain):
    # szuka zamalowanej czesci wspolnej 
    res = [1 for i in range(len(domain[0]))]
    for d in domain:
        for i in range(len(res)):
            res[i] = res[i] and d[i]
    return res

def find_white_common(domain):
    # szuka niezamalowanej czesci wspolnej
    res = [0 for i in range(len(domain[0]))]
    for d in domain:
        for i in range(len(res)):
            res[i] = res[i] or d[i]
    return res

def reduce_domain(color, orientation, index, common, vars): # 0 - wgite, 1 - black | 0 - col, 1 - row | 
    # color - podajesz czy czesc wspolna jest biala czy czarna, orientation - czy czesc wspolna jest z wierszy czy z kolumn, index - na ktorym indeksie czesc wspolna byla szukana, vars - wszsytkie zmienne razem z dziedzinami

    # ogarnac to ladniej
    if color == 1 and orientation == 1:
        for i in range(len(common)):
            temp = []
            if common[i] == 1:
                for j in range(len(vars[1][i])):
                    if vars[1][i][j][index] == 0:
                        continue
                    temp.append(vars[1][i][j])
                vars[1][i] = temp
    elif color == 1:
        for i in range(len(common)):
            temp = []
            if common[i] == 1:
                for j in range(len(vars[0][i])):
                    if vars[0][i][j][index] == 0:
                        continue
                    temp.append(vars[0][i][j])
                vars[0][i] = temp
    elif orientation == 1:
        for i in range(len(common)):
            temp = []
            if common[i] == 0:
                for j in range(len(vars[1][i])):
                    if vars[1][i][j][index] == 1:
                        continue
                    temp.append(vars[1][i][j])
                vars[1][i] = temp
    else:
        for i in range(len(common)):
            temp = []
            if common[i] == 0:
                for j in range(len(vars[0][i])):
                    if vars[0][i][j][index] == 1:
                        continue
                    temp.append(vars[0][i][j])
                vars[0][i] = temp


def solve(vars):
    # dopokoi dzidziny nie sa jednoelementowe przejdz po wszystkich wierszach, wyznacz czesci wspolne i na ich podstawie usun nie pasujace element z dziedzin kolumn zrob to samo przechodzac po kolumnach i zmniejszacac dziedziny wierszy
    
    #for i in vars: print(i)
    while not is_solved(vars):
        for r in range(n_rows):
            #print(r)
            #for k in vars: print(k)
            black_common = find_black_common(vars[0][r])
            white_common = find_white_common(vars[0][r])
            #print('black_common=', black_common)
            #print('white_common=', white_common)
            for i in range(len(black_common)):
                if black_common[i] == 1: reduce_domain(1, 1, r, black_common, vars)
            #print('po usunieciu czarnych')
            #for k in vars: print(k)
            for i in range(len(black_common)):
                if white_common[i] == 0: reduce_domain(0, 1, r, white_common, vars)
            #print('po usuniecu bilaych')
            #for k in vars: print(k)

        for c in range(n_cols):
            black_common = find_black_common(vars[1][c])
            white_common = find_white_common(vars[1][c])
            for i in range(len(black_common)):
                if black_common[i] == 1: reduce_domain(1, 0, c, black_common, vars)
                if white_common[i] == 0: reduce_domain(0, 0, c, white_common, vars)

solve(vars)
with open('zad_output.txt', 'w') as OUT:
    for i in vars[0]:
        s = ''
        for j in i[0]:
            if j == 1: s = s + '#'
            else: s = s + '.'
        s = s + '\n'
        OUT.write(s)
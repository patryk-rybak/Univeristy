from itertools import combinations
import copy

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

    # calo funkcji
    length = n_empty + sum(groups)
    res = []
    for c in combinations(range(n_empty + n_groups), n_groups):
        if is_ok(c):
            res.append(normalize(c, groups, length))
    return res

def create_vars(n_rows, n_cols, gr_rows, gr_cols):
    # tworzy zmienne razem z dziedzinami vars[0] to wiersze, vars[1] to klumny
    all_gr_rows = []
    all_gr_cols = []
    for r in range(n_rows):
        all_gr_rows.append(create_possibilities(n_cols - sum(gr_rows[r]), len(gr_rows[r]), gr_rows[r]))
    for c in range(n_cols):
        all_gr_cols.append(create_possibilities(n_rows - sum(gr_cols[c]), len(gr_cols[c]), gr_cols[c]))
    return all_gr_rows, all_gr_cols

def load_data():
    global n_rows, n_cols, gr_rows, gr_cols
    data = open('zad_input.txt', 'r').read().strip().split("\n")
    n_rows, n_cols = data[0].split(' ')
    n_rows = int(n_rows)
    n_cols = int(n_cols)
    gr_rows = []
    gr_cols = []
    for i in range(1, n_rows + 1): gr_rows.append(list(map(int, data[i].split(' '))))
    for j in range(n_rows + 1, n_rows + 1 + n_cols): gr_cols.append(list(map(int, data[j].split(' '))))
    #data.close()

def inference(solutions, field, val, is_cols=False):
    if is_cols: return [col for col in solutions[field[0]] if col[field[1]] == val]
    else: return [row for row in solutions[field[1]] if row[field[0]] == val]

def reduce(field, rows_domain, cols_domain):
    elem = rows_domain[field[1]][0][field[0]]
    possibilities = len(rows_domain[field[1]])

    if all(rows_domain[field[1]][k][field[0]] == elem for k in range(possibilities)):
        cols_domain[field[0]] = inference(cols_domain, field, elem, True)
        return True
    
    elem = cols_domain[field[0]][0][field[1]]
    possibilities = len(cols_domain[field[0]])

    if all(cols_domain[field[0]][k][field[1]] == elem for k in range(possibilities)):
        rows_domain[field[1]] = inference(rows_domain, field, elem, False)
        return True
    
    return False

def no_solution(rows_domains, cols_domains):
    for domain in rows_domains:
        if not domain: return True
    for domain in cols_domains:
        if not domain: return True
    return False 

def find_new_unassigned_fields(rows_domain_l, cols_domain_l, unassigned_fields):
    while True:
        exit_loop = True
        new_unassigned_fields = list()
        for i in range(len(unassigned_fields)):
            field = unassigned_fields[i]

            if reduce(field, rows_domain_l, cols_domain_l):
                exit_loop = False

                if not rows_domain_l[field[1]]:
                    return False, []
                if not cols_domain_l[field[0]]:
                    return False, []
            else:
                new_unassigned_fields.append(field)

        unassigned_fields = new_unassigned_fields

        if exit_loop:
            return True, new_unassigned_fields 

def backtracking(rows_domains, cols_domains, unassigned_fields):
    
    if no_solution(rows_domains, cols_domains): return -1

    res, new_unassigned_fields = find_new_unassigned_fields(rows_domains, cols_domains, unassigned_fields)

    if not res: return -1
    # if no_solution(rows_domains, cols_domains): return -1

    if new_unassigned_fields:

        field = new_unassigned_fields[0]
        new_unassigned_fields = new_unassigned_fields[1::]

        inferences_rows_true = copy.deepcopy(rows_domains)
        inferences_cols_true = copy.deepcopy(cols_domains)
        inferences_rows_false = copy.deepcopy(rows_domains)
        inferences_cols_false = copy.deepcopy(cols_domains)

        # zakladamy, ze wybrany pixel powinien byc zamalowany
        inferences_rows_true[field[1]] = inference(rows_domains, field, 1, False)
        inferences_cols_true[field[0]] = inference(cols_domains, field, 1, True)

        backtracking(inferences_rows_true, inferences_cols_true, new_unassigned_fields.copy())

        # juz wiemy, ze powinien byc niezamalowany
        inferences_rows_false[field[1]] = inference(rows_domains, field, 0, False)
        inferences_cols_false[field[0]] = inference(cols_domains, field, 0, True)

        backtracking(inferences_rows_false, inferences_cols_false, new_unassigned_fields.copy())
    
    else:
        write_data = open('zad_output.txt', 'w')
        s = ''
        for i in rows_domains:
            for j in i[0]:
                if j == 1: s += '#'
                else: s += '.'
            s += '\n'
        write_data.write(s)
        write_data.close()
        quit()   

load_data()

rows_domains, cols_domains = create_vars(n_rows, n_cols, gr_rows, gr_cols)

unassigned_fields = list()
for y in range(n_rows):
        for x in range(n_cols):
            if not reduce((x, y), rows_domains, cols_domains):
                unassigned_fields.append((x, y))

backtracking(rows_domains, cols_domains, unassigned_fields)
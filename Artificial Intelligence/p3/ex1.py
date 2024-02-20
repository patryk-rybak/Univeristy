inputPath = "zad_input.txt"
outputPath = "zad_output.txt"

from itertools import combinations

rows = 0 # ilosc wierszy
cols = 0 # ilosc kolumn
row_blocks = [] # ilosc i dlugosc blokow w poszczegolnych wierszach
column_blocks = [] # ilosc i dlugosc blokow w poszczegolnych kolumnach
row_perms = [] # mozliwe wypelnienia kazdego rzedu
col_perms = [] # mozliwe wypelnienia kazdej kolumny

# tlumaczy specyfikacje w postaci napisu liczb na tablice liczb, np. '3 2' -> [3, 2]
def StrToIntList(s):
    xs = s.split(" ") # rozbicie napisu na liste liczb w postaci napisowej
    xs = [int(elem) for elem in xs] # konwersja liczb napisowych na inty
    return xs

# wczytuje dane na temat ilosci kolumn, wierszy i wypelnionych pol
def load():
    global rows, cols, row_blocks, column_blocks, row_perms
    
    #global row_filledIntervals, column_filledIntervals, row_forbidden, column_forbidden
    input = open(inputPath, "r").read().strip().split("\n")
    x = input[0].split(" ")
    rows = eval(x[0])
    cols = eval(x[1])
    for rowSpec in input[1:rows+1]: # dla kazdej linii specyfikacji blokow wierszow
        row_blocks.append(StrToIntList(rowSpec))
    for colSpec in input[rows+1:]: # dla kazdej linii specyfikacji blokow kolumn
        column_blocks.append(StrToIntList(colSpec))

# wypisz w konsoli rozwiazanie
def draw():
    with open(outputPath, 'w') as file:
        for i in row_perms:
            s = ''
            for j in i[0]:
                if j == 1: 
                    s = s + '#'
                else: 
                    s = s + '.'
            s = s + '\n'
            file.write(s)

def init_perms():
    # tworzy mozliwe permutacje kazdego wiersza i kolumny
    global row_blocks, col_perms
    for r in range(rows):
        possibilities = create_possibilities(cols - sum(row_blocks[r]), row_blocks[r])
        row_perms.append(possibilities)
    for c in range(cols):
        possibilities = create_possibilities(rows - sum(column_blocks[c]), column_blocks[c])
        col_perms.append(possibilities)

def are_blocks_separated(start_indexes):
    """ sprawdza, czy kolejne bloki sa ulozone jeden po drugim
        :param start_indexes: lista  """
    for i in range(1, len(start_indexes)):
        if start_indexes[i] - start_indexes[i - 1] == 1: 
            return False
    return True

def is_solved():
    """ sprawdza, czy w kazdym rzedzie istnieje tylko 1 mozliwe rozwiazanie """
    for r in row_perms:
        if len(r) != 1: 
            return False
    for c in col_perms:
        if len(c) != 1: 
            return False
    return True

def create_possibilities(empty_count, blocks):
    """ tworze wszsytkie mozliwosc wiersza lub kolumny 
        :param empty_count: liczba pustych miejsc w pasku
        :param blocks: opis blokow np. [2, 3] """
    
    blocks_count = len(blocks) # ilosc blokow
    length = empty_count + sum(blocks) # minimalna odleglosc od poczatku 1 bloku do konca ostatniego
    res = []
    for empty_spaces in combinations(range(empty_count + blocks_count), blocks_count):
        if are_blocks_separated(empty_spaces):
            res.append(normalize(empty_spaces, blocks, length))
    return res

def find_filled_common(perms):
    """ zwraca permutacje, w ktorej pola oznaczone 1 sa pewne do zamalowania
        :param perms: lista wszystkich mozliwych permutacji paska """
    common_perm = [1 for _ in range(len(perms[0]))]
    for p in perms:
        for i in range(len(common_perm)):
            common_perm[i] = common_perm[i] and p[i]
    return common_perm

def find_empty_common(perms):
    """ zwraca permutacje, w ktorej pola oznaczone 0 na pewno nie sa zamalowane
        :param perms: lista wszystkich mozliwych permutacji paska """
    common_perm = [0 for _ in range(len(perms[0]))]
    for p in perms:
        for i in range(len(common_perm)):
            common_perm[i] = common_perm[i] or p[i]
    return common_perm

def normalize(start_indexes, blocks, length):
    """ tworzy mozliwe rozwiazanie paska
        :param start_indexes: lista poczatkow kolejnych blokow
        :param blocks: lista blokow w pasku
        :param length: odleglosc od poczatku 1 bloku do konca ostatniego
        :return: mozliwe rozwiazanie paska """
    perm = [] # mozliwe ustawienie w danym pasku
    start = 0

    # dla kazdego bloku w pasku
    for i in range(len(start_indexes)):
        # wypelnij zerami pierwszych start pol
        while start < start_indexes[i]:
            perm.append(0)
            start += 1

        # wypelnij jedynkami kolejne n pol
        perm = perm + [1]*blocks[i]   
        start = start_indexes[i] + 1
    
    # wypelnij zerami pozostale pola na koncu
    while length > len(perm):
        perm.append(0)
    return perm

def reduce_row_domain(type, index, common_perm): 
    """ zmniejsza ilosc potencjalnych rozwiazan
        :param type: typ czesci wspolnej: 0 - empty, 1 - filled
        :param index: na ktorym indeksie czesc wspolna byla szukana 
        :param common_perm: permutacja zawierajaca informacje o czesci wspolnej """

    for col in range(cols): # dla kazdej kolumny
        temp = []
        if common_perm[col] == type: # jesli kolumna nalezy do czesci wspolnej
            for j in range(len(col_perms[col])): # dla kazdego wiersza w tej kolumnie
                if col_perms[col][j][index] == type: # jesli tez nalezy do czesci wspolnej
                    temp.append(col_perms[col][j])
            col_perms[col] = temp # zaktualizuj czesc wspolna tej kolumny

def reduce_column_domain(type, index, common_perm): 
    """ zmniejsza ilosc potencjalnych rozwiazan
        :param type: typ czesci wspolnej: 0 - empty, 1 - filled
        :param index: na ktorym indeksie czesc wspolna byla szukana 
        :param common_perm: permutacja zawierajaca informacje o czesci wspolnej """

    for row in range(rows): # dla kazdego wiersza
        temp = []
        if common_perm[row] == type: # jesli wiersz nalezy do czesci wspolnej
            for j in range(len(row_perms[row])): # dla kazdej kolumny w tym wierszu
                if row_perms[row][j][index] == type: # jesli tez nalezy do czesci wspolnej
                    temp.append(row_perms[row][j])
            row_perms[row] = temp # zaktualizuj czesc wspolna tego wiersza

def solve():
    """ eliminuj potencjalne rozwiazania do momentu gdy kazdy 
        wiersz/kolumna ma jednoznaczne rozwiazanie """
    while not is_solved():
        # dla kazdego wiersza, zaktualizuj jego liste potencjalnych rozwiazan
        for r in range(rows):
            filled_common = find_filled_common(row_perms[r])
            empty_common = find_empty_common(row_perms[r])
            for i in range(len(filled_common)):
                if filled_common[i] == 1: 
                    reduce_row_domain(1, r, filled_common)
            for i in range(len(filled_common)):
                if empty_common[i] == 0: 
                    reduce_row_domain(0, r, empty_common)
        
        # dla kazdej kolumny, zaktualizuj jej liste potencjalnych rozwiazan
        for c in range(cols):
            filled_common = find_filled_common(col_perms[c])
            empty_common = find_empty_common(col_perms[c])
            for i in range(len(filled_common)):
                if filled_common[i] == 1: 
                    reduce_column_domain(1, c, filled_common)
                if empty_common[i] == 0: 
                    reduce_column_domain(0, c, empty_common)

load() # zaladuj dane z pliku
init_perms() # znajdz wszystkie mozliwe rozwiazania w kazdym wierszu/kolumnie
solve() # znajdz poprawne rozwiazanie
draw() # wypisz do pliku poprawne rozwiazanie

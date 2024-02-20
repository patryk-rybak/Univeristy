import random

def is_straight_flush(deck):
    if not deck[0][1] == deck[1][1] == deck[2][1] == deck[3][1] == deck[4][1]: return False
    temp = [i[0] for i in deck]
    temp.sort()
    for i in range(len(temp) - 1):
        if temp[i + 1] - temp[i] != 1:
            return False
    return True

def is_four(deck):
    for i in range(2):
        counter = 0
        for j in deck:
            if deck[i][0] == j[0]:
                counter += 1
        if counter == 4:
            return True
    return False

def is_full(deck):
    temp = []
    for i in deck:
        if i[0] in temp:
            continue
        temp.append(i[0])
    return len(temp) == 2

def is_flush(deck):
    return deck[0][1] == deck[1][1] == deck[2][1] == deck[3][1] == deck[4][1]

def is_straight(deck):
    temp = [i[0] for i in deck]
    temp.sort()
    for i in range(len(temp) - 1):
        if temp[i + 1] - temp[i] != 1:
            return False
    return True

def is_three(deck):
    counter = {}
    for i in deck:
        if i[0] in counter: counter[i[0]] += 1
        else: counter[i[0]] = 1
    return 3 in counter.values()

def is_two_pair(deck):
    temp = [i[0] for i in deck]
    counter = {}
    for i in temp:
        if i in counter:
            counter[i] += 1
        else:
            counter[i] = 1
    return len(counter) == 3

def is_blotkarz_winning(blot, figu):
    if is_straight_flush(blot): return True
    elif is_four(figu): return False
    elif is_four(blot): return True
    elif is_full(figu): return False
    elif is_full(blot): return True
    elif is_flush(blot): return True
    elif is_straight(blot): return True
    elif is_three(figu): return False
    elif is_three(blot): return True
    elif is_two_pair(figu): return False
    elif is_two_pair(blot): return True # NIZEJ ODPOWIEDNIO PAIR I HIGH CARD
    else: return False

def hand_generator(deck):
    temp = [i for i in deck]
    hand = []
    for i in range(5):
        card = random.choice(temp)
        hand.append(card)
        temp.remove(card)
    return hand

def find_ppb(trials, blotkarz_deck, figurant_deck):
    counter = 0
    for i in range(trials):
        blotkarz_hand = hand_generator(blotkarz_deck)
        figurant_hand = hand_generator(figurant_deck)
        if is_blotkarz_winning(blotkarz_hand, figurant_hand): counter += 1
    return (counter / trials) * 100

def tests():
    figu_deck = [(i, j) for i in range(10, 14) for j in range(1, 5)]
    
    blot_decl = [(i, j) for i in range(1, 10) for j in range(1, 4)]
    print('bez jednego koloru')
    print('ppb: ', find_ppb(pow(10, 5), blot_decl, figu_deck))
    print()

    blot_decl = [(i, j) for i in range(3, 10) for j in range(1, 4)]
    print('bez 2 i 3 kazdego koloru')
    print('ppb: ', find_ppb(pow(10, 5), blot_decl, figu_deck))
    print()

    blot_decl = [(i, j) for i in range(4, 10) for j in range(1, 4)]
    print('bez 2, 3 i 4 kazdego koloru')
    print('ppb: ', find_ppb(pow(10, 5), blot_decl, figu_deck))
    print()

    blot_decl = [(i, j) for i in range(5, 10) for j in range(1, 4)]
    print('bez 2, 3, 4 i 5 kazdego koloru')
    print('ppb: ', find_ppb(pow(10, 5), blot_decl, figu_deck))
    print()
    
    blot_decl = [(i, j) for i in range(7, 10) for j in range(1, 4)]
    print('bez 2, 3, 4, 5, 6 i 7 kazdego koloru')
    print('ppb: ', find_ppb(pow(10, 5), blot_decl, figu_deck))
    print()


blotkarz_deck = [(i, j) for i in range(1, 10) for j in range(1, 5)]
figurant_deck = [(i, j) for i in range(10, 14) for j in range(1, 5)]

print('ppb dla danych z polecenia: ', find_ppb(pow(10, 5), blotkarz_deck, figurant_deck))





# ['straight flush', 'four', 'full', 'flush', 'straight', 'three', 'two pair', 'pair', 'high card']
'''
from math import comb

blot_var = [5 * 4, 9 * 32, 9 * comb(4, 3) * 8 * comb(4, 2), 4 * comb(9, 5) - 5 * 4, 5 * pow(4, 5) - 4 * 5, 9 * comb(
    4, 3) * comb(8, 2) * pow(4, 2), comb(9, 2) * comb(4, 2) * comb(4, 2) * 7 * 4, 9 * comb(4, 2) * comb(8, 3) * pow(4, 3)]
blot_var.append((36 * 7 * 17 * 11 * 8) -
                         sum(i for i in blot_var))
figu_var = [0, 4 * 12, 4 * comb(4, 3) * 3 * comb(4, 2), 0, 0, 4 * comb(4, 3) * comb(
    3, 2) * pow(4, 2), comb(4, 2) * comb(4, 2) * comb(4, 2) * 2 * 4, 4 * comb(4, 2) * pow(4, 3), 0]

print(blot_var)
print(figu_var)
'''
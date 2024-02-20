def solve(line, words):
    sums = [0 for i in range(len(line) + 1)]
    res = ["" for i in range(len(line) + 1)]
    for i in range(1, len(line) + 1):
        len_pow_2 = 0
        for j in range(i):
            if (line[j:i] in words) and (len_pow_2 < sums[j] + pow((i - j), 2)):
                len_pow_2 = sums[j] + pow((i - j), 2)
                res[i] = res[j] + " " + line[j:i]
        sums[i] = len_pow_2
    return res[sums.index(max(sums))][1:]

with open('zad_input.txt', encoding='utf-8') as IN, open('zad_output.txt', 'w', encoding='utf-8') as OUT, open('ex2_words.txt', encoding='utf-8') as W:
    words = set(line[:-1] for line in W)
    res = ''
    for line in IN:
        res = res + solve(line[:-1], words) + '\n'
    OUT.write(res)

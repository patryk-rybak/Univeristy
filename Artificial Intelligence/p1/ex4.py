def opt_dist(s, D):
    if D > len(s) : return float('+inf')
    l = 0
    mid = D
    r = 0
    for i in range(D):
        if s[i] == '1':
            mid -= 1
    for i in range(D, len(s)):
        if s[i] == '1':
            r += 1
    res = l + mid + r
    for i in range(1, len(s) - D + 1):
        if s[i - 1] == '1':
            l += 1
        if s[i - 1 + D] == '1':
            r -= 1
        if s[i - 1] == '0' and s[i - 1 + D] == '1':
            mid -= 1
        elif s[i - 1] == '1' and s[i - 1 + D] == '0':
            mid += 1
        temp = l + mid + r
        if temp < res: res = temp

    return res

with open('zad_input.txt', 'r') as IN, open('zad_output.txt', 'w') as OUT:
    line = IN.readlines()
    res = []
    for args in line:
        args = args.split()
        res.append(str(opt_dist(args[0], int(args[1]))) + '\n')
    OUT.writelines(res)
    

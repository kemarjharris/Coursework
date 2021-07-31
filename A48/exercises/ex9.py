def radix_sort(L):
    return radix_succ(L)


def radix_succ(L, bigdig=0):
    radict = {}
    for i in range(10):
        radict[i] = []
    # biggest digit
    for x in range(len(L)):
        (col, dig) = (10**(bigdig + 1), 10**bigdig)
    # puts all the things in their correct dictionary spot
        radict[(L[x] % col)//dig].append(L[x])
        newlist = []
        # put them in their correct order
        for a in range(10):
            newlist += radict[a]
    if newlist != L:
        result = radix_succ(newlist, bigdig + 1)
    else:
        result = newlist
    return result

def greeting(name):
    '''(str) -> str
    A function that takes in a string as a name, and puts the
    name in the greeting: Hello <name> how are you today?
    >>> greeting("Sarah")
    'Hello Sarah how are you today?'
    >>> greeting('5')
    'Hello 5 how are you today?'
    '''
    return ('Hello ' + name + ' how are you today?')


def mutate_list(list1):
    '''(list) -> Nonetype
    A function that takes a list and mutates it in the following ways:
    Iff the element is an integer, it is doubled.
    Iff the element is a boolean, it is inverted.
    Iff the element is a string, it is replaced with its first
    and last letters removed.
    Regardless of the type, the first element is changed to
    the string "Hello".
    REQ: the list has at least one element in it.
    REQ: if the list has a string in it, the string is at least two characters
    long.
    >>> list1 = [True, True, False]
    >>> mutate_list(list1)
    >>> list1 == ['Hello', False, True]
    True
    >>> list1 = ['I THINK!', 'ab', '!you have a ways to go!', 'hey there']
    >>> mutate_list(list1)
    >>> list1 == ['Hello', '', '!ou have a ways to g!', 'ey ther']
    True
    >>> list1 = [1, 27, 42, 'buh buh buh, buh buh BOO la buh buh buh']
    >>> mutate_list(list1)
    >>> list1 == ['Hello', 54, 84, 'uh buh buh, buh buh BOO la buh buh bu']
    True
    >>> list1 = [True, True, 7, 'tru']
    >>> mutate_list(list1)
    >>> list1 == ['Hello', False, 14, 'r']
    True
    '''
    for i in range(len(list1)):
        # if its an integer, double it
        if (type(list1[i]) == int):
            list1[i] = (2*(list1[i]))
        # if its a boolean, invert it
        elif (type(list1[i]) is bool):
            list1[i] = not(list1[i])
        # if its a string, run safe_string
        elif (type(list1[i]) == str):
            list1[i] = safe_string(list1[i])
    list1[0] = 'Hello'
    # workin on  the fucction to get remove the first and last letter out of
    # a string. You were setting the boolean flags s_let and e_let, end letter
    # and start letter, and were gonna turn them to true afte riterating
    # through the string and finding the first and last letter. After that, you
    # were gonna return the string with the letters at e_let and s_let removed.


def safe_string(strin):
    '''(str) -> str
    Takes a string and removes first and last letters.
    Note: #!@%#$%&^*^)1234567890,;/'[L:{:
    etc, etc, aren't letters.
    REQ: strin has at least two characters in it.
    >>> safe_string('!!hi!!')
    '!!!!'
    >>> safe_string('!!!!!!yrankly!!!!!')
    '!!!!!!rankl!!!!!'
    >>> safe_string('frankly')
    'rankl'
    >>> safe_string('hih')
    'i'
    >>> safe_string('!!!!!!yrankl')
    '!!!!!!rank'
    >>> safe_string('yrankly!!!!!')
    'rankl!!!!!'
    >>> safe_string('ab')
    ''
    >>> safe_string('buh buh buh buh, buh buh BOO la buh buh buh')
    'uh buh buh buh, buh buh BOO la buh buh bu'
    >>> safe_string('hey there')
    'ey ther'
    >>> safe_string('!you have a ways to go!')
    '!ou have a ways to g!'
    '''
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    s_let = False
    e_let = False
    i = 0
    while s_let is False:
        if strin[i] in alpha:
            s_spot = i
            s_let = True
        i += 1
    # strin = strin.replace(strin[s_spot], '', 1)
    i = -1
    while e_let is False:
        if strin[i] in alpha:
            e_spot = i
            e_let = True
        i -= 1
    '''for e in range(len(strin) -1, 0, -1):
        if strin[e] in alpha:
            print(e)
            e_spot = e'''
    sos = strin[:s_spot]
    mos = strin[s_spot + 1:len(strin) + e_spot]
    if (e_spot < -1):
        eos = strin[e_spot + 1:]
        result = sos + mos + eos
    else:
        # eos = strin[e_spot:]
        result = sos + mos
    return result


def merge_dicts(d1, d2):
    # convert d1's dictionary keys to lists and when its in the second dicti,
    # append it.
    # if it isnt, add it to the first dictionary.
    d1k = list(d1.keys())
    for e in d2:
        if (e in d1k):
            d1[e] += d2[e]
        else:
            d1[e] = d2[e]
    return d1

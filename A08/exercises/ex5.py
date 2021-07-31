def copy_me(l):
    '''
    (list) -> list
    Write a function called copy me that takes as input a list, and returns a
    copy of the list with the following changes: Strings have all their letters 
    converted to upper-case, Integers and floats have their value increased by 1
    booleans are negated (False becomes True, True becomes False), and lists are
    replaced with the word ”List”
    REQ: l is a list.

    >>>copy_me(["baka baka ne", 14, True, 17.3, ('magicallu', 'change de')])
    ["BAKA BAKA NE", 15, False, 18.3, ('magicallu', 'change de')]
    >>>copy_me([[tru, to be], ['luv and were'], ['raving on', 12, 'junsha']])
    [List, List, List]
    >>>copy_me([])
    []
       '''
    # create a shallow copy of the list
    l_copy = l[:]
    # iterate through the list
    for i in range(len(l_copy)):
        # check at each value of te list what the type is using is
        # if its an integer or float add one
        if((type(l_copy[i]) is int) or (type(l_copy[i]) is float)):
            l_copy[i] += 1
        # if its a boolean use the is comparison, and negate the value
        elif(type(l_copy[i]) is bool):
            l_copy[i] = not(l_copy[i]) 
        # if its a string go all uppercase method
        elif(type(l_copy[i]) is str):
            l_copy[i] = l_copy[i].upper()
        # if its a list replac eit with the string "List"
        elif(type(l_copy[i]) is list):
            l_copy[i] = 'List'
    # return the copy of the list.
    return l_copy
    

def mutate_me(l_copy):
    '''
    (list) -> list
    Write a function called copy me that takes as input a list, and returns 
    the list with the following changes: Strings have all their letters 
    converted to upper-case, Integers and floats have their value increased by 1
    booleans are negated (False becomes True, True becomes False), and lists are
    replaced with the word ”List”
    REQ: l is a list.

    >>>copy_me(["baka baka ne", 14, True, 17.3, ('magicallu', 'change de')])
    ["BAKA BAKA NE", 15, False, 18.3, ('magicallu', 'change de')]
    >>>copy_me([[tru, to be], ['luv and were'], ['raving on', 12, 'junsha']])
    [List, List, List]
    >>>copy_me([])
    []
       '''
    # iterate through the list
    for i in range(len(l_copy)):
        # check at each value of te list what the type is using is
        # if its an integer or float add one
        if((type(l_copy[i]) is int) or (type(l_copy[i]) is float)):
            l_copy[i] += 1
        # if its a boolean use the is comparison, and negate the value
        elif(type(l_copy[i]) is bool):
            l_copy[i] = not(l_copy[i]) 
        # if its a string go all uppercase method
        elif(type(l_copy[i]) is str):
            l_copy[i] = l_copy[i].upper()
        # if its a list replac eit with the string "List"
        elif(type(l_copy[i]) is list):
            l_copy[i] = 'List'
    # return the copy of the list.
    return l_copy
    

    
    

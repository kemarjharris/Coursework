from container import *


def banana_verify(source, goal, cont, moves):
    '''(str, str, Container, str) -> bool
    A function that verifies if the source word is changed into a given goal
    word via banana game methods. If it was, return true, else return false.
    >>> a = bscont()
    >>> banana_verify('a','a', a, 'she succin')
    False
    '''
    # set a blank variable for building the goal word
    goalu = ''
    # if the operation is P, put the next letter in the container
    for i in range(len(moves)):
        if (moves[i] == 'P'):
            cont.put(source[0])
            source = source[1:]
        # if the operation is get return and remove the item from the container
        elif (moves[i] == 'G'):
            goalu += cont.get()
        # if the operation is move, move the next letter from the source word
        # to the goal word
        elif (moves[i] == 'M'):
            goalu += source[0]
            source = source[1:]
        # return if the goal word and the created word match
    return (goalu == goal)


class bscont:
    # stack
    def __init__(self, cont=[]):
        self._cont = []

    def put(self, o):
        self._cont.append(o)

    def get(self):
        return self._cont.pop()

    def peek(self):
        return self._cont[-1]

    def is_empty(self):
        return(len(self.cont) == 0)

    def succ(self):
        print('she succin')


class bscont2:
    # queue
    def __init__(self, cont=[]):
        self._cont = []

    def put(self, o):
        self._cont.append(o)

    def get(self):
        return self._cont.pop(0)

    def peek(self):
        return self._cont[0]

    def is_empty(self):
        return(len(self.cont) == 0)

    def succ(self):
        print('succinthfuccfucc')

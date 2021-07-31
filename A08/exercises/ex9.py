import math
class Parallelogram():
    '''a class with a unknown angles, side lengths, and theta'''
    def __init__(self, base, side, theta):
        '''initializes parallelogram with base, a side, and a theta. the highest
        in the parent heirarchy.'''
        # initialize base, side, and theta
        self._base = base
        self._side = side
        self._theta = theta

        if self._base < 0:
            self._base = self._base * (-1)
        if self._side < 0:
            self._side = self._side * (-1)
        if self._theta < 0 or self._theta > 180:
            self._theta = (-1) * self._theta

    def __str__(self):
        '''returns what the area is in a string'''
        #assign shape the name of the class
        shape = __class__.__name__
        # my main  problem, where the issue is coming up
        area = __class__.area(self)
        # return the string ' im a shape with a certain area'
        return'I am a ' + shape + ' with area ' + str(area)

    def area(self):
        '''a function that calculates the area of the shape.'''
        # convert self._theta from radians to degrees
        return (self._base) * (self._side) * (math.sin(math.radians(self._theta)))

    def bst(self):
        '''a function that returns base, side, and theta in a list'''
        return [self._base, self._side, self._theta]

class Rectangle(Parallelogram):
    '''a parallelogram with 4 right angles'''
    def __init__(self, base, side, theta = 90):
        Parallelogram.__init__(self, base, side, theta)

    def __str__(self):
            '''returns what the area is in a string'''
            #assign shape the name of the class
            shape = __class__.__name__
            # my main  problem, where the issue is coming up
            area = __class__.area(self)
            # return the string ' im a shape with a certain area'
            return'I am a ' + shape + ' with area ' + str(area)

class Rhombus(Parallelogram):
    '''a parallelogram with 4 equal sides'''
    def __init__(self, base, theta):
        side = base
        Parallelogram.__init__(self, base, side, theta)

    def __str__(self):
            '''returns what the area is in a string'''
            #assign shape the name of the class
            shape = __class__.__name__
            # my main  problem, where the issue is coming up
            area = __class__.area(self)
            # return the string ' im a shape with a certain area'
            return'I am a ' + shape + ' with area ' + str(area)


class Square(Rectangle, Rhombus):
    '''a rectangle and rhombus with 4 equal sides and 4 right angles'''
    def __init__(self, base):
        side = base
        theta = 90
        Rhombus.__init__(self, base, theta)
        Rectangle.__init__(self, base, side)

    def __str__(self):
            '''returns what the area is in a string'''
            #assign shape the name of the class
            shape = __class__.__name__
            # my main  problem, where the issue is coming up
            area = __class__.area(self)
            # return the string ' im a shape with a certain area'
            return'I am a ' + shape + ' with area ' + str(area)
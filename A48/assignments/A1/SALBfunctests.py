from salboard import SALboard
from salbnode import SALBnode
from salbLLfunctions import *
import unittest


#class TestSALfunctions(unittest.TestCase):



#def test_01_ab(self):
    #''' Should be false '''
print('1', end=" ")
n = SALboard(16, {2: 11, 10: 7, 6: 14})
nll = salb2salbLL(n)
print(willfinish(nll, 2))

#def test_02_ab(self):
    #''' Should be false '''
print('2', end=" ")
n = SALboard(16, {2: 11, 10: 7, 6: 14})
nll = salb2salbLL(n)
print(willfinish(nll, 10))

#def test_03_ab(self):
    #''' Should be false '''
print('3', end=" ")
n = SALboard(16, {2: 11, 10: 7, 6: 14})
nll = salb2salbLL(n)
print(willfinish(nll, 7))

#def test_04_ab(self):
    #''' Should be false '''
print('4', end=" ")
n = SALboard(16, {2: 11, 10: 7, 6: 14})
nll = salb2salbLL(n)
print(willfinish(nll, 3))

#def test_05_ab(self):
    #''' Should be True'''
print('5', end=" ")
n = SALboard(16, {2: 11, 10: 7, 6: 14})
nll = salb2salbLL(n)
print(willfinish(nll, 4))

''' My tests '''

#def test_06_ab(self):
 #   ''' Should be false '''
print('6', end=" ")
n = SALboard(8, {6: 2})
nll = salb2salbLL(n)
print(willfinish(nll, 2))

#def test_07_ab(self):
 #   ''' Should be false '''
print('7', end=" ")
n = SALboard(12, {8: 2, 4: 6})
nll = salb2salbLL(n)
print(willfinish(nll, 2))

#def test_08_ab(self):
 #   ''' Should be True '''
print('8', end=" ")
n = SALboard(12, {8: 2, 4: 6})
nll = salb2salbLL(n)
print(willfinish(nll, 3))

#def test_09_ab(self):
 #   ''' # Should be false '''
print('9', end=" ")
n = SALboard(16, {6: 8, 10: 4})
nll = salb2salbLL(n)
print(willfinish(nll, 2))

#def test_10_ab(self):
 #   ''' Should be false '''
print('10', end=" ")
n = SALboard(16, {6: 8, 10: 4})
nll = salb2salbLL(n)
print(willfinish(nll, 6))

#def test_11_ab(self):
 #   ''' LOL '''
print('11', end=" ")
n = SALboard(1, {})
nll = salb2salbLL(n)
print(willfinish(nll, 45))

print('12', end=" ")
# false
n = SALboard(16, {9: 7, 10: 8, 11: 9, 12: 5})
nll = salb2salbLL(n)
print(willfinish(nll, 7))

print('Finish!')
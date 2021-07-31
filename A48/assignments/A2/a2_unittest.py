#from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree
from formula_game_functions import *

import unittest

BUILD_TREE_VERBOSE = 0
DRAW_TREE_VERBOSE = 0

# 13 tests
class TestBuildTree(unittest.TestCase):

    def test_01_only_one_variable(self):
        formula = 'a'
        formula_tree = build_tree(formula)
        result = Leaf('a')

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_02_simple_and(self):
        formula = "(x*y)"
        formula_tree = build_tree(formula)
        result = AndTree(Leaf('x'), Leaf('y'))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_03_simple_or(self):
        formula = "(x+y)"
        formula_tree = build_tree(formula)
        result = OrTree(Leaf('x'), Leaf('y'))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_04_simple_not(self):
        formula = "-x"
        formula_tree = build_tree(formula)
        result = NotTree(Leaf('x'))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_05_not_bracket_not(self):
        formula = "((-x+y)*-(-y+x))"
        formula_tree = build_tree(formula)
        result = AndTree(OrTree(NotTree(Leaf('x')), Leaf('y')),
            NotTree(OrTree(NotTree(Leaf('y')), Leaf('x'))))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_06_start_with_not(self):
        formula = "-((x+y)*-(c*z))"
        formula_tree = build_tree(formula)
        result = NotTree(AndTree(OrTree(Leaf('x'), Leaf('y')),
                NotTree(AndTree(Leaf('c'), Leaf('z')))))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_07_many_connectives(self):
        formula = '(((x+y)*(-x+y))+((a+b)*(-b+a)))'
        formula_tree = build_tree(formula)
        result = OrTree(AndTree(OrTree(Leaf('x'), Leaf('y')),
            OrTree(NotTree(Leaf('x')), Leaf('y'))),
            AndTree(OrTree(Leaf('a'), Leaf('b')),
            OrTree(NotTree(Leaf('b')), Leaf('a'))))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_08_combinations(self):
        formula = '(c+-(-(b+a)+-(-x+-y)))'
        formula_tree = build_tree(formula)
        result = OrTree(Leaf('c'), NotTree(OrTree(NotTree(OrTree(Leaf('b'),
            Leaf('a'))), NotTree(OrTree(NotTree(Leaf('x')),
            NotTree(Leaf('y')))))))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_09_combinations_02(self):
        formula = '((((x+y)+y)+y)*((r*(r+u))*s))'
        formula_tree = build_tree(formula)
        result = AndTree(OrTree(OrTree(OrTree(Leaf('x'), Leaf('y')),
                Leaf('y')), Leaf('y')), AndTree(AndTree(Leaf('r'),
                OrTree(Leaf('r'), Leaf('u'))), Leaf('s')))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_10_combinations_03(self):
        formula = '-((f+(-e*f))*-(e*-c))'
        formula_tree = build_tree(formula)
        result = NotTree(AndTree(OrTree(Leaf('f'), AndTree(NotTree(Leaf('e')),
            Leaf('f'))), NotTree(AndTree(Leaf('e'), NotTree(Leaf('c'))))))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_11_piazza_01(self):
        formula = "((x*y)+(-x*-y))"
        formula_tree = build_tree(formula)
        result = OrTree(AndTree(Leaf('x'), Leaf('y')),
            AndTree(NotTree(Leaf('x')), NotTree(Leaf('y'))))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_12_piazza_02(self):
        formula = '((-x+y)+(-y+x))'
        formula_tree = build_tree(formula)

        result = OrTree(OrTree(NotTree(Leaf('x')), Leaf('y')),
            OrTree(NotTree(Leaf('y')), Leaf('x')))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_13_piazza_03(self):
        formula = '(-((f+(-e*f))*-(e*-c))+(-(f+((a+(e+b))*-b))*(f*a)))'
        formula_tree = build_tree(formula)

        result = OrTree(NotTree(AndTree(OrTree(Leaf('f'),
                    AndTree(NotTree(Leaf('e')), Leaf('f'))),
                    NotTree(AndTree(Leaf('e'), NotTree(Leaf('c')))))),
                    AndTree(NotTree(OrTree(Leaf('f'),
                    AndTree(OrTree(Leaf('a'), OrTree(Leaf('e'),
                    Leaf('b'))), NotTree(Leaf('b'))))),
                    AndTree(Leaf('f'), Leaf('a'))))

        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)


# 11 tests
class TestBuildTreeInvalidFormula(unittest.TestCase):

    def test_01_capital_variable(self):
        formula = 'A'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)


    def test_02_capital_with_and(self):
        formula = '(A*b)'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_03_capital_with_or(self):
        formula = '(a+B)'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_04_invalid_brackets(self):
        formula = '((((a'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_05_invalid_brackets_02(self):
        formula = 'a)))'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_06_extraneous_brackets(self):
        formula = '(a+b))))'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_07_only_brackets(self):
        formula = '()'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)


    def test_08_bracketed_variables(self):
        formula = '(a)'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_09_bracket_negative(self):
        formula = '(-a)'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_10_negative_bracket(self):
        formula = '-(a)'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)

    def test_11_extraneous_brackets_02(self):
        formula = '(-(x+y))'
        formula_tree = build_tree(formula)
        result = None
        if (BUILD_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(formula_tree)

        error_msg = 'output was: ' + str(formula_tree)

        self.assertEqual(formula_tree, result, error_msg)


# 5 tests
class TestDrawFormulaTree(unittest.TestCase):

    def test_01_simple_one_variable(self):
        formula = 'a'
        formula_tree = build_tree(formula)
        str_tree = draw_formula_tree(formula_tree)
        result = 'a'
        if (DRAW_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(str_tree)

        self.assertEqual(str_tree, result)

    def test_02_simple_and(self):
        formula = '(x*y)'
        formula_tree = build_tree(formula)
        str_tree = draw_formula_tree(formula_tree)
        result = '* y\n  x'
        if (DRAW_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(str_tree)

        self.assertEqual(str_tree, result)

    def test_03_simple_or(self):
        formula = '(x+y)'
        formula_tree = build_tree(formula)
        str_tree = draw_formula_tree(formula_tree)
        result = '+ y\n  x'
        if (DRAW_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(str_tree)

        self.assertEqual(str_tree, result)

    def test_04_not(self):
        formula = '(-x+y)'
        formula_tree = build_tree(formula)
        str_tree = draw_formula_tree(formula_tree)
        result = '+ y\n  - x'
        if (DRAW_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(str_tree)

        self.assertEqual(str_tree, result)

    def test_05_not_bracket_not(self):

        formula = "((-x+y)*-(-y+x))"
        formula_tree = build_tree(formula)
        str_tree = draw_formula_tree(formula_tree)
        result = '* - + x\n      - y\n  + y\n    - x'
        if (DRAW_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(str_tree)

        self.assertEqual(str_tree, result)

    def test_06_(self):
        formula = '-((-x+y)*-c)'
        formula_tree = build_tree(formula)
        str_tree = draw_formula_tree(formula_tree)
        result = '- * - c\n    + y\n      - x'
        if (DRAW_TREE_VERBOSE == 1):
            print("")
            print(formula)
            print(str_tree)

        self.assertEqual(str_tree, result)


# 2 tests
class TestEvaluate(unittest.TestCase):

    def test_01_simple_one_variable(self):
        formula = 'a'
        variables = 'a'
        values = '0'
        formula_tree = build_tree(formula)
        str_tree = evaluate(formula_tree, variables, values)
        result = 0

        self.assertEqual(str_tree, result)

    def test_02_simple_or(self):
        formula = '(a+b)'
        variables = 'ab'
        values = '01'
        formula_tree = build_tree(formula)
        str_tree = evaluate(formula_tree, variables, values)
        result = 1

        self.assertEqual(str_tree, result)

hard_tree = build_tree('((-((x+z)*x)+(y*(((-z*y)+z)*-z)))+((x*(((x+y)*z)*(-x*(-y+z))))+-((y*z)+-x)))')

class TestPlay2Win(unittest.TestCase):

    def test_01(self):
        turns = 'AAA'
        variables = 'xyz'
        values = ''
        win_value = play2win(hard_tree, turns, variables, values)
        result = 1

        self.assertEqual(win_value, result)

    def test_02(self):
        turns = 'AAA'
        variables = 'yxz'
        values = ''
        win_value = play2win(hard_tree, turns, variables, values)
        result = 1

        self.assertEqual(win_value, result)

    def test_03(self):
        turns = 'AAA'
        variables = 'zxy'
        values = ''
        win_value = play2win(hard_tree, turns, variables, values)
        result = 1

        self.assertEqual(win_value, result)

    def test_04(self):
        turns = 'AAA'
        variables = 'zxy'
        values = '1'
        win_value = play2win(hard_tree, turns, variables, values)
        result = 1

        self.assertEqual(win_value, result)

    def test_05(self):
        turns = 'AAA'
        variables = 'zxy'
        values = '11'
        win_value = play2win(hard_tree, turns, variables, values)
        result = 1

        self.assertEqual(win_value, result)

    def test_06(self):
        turns = 'AAA'
        variables = 'zxy'
        values = '0'
        win_value = play2win(hard_tree, turns, variables, values)
        result = 0

        self.assertEqual(win_value, result)

    def test_07(self):
        turns = 'EEE'
        variables = 'zxy'
        values = ''
        win_value = play2win(hard_tree, turns, variables, values)
        result = 1

        self.assertEqual(win_value, result)

    def test_08(self):
        turns = 'AAE'
        variables = 'zxy'
        values = '11'
        win_value = play2win(hard_tree, turns, variables, values)
        result = 0

        self.assertEqual(win_value, result)

    def test_09(self):
        turns = 'AEA'
        variables = 'zxy'
        values = '1'
        win_value = play2win(hard_tree, turns, variables, values)
        result = 0

        self.assertEqual(win_value, result)

    def test_10(self):
        turns = 'AAE'
        variables = 'zxy'
        values = ''
        win_value = play2win(hard_tree, turns, variables, values)
        result = 0

        self.assertEqual(win_value, result)

    def test_11(self):
        turns = 'AAE'
        variables = 'zxy'
        values = '1'
        win_value = play2win(hard_tree, turns, variables, values)
        result = 0

        self.assertEqual(win_value, result)

    def test_12(self):
        turns = 'EAE'
        variables = 'xyz'
        values = ''
        win_value = play2win(hard_tree, turns, variables, values)
        result = 1

        self.assertEqual(win_value, result)


if (__name__ == '__main__'):
    unittest.main(exit=False)

    #formula = '((-((x+z)*x)+(y*(((-z*y)+z)*-z)))+((x*(((x+y)*z)*(-x*(-y+z))))+-((y*z)+-x)))'
    #tree = build_tree(formula)

    #print(evaluate(tree, 'xyz', '000'))

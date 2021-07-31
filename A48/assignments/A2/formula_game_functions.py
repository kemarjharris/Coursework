# Copyright Nick Cheng, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment

# Add your functions here.


def build_tree(formula):
    '''(str) -> FormulaTree
    Given a string, creates a FormulaTree representation of the string.
    >>> build_tree('(-x*x)')
    AndTree(NotTree(Leaf('x')), Leaf('x'))
    >>> build_tree('x')
    Leaf('x')
    >>> build_tree('-y')
    NotTree(Leaf('y'))
    >>> build_tree('(x*y)')
    AndTree(Leaf('x'), Leaf('y'))
    >>> build_tree('(x+(x+y))')
    OrTree(Leaf('x'), OrTree(Leaf('x'), Leaf('y')))
    >>> build_tree('((x+y)*(y+x))')
    AndTree(OrTree(Leaf('x'), Leaf('y')), OrTree(Leaf('y'), Leaf('x')))
    '''
    # check if the formula follows the necesarry criteria for a valid formula.
    if is_valid_formula(formula):
        # create and return the tree.
        return make_tree(formula)


def make_tree(input_string):
    '''(str) -> FormulaTree
    Given a valid string, create a FormulaTree representation of the string.
    REQ: String must be a valid formula.
    Note: In given examples, the symbol @ stands for * and +. ~ stands for
    any type of variable.
    >>> make_tree('(-x*x)')
    AndTree(NotTree(Leaf('x')), Leaf('x'))
    >>> make_tree('x')
    Leaf('x')
    >>> make_tree('-y')
    NotTree(Leaf('y'))
    >>> make_tree('(x*y)')
    AndTree(Leaf('x'), Leaf('y'))
    >>> make_tree('(x+(x+y))')
    OrTree(Leaf('x'), OrTree(Leaf('x'), Leaf('y')))
    >>> make_tree('((x+y)*(y+x))')
    AndTree(OrTree(Leaf('x'), Leaf('y')), OrTree(Leaf('y'), Leaf('x')))
    '''
    # if its just a value, create a leaf node with just the variable ie. x
    if input_string in 'abcdefghijklmnopqrstuvwxyz':
        tree = Leaf(input_string)

    # if it starts with a negative operator, send everything after negative
    elif (input_string.startswith('-')):
        tree = NotTree(make_tree(input_string[1:]))

    # if it's a formula with only one operand @, and exactly two variables.
    # A negative operator will never be outside of the brackets, because that
    # occurence is handled by the above elif statement.
    # Create the rest of the tree with the two given leaves.
    elif ((input_string.count('(')) == 1 and (input_string.count(')') == 1)):
        try:
            op_ind = input_string.index('+')
            tree = OrTree(make_tree(input_string[1:op_ind]),
                          make_tree(input_string[op_ind + 1: -1]))
        # if the plus wasnt found that implies that the operator will be *
        except ValueError:
            op_ind = input_string.find('*')
            tree = AndTree(make_tree(input_string[1:op_ind]),
                           make_tree(input_string[op_ind + 1: -1]))

    # recursive case.
    # Note: any string that touches this code will always be bracketed.
    else:
        # If there are brackets before the main operand
        brac_close_id = (find_end_bracket(input_string))
        if (brac_close_id >= 0):
            # Create the corresponding tree according to the operator.
            if input_string[brac_close_id + 1] == '*':
                tree = AndTree(make_tree(input_string[1:brac_close_id + 1]),
                               make_tree(input_string[brac_close_id + 2: -1]))
            else:
                tree = OrTree(make_tree(input_string[1:brac_close_id + 1]),
                              make_tree(input_string[brac_close_id + 2: -1]))

        # if there arent any brackets before the main operand, and the first
        # variable is negated
        # input given to this block will be of the form (-x @ (~~~~~))
        elif input_string[1:].startswith('-'):
            if input_string[3] == '*':
                tree = AndTree(make_tree(input_string[1:3]),
                               make_tree(input_string[4:-1]))
            else:
                tree = OrTree(make_tree(input_string[1:3]),
                              make_tree(input_string[4:-1]))
        # If not, just make a value tree with the variable, and the rest of the
        # formula on the right
        # Input given to this block will be of the form (x @ (~~~~~))
        else:
            if input_string[2] == '*':
                tree = AndTree(make_tree(input_string[1]),
                               make_tree(input_string[3:-1]))
            else:
                tree = OrTree(make_tree(input_string[1]),
                              make_tree(input_string[3:-1]))
    return tree


def draw_formula_tree(root, left_pos=1):
    '''(FormulaTree, int) -> str
    Takes a FormulaTree root and returns a string representation of the tree.
    >>> tree = build_tree('(j*i)')
    >>> a = draw_formula_tree(tree)
    >>> print(a)
    * i
      j
    >>> tree = build_tree('((-x+y)*(-y+x))')
    >>> a = draw_formula_tree(tree)
    >>> print(a)
    * + x
        - y
      + y
        - x
    >>> tree = build_tree('(x*i)')
    >>> a = draw_formula_tree(tree)
    >>> print(a)
    * i
      x
    >>> tree = build_tree('((x+y)*-(y+x))')
    >>> a = draw_formula_tree(tree)
    >>> print(a)
    * - + x
          y
      + y
        x
    '''
    tree_string = ''
    # If the root isn't None,
    if root:
        # Add the current root's symbol to the string.
        tree_string = tree_string + root.symbol
        # If the tree has a right child,
        if len(root.children) > 1 and root.children[1]:
            # indent the string, and add the right subchild to the string.
            tree_string = (tree_string + ' ' +
                           draw_formula_tree(root.children[1], left_pos + 1))
        # If the tree has a left child, Indent the string and add a newline.
        # Then, add the left side to the string.
        if len(root.children) > 0 and root.children[0]:
            if not (len(root.children) == 1):
                tree_string += '\n' + '  '*left_pos
            else:
                tree_string += ' '
            tree_string += draw_formula_tree(root.children[0], left_pos + 1)
    return tree_string


def brac_before_op(input_string):
    '''(str) -> bool
    checks if the left side of a formula has brackets or not. if it has
    brackets that implies that it has an operator in it.
    >>> brac_before_op('x+y)')
    False
    >>> brac_before_op('(x+x)*(y*y))')
    True
    >>> brac_before_op('(x+y)')
    True
    >>> brac_before_op('x*y)')
    False
    >>> brac_before_op('(x*x)*(y*y))')
    True
    >>> brac_before_op('(x+x)+(y+y))')
    True
    >>> brac_before_op('(x*y)')
    True
    >>> brac_before_op('x*(x+y))')
    False
    '''
    # Find where the bracket is in the string. If it's not there, pretend it's
    # at the very back of the string.
    try:
        open_bracket_ind = input_string.index('(')
    except ValueError:
        open_bracket_ind = len(input_string)

    # Find the operators in the string.
    if ('*' in input_string) and ('+' in input_string):
        asterisk_bracket_ind = input_string.find('*')
        plus_bracket_ind = input_string.find('+')
        # If the open bracket appears before the operators, that means there is
        # a formula infront of the operator. Therefore, set result to True.
        result = ((open_bracket_ind < asterisk_bracket_ind) and
                  (open_bracket_ind < plus_bracket_ind))

    # Same as case above, but for just +
    elif ('+' in input_string):
        plus_bracket_ind = input_string.find('+')
        result = (open_bracket_ind < plus_bracket_ind)
    # Same as case above, except for just *
    elif ('*' in input_string):
        asterisk_bracket_ind = input_string.find('*')
        result = (open_bracket_ind < asterisk_bracket_ind)
    # If an operator hasn't been found, that means the open bracket will always
    # appear first.
    else:
        result = True
    return result


def play2win(root, turns, variables, values):
    '''(FormulaTree, str, str, str) -> int
    Given a valid formula game with all the necesary variables, this function
    returns the next best move for whoever's turn it is. If the next best turn
    is the same, return the default value. A's default is 0, and E's default
    is 1.
    REQ: length of values is less than length of variables.
    >>> a = build_tree('x')
    >>> play2win(a, 'A', 'x', '')
    0
    >>> a = build_tree('x')
    >>> play2win(a, 'E', 'x', '')
    1
    >>> a = build_tree('(x*y)')
    >>> play2win(a, 'AE', 'xy', '')
    0
    >>> a = build_tree('(x*y)')
    >>> play2win(a, 'AE', 'xy', '0')
    1
    >>> a = build_tree('(x+y)')
    >>> play2win(a, 'AE', 'xy', '')
    0
    >>> a = build_tree('(x*y)')
    >>> play2win(a, 'EA', 'xy', '1')
    0
    >>> a = build_tree('(x*y)')
    >>> play2win(a, 'EA', 'xy', '1')
    0
    >>> a = build_tree('(x*-y)')
    >>> play2win(a, 'AE', 'xy', '1')
    0
    '''
    # Variables to count the number of wins for each input.
    zerowintally = 0
    onewintally = 0
    # Find out whose turn it is
    player = turns[:len(values) + 1][-1]
    # get all possible permuations of the game:
    unset_variables = variables[len(values):]
    bin_list = []
    for i in range(2**len(unset_variables)):
        bin_val = bin(i)[2:]
        bin_val = '0'*(len(unset_variables) - len(bin_val)) + bin_val
        bin_list.append(bin_val)
    # play the game with all the possible permutations.
    for i in range(len(bin_list)):
        answer = evaluate(root, variables, values + bin_list[i])
        a = bin_list[i]
        # Determine who wins the most games depending on the permutations.
        if player == 'E':
            if answer == 1 and bin_list[i][0] == '1':
                onewintally += 1
            elif answer == 1 and bin_list[i][0] == '0':
                zerowintally += 1
        elif player == 'A':
            if answer == 0 and bin_list[i][0] == '1':
                onewintally += 1
            elif answer == 0 and bin_list[i][0] == '0':
                zerowintally += 1
    # Return whichever number had the greatest number of wins.
    if zerowintally > onewintally:
        result = 0
    elif zerowintally < onewintally:
        result = 1
    elif player == 'A':
        result = 0
    else:
        result = 1
    return result


def evaluate(root, variables, values):
    '''(FormulaTree, str, str) -> int or None
    Given a FormulaTree and the corresponding variables and values of the trees
    in that formula, this function will evaluate what truth value of the
    FormulaTree is. If any of the values are missing, this formula will return
    None.
    >>> tree = build_tree('((-x+y)*-(-y+x))')
    >>> evaluate(tree, 'yx', '00')
    0
    >>> tree = build_tree('((-x+y)*-(-y+x))')
    >>> evaluate(tree, 'xy', '10')
    0
    >>> tree = build_tree('((x+y)*((y+z)*(-y+-z)))')
    >>> evaluate(tree, 'yzx', '101')
    1
    >>> tree = build_tree('((a+b)*((b+c)*(-b+-c)))')
    >>> evaluate(tree, 'abc', '110')
    1
    >>> tree = build_tree('((x+y)*((y+z)*(-y+-z)))')
    >>> evaluate(tree, 'xyz', '010')
    1
    '''
    left = None
    right = None
    # If the given tree is a leaf,
    if len(root.children) == 0:
        # Create a string with just the given variables in it.
        given_variables = variables[:len(values)]
        # If the root has a given variable in it return it's corresponding
        # numerical value, otherwise return None.
        if root.symbol in given_variables:
            result = int(values[variables.find(root.symbol)])
        else:
            result = None
    # recursive case
    else:
        # If the left child exists, set left to it's corresponding numerical
        # value. Follow suit with the right child
        if root.children[0]:
            left = evaluate(root.children[0], variables, values)
            if isinstance(root, AndTree) and left == 0:
                result = 0
            elif isinstance(root, OrTree) and left == 1:
                result = 1

        if len(root.children) > 1 and root.children[1]:
            right = evaluate(root.children[1], variables, values)
            if isinstance(root, AndTree) and right == 0:
                result = 0
            elif isinstance(root, OrTree) and right == 1:
                result = 1
        # After retrieving the values, if the current root being evaluated is a
        # UnaryTree, just evaluate the single child.
        if len(root.children) == 1 and type(left) == (int):
            result = eval_root(root, left, right)
        # Otherwise, if both the left and right side of the tree have been set
        # to a number, evaluate it and return it.
        elif type(left) == (int) and type(right) == (int):
            result = eval_root(root, left, right)
        # However, if anything of the necesarry things needed to be set has not
        # simply return None.
        else:
            result = None
    return result


def eval_root(root, left, right):
    '''(FormulaTree, int, int) -> int
    Given a root, and the roots left and right numerical value, this function
    returns what the root evaluates to.
    >>> a = build_tree('-x')
    >>> eval_root(a, 1, None)
    0
    >>> a = build_tree('(x*y)')
    >>> eval_root(a, 1, 0)
    0
    >>> a = build_tree('(x*y)')
    >>> eval_root(a, 1, 1)
    1
    >>> a = build_tree('(x+y)')
    >>> eval_root(a, 1, 0)
    1
    >>> a = build_tree('(x+y)')
    >>> eval_root(a, 0, 0)
    0
    >>> a = build_tree('(x+y)')
    >>> eval_root(a, 1, 1)
    1
    '''
    # If it's a not symbol, flip the value.
    if root.symbol == '-':
        result = 1 - left
    # If both values are 1, return 1.
    elif root.symbol == '*':
        result = min(left, right)
    # If either of the values are 1, return 1.
    elif root.symbol == '+':
        result = max(left, right)
    # If the symbol is simply a value (which will never happen, but just in
    # case) return the symbol itself.
    else:
        result = root.symbol
    return result


def is_valid_formula(input_string):
    '''(str) -> bool
    Checks if the input string given is a valid Formula. if it is, return True,
    else return False.
    >>> is_valid_formula('()')
    False
    >>> is_valid_formula('(x)')
    False
    >>> is_valid_formula('(')
    False
    >>> is_valid_formula(')')
    False
    >>> is_valid_formula('')
    False
    >>> is_valid_formula('((((x))))')
    False
    >>> is_valid_formula('(-x*x)')
    True
    >>> is_valid_formula('((-x)*y)')
    False
    >>> is_valid_formula('X')
    False
    >>> is_valid_formula('x*y')
    False
    >>> is_valid_formula('-(x)')
    False
    >>> is_valid_formula('(x+(y)*z)')
    False
    >>> is_valid_formula('x')
    True
    >>> is_valid_formula('-y')
    True
    >>> is_valid_formula('(x*y)')
    True
    >>> is_valid_formula('((-x+y)*-(-y+x))')
    True
    >>> is_valid_formula('(0+y)')
    False
    >>> is_valid_formula('(((x+y)))')
    False
    >>> is_valid_formula('(((x+y))*((x+y)))')
    False
    >>> is_valid_formula('(x+y)*(x+y)')
    False
    >>> is_valid_formula('x+y)')
    False
    >>> is_valid_formula('(y+x')
    False
    >>> is_valid_formula('-((x+y))')
    False
    >>> is_valid_formula('(-(x)+(x+y))')
    False
    >>> is_valid_formula('((x*y)+((y+z)*(-y+-z)))')
    True
    >>> is_valid_formula('(z-y)')
    False
    >>> is_valid_formula('--x')
    True
    >>> is_valid_formula('xyx')
    False
    >>> is_valid_formula('xyydxsds')
    False
    >>> is_valid_formula('---------')
    False
    >>> is_valid_formula('---------x')
    True
    >>> is_valid_formula('-----------(x+y)')
    True
    >>> is_valid_formula('------------------((x+y)*(y+x))')
    True
    >>> is_valid_formula('-------(z*(c+a))')
    True
    >>> is_valid_formula('((x+y)+(x+-z)*(x+-z))')
    False
    >>> is_valid_formula('(((x+y)*(x+z))*((x+y)*(x+z)))')
    True
    >>> is_valid_formula('((((((x+y)*(y+x))))))')
    False
    >>> is_valid_formula(')x+y(')
    False
    '''
    # Strip all those pesky extra negatives
    input_string = input_string.replace('-', '')
    # Check if the formula ha the right number of brackets.
    valid = valid_num_of_brackets(input_string)
    # If so check if each character following the last is acceptable in a valid
    # formula.
    if valid and not valid_next_character(input_string):
        valid = False
    # If so, if every character in the string is lowercase and also check if it
    # has any lowercase characters in it.
    elif valid and not input_string.islower():
        valid = False
    # If so, check if each bracket has at least 3 things in it.
    elif valid and not valid_in_brac(input_string) and len(input_string) >= 3:
        valid = False
    # Return if it passed all of these tests!
    return valid


def valid_num_of_brackets(input_string):
    '''(str) -> bool
    Checks for extraneous brackets. Every pair of brackets must have a
    corresponding operator.
    >>> valid_num_of_brackets('()')
    False
    >>> valid_num_of_brackets('(*)')
    True
    >>> valid_num_of_brackets('(+)')
    True
    >>> valid_num_of_brackets('((*))')
    False'''
    valid = True
    # count the number of brackets and operators
    num_of_operators = input_string.count('+') + input_string.count('*')
    num_of_brackets = input_string.count('(') + input_string.count(')')
    # There should be one operator for two brackets
    try:
        if (num_of_brackets / num_of_operators) != 2:
            valid = False
    # If there were no operators at all
    except ZeroDivisionError:
        if len(input_string) > 1:
            valid = False
    return valid


def valid_next_character(input_string):
    '''(str) -> bool
    Checks if the next chracter in the string is followed by a valid possible
    character. If it ever isn't, valid is set to False.
    >>> valid_next_character('xy')
    False
    >>> valid_next_character('xy(')
    False
    >>> valid_next_character('()')
    False
    >>> valid_next_character(')(')
    False
    >>> valid_next_character('x*y')
    True
    >>> valid_next_character('-)')
    False'''
    valid = True
    alph = 'abcdefghijklmnopqrstuvwxyz'
    if len(input_string) == 0:
        valid = False
    for i in range(len(input_string) - 1):
        # if (, * or + isnt followed by -, (, or a letter
        if (input_string[i] == '(' or input_string[i] == '+' or
                input_string[i] == '*'):
            if not(input_string[i + 1] in '-(' or input_string[i + 1] in alph):
                valid = False
        # if ) or a letter isnt followed by an operator, or another closed
        # bracket
        elif input_string[i] == ')' or input_string[i] in alph:
            if not(input_string[i + 1] in '+*)'):
                valid = False
        # And if it isn't any of these characters, that means it has to be
        # False.
        else:
            valid = False
    return valid


def valid_in_brac(input_string):
    '''(str) -> bool
    Checks if the formula inside a bracket is valid.
    >>> valid_in_brac('x')
    False
    >>> valid_in_brac('')
    False
    >>> valid_in_brac('----x')
    False
    >>> valid_in_brac('(x+y)')
    True
    >>> valid_in_brac('((y+x)*(x+y))')
    True
    >>> valid_in_brac('((x)*(x+y))')
    False
    >>> valid_in_brac('((x+y)*(x))')
    False
    >>> valid_in_brac('(((x+y)*(x+z))*((x+y)*(x+z)))')
    True
    '''
    # Remove all the negatives
    input_string = input_string.replace('-', '')
    valid = True
    # If the given string doesn't have brackets around it and it's length is
    # greater than three, then it's invalid. This is because any input with a
    # length less than three shouldn't have brackets around it, and it was sent
    # through as a previously brcketed string.
    if (input_string.find('(') == -1 and input_string.find(')') == -1):
        if len(input_string) < 3:
            valid = False
    # Recursively send in brackeketed string to be checked if what's inside has
    # a greater length than 3.
    else:
        for i in range(len(input_string)):
            if valid is False:
                i = len(input_string) + 1
            elif input_string[i] == '(':
                # Find the bracketed pair and send everything inside it through
                # The function again.
                close_bracid = find_end_bracket('(' + input_string[i:]) - 1
                valid = valid_in_brac(input_string[i + 1: close_bracid + i])
    return valid


def find_end_bracket(input_string):
    '''(str) -> int
    given a bracketed string, it finds and returns the index of the open
    bracket's closed bracket index. If the bracket appears after the main
    operand, return -1.
    >>> find_end_bracket('(((x+y)+(y+x))+(x+y))')
    13
    >>> find_end_bracket('(x+y)')
    -1
    >>> find_end_bracket('((x+y)')
    5
    '''
    # If there was one open bracket (or none at all)
    if brac_before_op(input_string[1:]):
        bracket_num = -1
        result = None
        # Count the number of brackets that open and close. If an open bracket
        # is found, increase the bracket counter, and if a closed bracket is
        # found, decrease the number.
        for i in range(len(input_string)):
            if result is not None:
                i = len(input_string) + 1
            elif input_string[i] == '(':
                bracket_num += 1
            elif input_string[i] == ')':
                bracket_num -= 1
                # If a close bracket was found it matches to the first bracket,
                # return this id.
                if bracket_num == 0:
                    result = i
    else:
        result = -1
    return result

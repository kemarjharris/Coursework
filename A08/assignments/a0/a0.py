# Code for working with word search puzzles
#
# Do not modify the existing code
#
# Complete the tasks below marked by *task*
#
# Before submission, you must complete the following header:
#
# I hear-by decree that all work contained in this file is solely my own
# and that I received no help in the creation of this code.
# I have read and understood the University of Toronto academic code of
# behaviour with regards to plagiarism, and the seriousness of the
# penalties that could be levied as a result of committing plagiarism
# on an assignment.
#
# Name: Kemar Harris
# MarkUs Login: harri471
#

PUZZLE1 = '''
tlkutqyu
hyrreiht
inokdcne
eaccaayu
riainpaf
rrpnairb
ybybnick
ujvaynak
'''

PUZZLE2 = '''
fgbkizpyjohwsunxqafy
hvanyacknssdlmziwjom
xcvfhsrriasdvexlgrng
lcimqnyichwkmizfujqm
ctsersavkaynxvumoaoe
ciuridromuzojjefsnzw
bmjtuuwgxsdfrrdaiaan
fwrtqtuzoxykwekbtdyb
wmyzglfolqmvafehktdz
shyyrreihtpictelmyvb
vrhvysciipnqbznvxyvy
zsmolxwxnvankucofmph
txqwkcinaedahkyilpct
zlqikfoiijmibhsceohd
enkpqldarperngfavqxd
jqbbcgtnbgqbirifkcin
kfqroocutrhucajtasam
ploibcvsropzkoduuznx
kkkalaubpyikbinxtsyb
vjenqpjwccaupjqhdoaw
'''


def rotate_puzzle(puzzle):
    '''(str) -> str
    Return the puzzle rotated 90 degrees to the left.
    '''

    raw_rows = puzzle.split('\n')
    rows = []
    # if blank lines or trailing spaces are present, remove them
    for row in raw_rows:
        row = row.strip()
        if row:
            rows.append(row)

    # calculate number of rows and columns in original puzzle
    num_rows = len(rows)
    num_cols = len(rows[0])

    # an empty row in the rotated puzzle
    empty_row = [''] * num_rows

    # create blank puzzle to store the rotation
    rotated = []
    for row in range(num_cols):
        rotated.append(empty_row[:])
    for x in range(num_rows):
        for y in range(num_cols):
            rotated[y][x] = rows[x][num_cols - y - 1]

    # construct new rows from the lists of rotated
    new_rows = []
    for rotated_row in rotated:
        new_rows.append(''.join(rotated_row))

    rotated_puzzle = '\n'.join(new_rows)

    return rotated_puzzle


def lr_occurrences(puzzle, word):
    '''(str, str) -> int
    Return the number of times word is found in puzzle in the
    left-to-right direction only.

    >>> lr_occurrences('xaxy\nyaaa', 'xy')
    1
    '''
    return puzzle.count(word)

# ---------- Your code to be added below ----------

# *task* 3: write the code for the following function.
# We have given you the header, type contract, example, and description.


def total_occurrences(puzzle, word):
    '''(str, str) -> int
    Return total occurrences of word in puzzle.
    All four directions are counted as occurrences:
    left-to-right, top-to-bottom, right-to-left, and bottom-to-top.

    >>> total_occurrences('xaxy\nyaaa', 'xy')
    2
    '''
    #tally all of the occurrences in each rotation of the puzzle
    #left to right
    occurance_tally = lr_occurrences(puzzle, word)
    #top to bottom
    rotatated_puzzle = rotate_puzzle(puzzle)
    occurance_tally += lr_occurrences(rotatated_puzzle, word)
    #right to left
    rotatated_puzzle = rotate_puzzle(rotatated_puzzle)
    occurance_tally += lr_occurrences(rotatated_puzzle, word)
    #bottom to top
    rotatated_puzzle = rotate_puzzle(rotatated_puzzle)
    occurance_tally += lr_occurrences(rotatated_puzzle, word)    
    #return total
    return occurance_tally
    
    # your code here

# *task* 5: write the code for the following function.
# We have given you the function name only.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def in_puzzle_horizontal(puzzle, word):
    '''(str, str) -> bool
    Return True if a word is found in the horizontal direction.
    
    >>>in_puzzle_horizontal('abc\nbab\naca', 'abc')
    True
    '''
    #rotate puzzle twice and save it to a new variable
    puzzle_backwards = rotate_puzzle(puzzle)
    puzzle_backwards = rotate_puzzle(puzzle_backwards)
    #check if the puzzle and the puzzle backwards has the word in it  
    result = (lr_occurrences(puzzle, word) >= 1) or (lr_occurrences(puzzle_backwards, word) >= 1)
    #return result
    return result

# *task* 8: write the code for the following function.
# We have given you the function name only.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def in_puzzle_vertical(puzzle, word):
        '''(str, str) -> bool
        Return True if the word is found in the puzzle in the vertical 
        direction.
        
        >>>in_puzzle_vertical('abc\nbab\naca', 'abc')
        True
        '''   
        #rotate once and save to bottom to top
        puzzle_top_to_bottom = rotate_puzzle(puzzle)
        #rotate two more times and save in a new variable
        puzzle_bottom_to_top = rotate_puzzle(puzzle_top_to_bottom)
        puzzle_bottom_to_top = rotate_puzzle(puzzle_bottom_to_top)
        #compare two new rotated puzzles if they have the word in it
        result = (lr_occurrences(puzzle_top_to_bottom, word) >= 1) or (lr_occurrences(puzzle_bottom_to_top, word) >= 1)
        #return a boolean.
        return result
# *task* 9: write the code for the following function.
# We have given you the function name only.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def in_puzzle(puzzle, word):
    '''(str, str) -> bool
           Return True if the word is found in the puzzle in any direction.
           
           >>>in_puzzle('abc\nbab\naca', 'abc')
           True
           >>>in_puzzle('abc\nbab\naca', 'def')
           False
           '''       
    #compare if the word is found either vertically or horrizontally by calling
    #previously defined functions.
    result= (in_puzzle_vertical(puzzle, word)) or (in_puzzle_horizontal(puzzle, word))
    #return the result.
    return result

# *task* 10: write the code for the following function.
# We have given you only the function name and parameters.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def in_exactly_one_dimension(puzzle, word):  
    
    '''(str, str)-> bool
    If the word is in one dimension but no the other, return true. If the 
    words happens to not be in the puzzle, the result will be true.
    
    >>>in_exactly_one_dimension('abc\nbab\naca', 'abc')
    False
    >>>in_exactly_one_dimension('abc\nbab\naca', 'def')
    True
    >>>in_exactly_one_dimension('abc\nbab\naca', 'aca')
    True
    '''
    #comparisons
    result = not(((in_puzzle_vertical(puzzle, word)) and (in_puzzle_horizontal(puzzle, word))) or ((in_puzzle_vertical(puzzle, word)) and (in_puzzle_horizontal(puzzle, word))))
    #return result
    return result

# *task* 11: write the code for the following function.
# We have given you only the function name and parameters.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.


def all_horizontal(puzzle, word):
    '''(str, str) -> bool
    Return True if the word only appears in the puzzle in the horizontal 
    direction. If the word appears in the vertical direction, it will be false.
    If the word is not in the puzzle, it will be true.
    >>>all_horizontal('abc\nbab\naca', 'abc')
    False
    '''
    result = ((in_puzzle_horizontal(puzzle, word)) and (not((in_puzzle_vertical(puzzle, word)))))
    return result                                                      
# *task* 12: write the code for the following function.
# We have given you only the function name and parameters.
# You must follow the design recipe and complete all parts of it.
# Check the handout for what the function should do.

def at_most_one_vertical(puzzle, word):
    '''(str, str)-> bool
    Return if a word is in the puzzle in the vertical direction.
    >>>at_most_one_vertical('abc\nbab\naca', 'abc')
    True
    '''
    #rotate once and save to bottom to top
    puzzle_top_to_bottom = rotate_puzzle(puzzle)
    #rotate two more times and save in a new variable
    puzzle_bottom_to_top = rotate_puzzle(puzzle_top_to_bottom)
    puzzle_bottom_to_top = rotate_puzzle(puzzle_bottom_to_top)    
    vertical_word_count= lr_occurrences(puzzle_top_to_bottom, word) + lr_occurrences(puzzle_bottom_to_top, word)
    return (((vertical_word_count) <= 1) and not(in_puzzle_horizontal(puzzle, word)))
                                               

def do_tasks(puzzle, name):
    '''(str, str) -> NoneType
    puzzle is a word search puzzle and name is a word.
    Carry out the tasks specified here and in the handout.
    '''

    # *task* 1a: add a print call below the existing one to print
    # the number of times that name occurs in the puzzle left-to-right.
    # Hint: one of the two starter functions defined above will be useful.

    # the end='' just means "Don't start a newline, the next thing
    # that's printed should be on the same line as this text
    print('Number of times', name, 'occurs left-to-right: ', end='')
    # your print call here
    print(lr_occurrences(puzzle, name)) 
  
    # *task* 1b: add code that prints the number of times
    # that name occurs in the puzzle top-to-bottom.
    # (your format for all printing should be similar to
    # the print statements above)
    # Hint: both starter functions are going to be useful this time!
    rotated_puzzle = rotate_puzzle(puzzle)
    print('Number of times', name, 'occurs top-to-bottom: ', end='')
    print(lr_occurrences(rotated_puzzle, name)) 

    # *task* 1c: add code that prints the number of times
    # that name occurs in the puzzle right-to-left.
    rotated_puzzle = rotate_puzzle(rotated_puzzle)
    print('Number of times', name, 'occurs right-to-left: ', end='')
    print(lr_occurrences(rotated_puzzle, name))

    # *task* 1d: add code that prints the number of times
    # that name occurs in the puzzle bottom-to-top.
    rotated_puzzle = rotate_puzzle(rotated_puzzle)
    print('Number of times', name, 'occurs bottom-to-top: ', end='')
    print(lr_occurrences(rotated_puzzle, name))
    

    # *task* 4: print the results of calling total_occurrences on
    # puzzle and name.
    # Add only one line below.
    # Your code should print a single number, nothing else.
    print(total_occurrences(puzzle, name))
    # *task* 6: print the results of calling in_puzzle_horizontal on
    # puzzle and name.
    # Add only one line below. The code should print only True or False.
    print(in_puzzle_horizontal(puzzle, name))

do_tasks(PUZZLE1, 'brian')

# *task* 2: call do_tasks on PUZZLE1 and 'nick'.
# Your code should work on 'nick' with no other changes made.
# If it doesn't work, check your code in do_tasks.
# Hint: you shouldn't be using 'brian' anywhere in do_tasks.
do_tasks(PUZZLE1, 'nick')

# *task* 7: call do_tasks on PUZZLE2  and 'nick'.
# Your code should work on the bigger puzzle with no changes made to do_tasks.
# If it doesn't work properly, go over your code carefully and fix it.
do_tasks(PUZZLE2, 'nick')

# *task* 9b: print the results of calling in_puzzle on PUZZLE1 and 'nick'.
# Add only one line below. Your code should print only True or False.
print(in_puzzle(PUZZLE1, 'nick'))

# *task* 9c: print the results of calling in_puzzle on PUZZLE2 and 'thierry'.
# Add only one line below. Your code should print only True or False.
print(in_puzzle(PUZZLE2, 'thierry'))
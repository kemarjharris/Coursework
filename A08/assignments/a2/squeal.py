from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results
# NOTE: the tables used in most examples if not all examples are as follows:
# {'book.year': ['1979', '2014', '2015', '2014'],
# 'book.title': ['Godel Escher Bach', 'What if?', 'Thing Explainer', 'Alan Turing: The Enigma'],
# 'book.author': ['Douglas Hofstadter', 'Randall Munroe', 'Randall Munroe', 'Andrew Hodges']}
# {'alpha.#': ['1', '2', '3'],
# 'alpha.span': ['uno', 'dos', 'tres'],
# 'alpha.a': ['a', 'b', 'c']}
# {'o.year': ['2010', '2003', '1997', '1997'],
# 'o.category': ['Animated Feature Film', 'Directing', 'Directing', 'Best Picture'],
# 'o.title': ['Toy Story 3', 'The Lord of the Rings: The Return of the King', 'Titanic', 'Titanic']}

def cartesian_product(table1, table2):
    '''(Table, Table) -> Table
    a function that combines two tables. It will multiply the tables together,
    and then return a new table.
    REQ: this function gets two tables
    REQ: none of the given tables are empty.
    '''
    # get the table columns and coloumn names of both tables given in the
    # parameter
    t1_col_names = table1.get_column_names()
    t2_col_names = table2.get_column_names()
    t1_rows = table1.get_rows()
    t2_rows = table2.get_rows()
    # assign the column names to one big list
    t_12_col_names = t1_col_names + t2_col_names
    # multiply the rows in the first table
    hold_list = []
    # for the amount of rows that the first table has
    for i in range(len(t1_rows)):
        # for the amount of rows the second table has
        for x in range(len(t2_rows)):
            # add a list version of every row in t1 to a new_list.
            hold_list += [(t1_rows[i])]
    #for the length of hold list
    for i in range(len(hold_list)):
        # get the remainder of the spot i is at divided by the length of t2_rows
        a = i % (len(t2_rows))
        # save z to a copy of of hold_list at each index
        z = hold_list[i].copy()
        # do this twice
        for x in range(1):
            # add the rows at the index of t2_rows at a to the list z
            z += t2_rows[a]
            # add all of this to the list copy
            hold_list[i] = z
    # save this list, which is now the rows of the new table, to a variable.
    t_12_rows = hold_list
    # create a dictiionary with both of these news coloumns and rows.
    cart_dicto = Table(t_12_col_names, t_12_rows)
    return cart_dicto

def run_query(base, user_input):
    '''(Database, str) -> Table
    Runs the query.
    query will be in the form:
    [select, col_names, from, table_names, where, where clause]
    REQ: user input is in proper SQuEaL format.
    '''
    # split user input to list
    query = user_input.split()
    #get all of the where clauses
    if (len(query) > 4):
        where_clause = query[5].split(',')
    # select each row and get that list for the rows
    table_names = query[3].split(',')
    # get all the column names
    col_names = []
    for e in table_names:
        col_names += base.get_table(e).get_column_names()
    # get the table needed if its only from one table
    if (len(table_names) == 1):
        needed_rows = create_row_list(table_names, col_names, base)
        # initialize the variable t2 just in case where is called on one
        t2 = Table(col_names,needed_rows)
    # getting from two different tables
              # from
    else:
        # get the first two tables
        t1 = base.get_table(table_names[0])
        t2 = base.get_table(table_names[1])
        # multiply the first two tables in a cartesian product
        t2 = cartesian_product(t1, t2)
        # get the rows needed from the cartesian product
        needed_rows = cart_create_row_list(t2, base)
        # if more than two tables are being multiplied, aka if more then 2
        # tables are called
        if (len(table_names) > 2):
            # counter for while loop, starts at 1 because first table has
            # already gone through the function
            i = 1
            # while i is less than the length of the tables called MINUS 2
            # because two tables have already been multiplied
            while (i <= (len(table_names) - 2)):
                # cartesian product each table called
                t2 = cartesian_product(t2,base.get_table(table_names[i+1]))
                # get the rows from the new cartesian table
                needed_rows = cart_create_row_list(t2, base)
                i+=1
    #use the table init to initialize the new table
            # where
    # if the where clause was inputted
    if (len(query) > 4):
        # save the where clauses to list
        where_clause = query[5].split(',')
        # do the first where clause
        needed_rows = do_where_clause(where_clause[0], t2)
        #do the where clause more than once if there is more than one.
        if (len(where_clause) >= 2):
            # create the next table for the where clause
            next_t_for_clause = Table(col_names, needed_rows)
            i = 1
            while (i < (len(where_clause))):
                # do the next where clause
                needed_rows = do_where_clause(where_clause[i], next_t_for_clause)
                # make a new table with the previous where claus executed
                next_t_for_clause = Table(col_names, needed_rows)
                # increase count
                i += 1
    # after the where clauses have been handled, make the next table
    final_table = Table(col_names, needed_rows)
    # do the select clause
    #if all the colouns havent already been chosen/ if the user did not input *
    if (query[1] != '*'):
        # run select_wanted_columns to get the coloumns needed
        final_table = select_wanted_columns(query, final_table)
    # after from, where, and select have been handled, return the final table
    return final_table

#function to select each column
def select_wanted_columns(query, result_query):
    '''(list, Table)-> Table
    A function that takes the query and a table, and using the query finds what
    values need to be selected, and makes a table using those values.
    REQ: a column has been selected.
    '''
    # get the wanted column names from the query
    col_names = query[1].split(',')
    # get the column at each column name
    #make a table and return it
    # blank variables, hold_list for holding data and a to index through the
    # wanted coloumn names
    hold_list = []; a = 0
    # for the amount of coloumns called
    for i in range(len(col_names)):
        # add each coloumn to a list at each called column
        hold_list += [result_query.get_column(col_names[a])]
        # add one to the counter
        a+=1
    # take the list and put it from coloumn format into row format
    hold_list = set_proper_list(hold_list)
    # make a new table with only the selected coloumns and rows
    table = Table(col_names, hold_list)
    # return the new table
    return table


def create_row_list(table_names, column_names, base):
    '''(list, list, Database) -> list of list of str
    a function that gets the table names and column names and puts them in a
    list to be made into the selected part of a table
    Note: this function works for 1 and only 1 table.
    REQ: only one tables is given
    REQ: the database given isnt empty
    REQ: a table name is actually called.'''
    # a blank list, and a blank variable for indexing
    total_list = []; b = 0
    # for all of the column names called
    for x in range(len(column_names)):
        # for the amount of column names called
        while (b < len(column_names)):
            # table is assigned to table for the current table name, aka the
            # current table that table_names is at
            table = base.get_table(table_names[0])
            # an empty list
            hold_list= []
            # c is the things in each column
            c = table.get_column(column_names[b])
            # add 1 to counter
            b += 1
            # for the number of things in the column
            for l in range(len(c)):
                # a list version of each thing in the column to hold list
                hold_list += [c[l]]
            # add the list of each thing in each coloumn to the total things in
            # each coloumn
            total_list += [hold_list]
    # run the set_proper_lost methed to arrange from coloumn form to row form
    # and return in
    return set_proper_list(total_list)

def cart_create_row_list(table, base):
    '''(Table, list) -> list of list of str
    a function that gets the table names and column names and puts them in a
    list to be made into the selected rows of a table
    Note: this function works for 1 and only 1 table. This function is a
    duplicate of create_row_list, except specifically for the cartesian
    producted table
    REQ: the table given has columns.'''

    # a blank list
    total_list = []; b= 0
    # for all of the column names called
    column_names = table.get_column_names()
    # for the amount of coloumns called (which will be all of them)
    for x in range(len(column_names)):
        # for the amount of column names called
        while (b < len(column_names)):
            #because the table is already set to a cartesian table, and table is
            # is now the parameter nothing needs to be changed
            hold_list= []
            # c is the things in each column
            c = table.get_column(column_names[b])
            # add 1 to the counter
            b += 1
            # for the number of things in the column
            for l in range(len(c)):
                # a list version of each thing in the column to hold list
                hold_list += [c[l]]
            # add each hold_list to a list
            total_list += [hold_list]
    # return the coloumns in row format
    return set_proper_list(total_list)

def set_proper_list(total_list):
    '''(list of list of str) -> list
    Rearranges the list to its proper order to get the desired columns. It
    rearranges a list of a list from coloumn form to row form and vice versa.
    REQ: a list of a list is given
    '''
    # rearrange the orders of the list from column form to row form and vice
    # versa
    # initialize blak variables, one for saving information and one for indexing
    final_rows = []; i = 0
    # for the number of columns in the table
    for x in range(len(total_list[i])):
        # another blank list for holding information
        hold_list = []
        # for all the rows in the table
        for i in range(len(total_list)):
            # add each value at the start of the coloumn to a new row
            hold_list += [total_list[i][x]]
        # add this row to the final rows
        final_rows += [hold_list]
    # return hold list
    return final_rows

def do_where_clause(where_clause, table):
    '''(list, str, Table) -> list of list
    a function that handles the where clauses depending on what the clauses
    were and what values were given.
    REQ: A where clause is given
    REQ: A table is given.'''
    # if clause is =, clause = true otherwise clause = False
    clause = True
    # find the equal sign in the where clause
    index = where_clause.find('=')
    # if it wasnt there (when its not there .find returns -1) set the clause to
    # false.
    if index == (-1):
        # find the index where the greater sign is and set the clause to false,
        # to later say to compare for greater than and not for equal to.
        index = where_clause.index('>')
        clause = False
    # get column that needs to be compared, aka column 1
    col_1 = where_clause[:index]
    # get column that needs to be compared to, aka column 2
    col_2 = where_clause[index+1:]
    #check if the second thing is equeal to a value or a column.
    # get all the coloumn names
    col_names = table.get_column_names()
    # interate through the coloumn names and if it's there set the variable
    # coloumn to true.
    is_column = False
    for i in range(len(col_names)):
        # if col_2 has a value in col_names then column is true and a value is
        # being compared and not two column names
        if (col_2 == col_names[i]):
            is_column = True
    # set column 1 to an actual column in the table
    col_1 = table.get_column(col_1)
    # set column 2 to an actual column in the table
    if (is_column is True):
        col_2 = table.get_column(col_2)
    # empty list for saving data
    hold_list = handle_clause(table, col_1, col_2, is_column, clause)
    # for all of column 2
    # if a column is being compared
    return hold_list

def handle_clause(table, col_1, col_2, is_column, clause):
    '''(Table, list, list/str, bool, bool) -> list of list of str
    A function that handles the main selection of rows in a where clause.
    REQ: All parameters are given
    REQ: table given isnt empty
    REQ: coloumns arent empy
    '''
    hold_list = []
    # if a column is being compared
    if (is_column is True):
        # if the clause is =
        if (clause is True):
            for i in range(len(col_1)):
            # if the rows are equal to each other,
                if (col_1[i] == col_2[i]):
                    # save that entire row to a new list
                    hold_list += [table.get_spec_row(i)]
        # if the clause is <
        else:
            for i in range(len(col_1)):
            # if the rows are equal to each other,
                if (col_1[i] > col_2[i]):
                    # save that entire row to a new list
                    hold_list += [table.get_spec_row(i)]
    # if a value is being compared
    else:
        if (clause is True):
            for i in range(len(col_1)):
                # if the rows are equal to each other,
                if (col_1[i] == col_2):
                    # save that entire row to a new list
                    hold_list += [table.get_spec_row(i)]
        # if the clause is <
        else:
            for i in range(len(col_1)):
            # if the rows are equal to each other,
                if (col_1[i] > col_2):
                    # save that entire row to a new list
                    hold_list += [table.get_spec_row(i)]
    return hold_list

if(__name__ == "__main__"):
    database = read_database()
    query = input("Enter a SQuEaL query, or a blank line to exit:")
    while (query != ''):
        d = run_query(database, query)
        d.print_csv()
        query = input("Enter a SQuEaL query, or a blank line to exit:")

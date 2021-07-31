# Functions for reading tables and databases

import glob
from database import *


# YOU DON'T NEED TO KEEP THE FOLLOWING CODE IN YOUR OWN SUBMISSION
# IT IS JUST HERE TO DEMONSTRATE HOW THE glob CLASS WORKS. IN FACT
# YOU SHOULD DELETE THE PRINT STATEMENT BEFORE SUBMITTING
file_list = glob.glob('*.csv')

# Write the read_table and read_database functions below
def read_table(filu):
    '''(str) -> Table
    A function that reads values from a list and returns the table given the table.
    '''
    # open the file, read, and close the file
    file = open(filu, 'r')
    content = file.readlines()
    file.close()
    # for the first line in the file, just set it to a list called "column names"
    column_names = content[0].split(',')
    # a dictionary for use for the keys
    '''table = {}
    # set each column to a key in a dictionary with an empty list
    for i in range(len(column_names)):
        column_names[i] = column_names[i].replace('\n','')
        column_names[i] = column_names[i].strip()
        table[column_names[i]] = []
    '''
    # now set the rest of the lines constant to their own list
    # create an empty list for that with the same length as content - 1
    # mvndlstand = movin da list and
    mvndlstand = []
    for i in range(1, len(content)):
        if (len(column_names) == len(content[i].split(','))):
            mvndlstand.append(content[i].split(','))
    '''for i in range(len(mvndlstand)):
        for x in range(len(mvndlstand[i])):
            mvndlstand[i][x] = mvndlstand[i][x].strip()
            mvndlstand[i][x] = mvndlstand[i][x].replace('\n','')
    #repeats  times
    # each apply to each column
    for i in range(len(column_names)):
        #repeats  times
        # go through each row
        for x in range(len(mvndlstand)):
            table[column_names[i]].append(mvndlstand[x][i])
    print(table)'''
    tabelu = Table(column_names, mvndlstand)
    return tabelu

def read_database():
    '''() -> Database
    A function that consists of all of the table files in the current directory,
    and reads them, and creates multiple tables that exist as one Database.'''
    #  create an empty database
    # run a for loop that uses the global "file_list" to get each table but set
    # it to a blank dictionary
    '''# remove .scsv from all spots
    for i in range(len(file_list)):
        file_list[i] = file_list[i].replace('.csv','')'''
    # make a list of tables
    tables = []
    f_list_copy = file_list[:]
    for i in range(len(f_list_copy)):
        tables.append(read_table(f_list_copy[i]))
    databasu = Database(tables, file_list)
    return databasu

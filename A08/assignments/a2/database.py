
class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self, columns = [], rows = []):
        '''(Table, dict) -> None
        Initializes a table. This is often used to create new tables.'''
        dicto = {}; self._columns = columns; self._rows = rows
        # set each column to a key in a dictionary with an empty list after
        # stripping newlines
        for i in range(len(self._columns)):
            self._columns[i] = self._columns[i].replace('\n','')
            self._columns[i] = self._columns[i].strip()
            dicto[self._columns[i]] = []
        # set each part in each row to its respective column
        # for the number of rows
        for i in range(len(self._rows)):
            # for the number of coloumns
            for x in range(len(self._rows[i])):
                # clean the rows
                self._rows[i][x] = self._rows[i][x].strip()
                self._rows[i][x] = self._rows[i][x].replace('\n','')
        # each apply to each column
        for i in range(len(self._columns)):
            #repeats  times
            # go through each row and add each spot at each row to a coloumn
            for x in range(len(self._rows)):
                dicto[self._columns[i]].append(self._rows[x][i])
        self._dicto = dicto

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        self._dicto = new_dict

    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        return self._dicto

    def get_column_names(self):
        '''(Table) -> list
        Gets the column names from a given table'''
        return self._columns

    def get_rows(self):
        '''(Table) -> list of list of str
        Returns a list of all the rows in the table'''
        return self._rows

    def get_column(self, key):
        '''(Table, str) -> list
        returns a list of str from a column in a table'''
        return self._dicto[key]

    def num_rows(self):
        '''(Table) -> int
        Returns how many rows the function has'''
        return len(self._rows)

    def print_csv(self):
        '''(Table) -> NoneType
        Print a representation of table in csv format.
        '''
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        row = self.num_rows()
        for i in range(row):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))

    def get_spec_row(self, row_level):
        '''(int) -> list
        Gets a specific row from a table at a certain level. This function
        ensures the rows get retured in the correct order.
        REQ: row_level has to be less than or equal the number of rows'''
        # blank list for saving
        hold_list = []
        # at each in list in each key,
        i = 0
        for key in self._dicto:
        # go through the dictionary and save each list value at a specific value to
        # a new list, then return that list.
            key = self._columns[i]
            hold_list += [self._dicto[key][row_level]]
            i += 1
        #return the list
        return hold_list


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self, tables, file_names):
        '''(Database, dict) -> None
        initializes a blank Database, which is a combo of many dicts'''
        base = {}
        self._file_names = file_names
        self._tables = tables
        for i in range(len(file_names)):
            self._file_names[i] = self._file_names[i].replace('.csv','')
            base[self._file_names[i]] = self._tables[i]
        self._base = base


    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType
        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        self._dicto = new_dict

    def get_dict(self):
        '''(Database) -> dict of {str: Table}
        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        return self._dicto

    def get_table(self, key):
        '''(str) -> able
        Gets a table from a key in the database and returns that table'''
        return self._base[key]
def create_dict(file_name):
    '''(io.TextIOWrapper) -> dict of {str: [str, str, str, int, str]}
        A function that reads a file and then creates and returns a dictionary
    with the key as a username, and the value as a list in the following order:
    last name, first name, email, age, then gender.
    REQ: the file is in the order: username, first name, last name, age, gender,
    email
    REQ: Gender is either given as M or F
    '''
    # read a file and save it to a variable.
    filu = file_name.readlines()    
    # create an empty dictionary.
    user_list = {}
    # create a for loop that reads each line of the file.
    for line in filu:
        # use .split() to save all words to a value
        val = line.split()
        # rearrange values to desired order
        # order is lastname, firstname, email, age, gender
        user_creds = [val[2], val[1], val[5], int(val[3]), val[4]]
        # create dictionary value
        user_list[val[0]] = user_creds
    # return dictionary
    return user_list

def update_field(dic, name, field, value):
    '''(dict, key, str, str/int) -> dict
    A function called update field, that takes 4 parameters: A dictionary in
    the format created by the previous function, a username, the name of a,
    field (One of: ’LAST’, ’FIRST’, ’E-MAIL’, ’AGE’ or ’GENDER’), and a new
    value to replace the current value of the specified field.
    
    REQ: when GENDER is given the value is either male or female
    REQ: age is a number
    '''
    # check the field
    # depending on the field, change the value
    diclist = dic[name]
    # if its last name
    if field == 'LAST':
        diclist[0] = value
    # if first name
    elif field == 'FIRST':
        diclist[1] = value
    # if email
    elif field == 'E-MAIL':
        diclist[2] = value
    # if age
    elif (field == 'AGE'):
        diclist[3] = value
    # if gender
    elif field == 'GENDER':
        diclist[4] = value
    # assign new value
    dic[name] = diclist
    
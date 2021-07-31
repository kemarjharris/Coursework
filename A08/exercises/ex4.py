def percent_to_gpv(grade):
    '''int-> float
    take a grade and convert it to your gpa
    REQ: grade>=0, grade<=100
    >>>percent_to_gpv(17)
    0.0
    >>>percent_to_gpv(54)
    1.0
    >>>percent_to_gpv(66)
    2.0
    '''
    #check grade values, and return.
    if (grade > 84):
        return 4.0
    elif (grade > 79):
        return 3.7
    elif (grade > 76):
        return 3.3
    elif (grade > 72):
        return 3.0
    elif (grade >69):
        return 2.7
    elif (grade > 66):
        return 2.3
    elif (grade > 62):
        return 2.0
    elif (grade > 59):
        return 1.7
    elif (grade > 56):
        return 1.3
    elif (grade > 52):
        return  1.0
    elif (grade > 49):
        return 0.7
    else:
        return 0.0

def card_namer(value, suit):
    '''(string, string)-> String
    Takes two inputs as card values and out puts a card, if its a non-existant
    card the word CHEATER is printed.
    >>> card_namer('Q','D')
    'Queen of Diamonds'
    >>> card_namer('9','S')
    '9 of Spades'
    >>> card_namer('8','T')
    'CHEATER!'
    '''
    #convert value to string to avoid disrespect
    value = str(value)
    #name first portion
    if (value=="Q"):
        value = "Queen"
    elif (value=="A"):
        value = "Ace"
    elif (value=="T"):
        value = "10"
    elif (value== "K"):
        value = "King"
    elif (value == "J"):
        value = "Jack"
    elif (value == "T"): 
        value = "10"
    elif (value >="2" and value <= "9"):
        value = str(value)
    else:
        return "CHEATER!"
    #name second portion
    if (suit =="S"):
        suit = "Spades"
    elif (suit == "D"):
        suit = "Diamonds"
    elif (suit == "C"):
        suit = "Clubs"
    elif (suit == "H"):
        suit = "Hearts"
    else:
        return "CHEATER!"
    #combine the two names
    return value + " of " + suit

# Functions for running an encryption or decryption.

# The values of the two jokers.
JOKER1 = 27
JOKER2 = 28

# Write your functions here:
def clean_message(message):
    '''(str) -> str
    A function that removes all characters from the message that arent letters,
    and then returns the message in all caps.
    REQ: the function is a string.
    
    >>> clean_message("Blue Tomatoes.")
    'BLUETOMATOES'
    >>> clean_message("3.14159265385 are a few digits of pi.")
    'AREAFEWDIGITSOFPI'
    >>> clean_message("Sayonara!")
    'SAYONARA'
    >>> clean_message("[You've got a {ways} to go]\\\")
    YOUVEGOTAWAYSTOGO'
    >>> clean_message("~SO SHOCKING!!~")
    'SOSHOCKING'
    '''
    # create a list of all the letters A-Z in uppercase.
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # first, upper case the message. 
    message = message.upper()
    # the conditions for this use the method that checks if there are any values
    # in the string are not alphanumeric
    while (not(message.isalpha())):
        # create an elemental for loop
        for e in message:
        # check if each value is a letter in the alphabet.
            if not(e in alpha):
        # if not, use .replace method to replace it with a null string.
                message = message.replace(e, '')
    # finally, when the loop ends, return the string.
    return message
    
def encrypt_letter(char, keystream):
    '''(str, int) -> str
    A function that takes a letter, and then converts the letter
    to a numbers, starting with A being 0 and Z being 25. It then runs the 
    algorithm to find the new numerical value of the character, and then
    converts it back to its letter form. It then returns this letter.
    REQ: char is uppercase.
    
    >>> encrypt_letter('L', 12)
    'W'
    >>> encrypt_letter('X', 24)
    'V'
    >>> encrypt_letter('L', 29)
    'O'
    >>> encrypt_letter('L', -2)
    'J'
    '''
    # set up the alphabet for checking
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # assign the given letter to its numerical position in the alphabet
    crypt_value = alpha.find(char)
    # if the sum of the crypt value and keystream are greater than 25, modulo 26
    if (((crypt_value) + keystream) > 25):
        crypter = (crypt_value + keystream) - 26
    # if not, just assign the value normally.
    else:
        crypter = (crypt_value + keystream)
    # return a letter at the position of cryptor in the alphabet
    return alpha[crypter]
    
def decrypt_letter(char, keystream):
    '''(str, int) -> str
    Does the same thing as the encrypt function, but backwards. 
    REQ: keystream >= -26
    REQ: char has a length of one and is a string
    
    >>> decrypt_letter('D', 9)
    'U'
    >>> decrypt_letter('X', 9)
    'O'
    >>> decrypt_letter('H', 43)
    'Q'
    '''
    # set up the alphabet for checking
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # assign the given letter to its numerical position in the alphabet
    crypt_value = alpha.find(char)
    # if the difference of the crypt value and keystream less than 0, modulo 26
    if (((crypt_value) - keystream) < 0):
        crypter = (crypt_value - keystream) + 26
    # if not, just assign the value normally.
    else:
        crypter = (crypt_value - keystream)
    # return a letter at the position of cryptor in the alphabet
    return alpha[crypter]    
    
def read_deck(file):
    '''(file open for reading) -> list of int *****
    A function that reads a file of integers and adds them all to a list.
    REQ: The file has integers in it.
    REQ: The file has no strings.
    
    >>> file = open('deck1.txt', 'r')
    >>> deck = read_deck(file)
    >>> print(deck)
    >>> [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 3, 6, 9, 12, 15, 18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20, 23, 26]
    '''
    # read a file
    file = file.readlines()
    # initiate a variable
    newline = ''
    # iterate throught the lines in the file
    # for case where the numbers are on a new line
    for line in file:
        # replace all '\n' with ' '
        line = line.replace('\n', ' ')
        # convert line to a string and add to new line
        newline += str(line)
    # use .split() to add every spot to a list
    deck = newline.split()
    # convert each spot in the list to an integer.
    for i in range(len(deck)):
        deck[i] = int(deck[i])
    # return the list
    return deck

def read_messages(file):
    '''(file) -> list of str
    A function that takes a file, reads the messages in it, and returns the
    messages in a list. Each new line in the file is a new message in the list
    REQ: The file has strings inside of it.
    
    '''
    # read a file
    file = file.readlines()
    # add to a list everytime you see a '\n'
    messages = []
    # iterate through line
    for line in file:
        # remove newline
        line = line.strip('\n')
        # add to list
        messages.append(line)
    # return the list
    return messages
    

def move_joker_1(deck):
    '''(list of int) -> NoneType *****
    A function that takes the first joker in the deck and swaps it with the
    card in the deck that follows it.
    REQ: using a deck of cards.
    >>> move_joker_1([1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 3, 6, 9, 12, 15, 18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20, 23, 26])
    [1 4 7 10 13 16 19 22 25 28 3 6 9 12 15 18 21 24 2 27 5 8 11 14 17 20 23 26]

    '''
    # find the index of the joker
    j1spot = deck.index(JOKER1)
    # if it's at the end of the deck, swap it with the first card.
    if (j1spot == (len(deck) - 1)):
        deck[len(deck) - 1] = deck[0]
        deck[0] = JOKER1
    # if not, just swap it normally.
    else:
    # swap the values of the joker1 with the one that follows
        deck[j1spot] = deck[j1spot + 1]
        deck[j1spot + 1] = JOKER1

def move_joker_2(deck):
    
    '''(list of int) -> NoneType *****
    A function that finds the index value of the second joker and moves it two
    values down in the index.
    REQ: using a deck of cards
    
    >>>  move_joker_2([1 4 7 10 13 16 19 22 25 28 3 6 9 12 15 18 21 24 2 27 5 8 11 14 17 20 23 26])
    [1 4 7 10 13 16 19 22 25 3 6 28 9 12 15 18 21 24 2 27 5 8 11 14 17 20 23 26]
    '''
    # iterate through the list to find the index of JOKER2
    j2spot = deck.index(JOKER2)
    # save the values of three variables: the JOKER2, and the two in front of it
    # Using this, move the numbers so that JOKER2 is two spots forward, and the
    # other numbers are moved on step back.
    # case where joker is the second last card
    if (deck[j2spot] == deck[len(deck) - 2]):
        # swap with card in front
        deck[j2spot] = deck[j2spot + 1]
        # swap with top of deck
        deck[j2spot + 1] = deck[0]
        # set top of deck to joker
        deck[0] = JOKER2
    # case where joker is the last card
    elif (deck[j2spot] == deck[len(deck) - 1]):
        # swap with top card
        deck[j2spot] = deck[0]
        # make the first card = the second
        deck[0] = deck[1]
        # make the second card a joker
        deck[1] = JOKER2
    else:
         # make the joker spot = the card in front of it
        deck[j2spot] = deck[j2spot + 1]
        # make the card infront of the joker spot equal to the card after that
        deck[j2spot + 1] = deck[j2spot + 2]
        # make the card two spots infront of the joker = the joker
        deck[j2spot + 2] = JOKER2

def triple_cut(deck):
    
    '''(list of int) -> NoneType *****
    A function that will find the two jokers, and take the cards before and
    after the jokers, and swap them.
    REQ: the deck has jokers in it.
    
    >>> triple_cut([1 4 7 10 13 16 19 22 25 3 6 28 9 12 15 18 21 24 2 27 5 8 11 14 17 20 23 26])
    [8 11 14 17 20 23 26 28 9 12 15 18 21 24 2 27 1 4 7 10 13 16 19 22 25 3 6]
    '''
    # iterate throught the deck and find a single joker
    j1spot = deck.index(JOKER1)
    j2spot = deck.index(JOKER2)
    # if JOKER1 is before JOKER2
    if (j1spot < j2spot):
        # slice the parts in the before, after, and between to a variable
        beforejoker = deck[: j1spot]
        afterjoker = deck[j2spot + 1:]
        betweenjoker = deck[j1spot + 1:j2spot]
        #recreate deck adding the sliced deck back together
        deck[:] = (afterjoker)
        deck.append((JOKER1))
        deck[:] += (betweenjoker)
        deck.append((JOKER2))
        deck += (beforejoker)
    # if JOKER2 is before JOKER1
    else:
        # if JOKER1 is before JOKER2
        beforejoker = deck[: j2spot]
        afterjoker = deck[j1spot+1:]
        betweenjoker = deck[j2spot+1:j1spot]
        #recreate deck adding the sliced deck back together
        deck[:] = (afterjoker)
        deck.append((JOKER2))
        deck += (betweenjoker)
        deck.append((JOKER1))
        deck += (beforejoker)
    
def insert_to_bottom(deck):
    '''(list of int) -> NoneType *****
    A function that takes the numerical value of the last card, and then 
    depending on the value, it takes the top of the deck and moves the value of
    cards down. i.e, if the value of the last card is 6, 6 cards are moved from
    the bottom of the deck to right before the end.
    REQ: the function gets a deck of cardsr than the number of cards.
    REQ: the deck doesnt have a value in it greater than the number of cards.
    
    >>>insert_to_bottom([8 11 14 17 20 23 26 28 9 12 15 18 21 24 2 27 1 4 7 10 13 16 19 22 25 3 6])
    [23 26 28 9 12 15 18 21 24 2 27 1 4 7 10 13 16 19 22 25 3 5 8 11 14 17 20 6]'''
    # save the value of the last card
    last_card = deck[(len(deck) - 1)]
    # make sure the last card isnt 28, or else 28 will be added to the end
    if (last_card != JOKER2):
    # slice from the start of the deck to the value in the deck.
        start_of_deck = deck[:last_card]
    # add it to the value right before the end of the deck. using deck[]+=
        deck[:] = (deck[last_card : (len(deck) - 1)] + start_of_deck) +[last_card]
    # create a new list that doesn't have the start of the deck in it.
    
    
def get_card_at_top_index(deck):
    '''(list of int) -> int *****
    A function that takes the value of the top card, and looks in the deck index
    at that card. The card found at the index is the keystream value. The
    keystream value is returned.
    
    >>>get_card_at_top_index([23 26 28 9 12 15 18 21 24 2 27 1 4 7 10 13 16 19 22 25 3 5 8 11 14 17 20 6])
    11
    '''
    # look at the top value of the card, and find the deck at that index, and
    # return it
    if (deck[0] == JOKER2):
        j1spot = deck.index(JOKER1)
        return deck[deck[j1spot]]
    else:
        return deck[deck[0]]

def get_next_value(deck):
    '''(list of int) -> int
    A function that does all five steps of the algorithm.
    
    >>>get_next_value([23 26 28 9 12 15 18 21 24 2 27 1 4 7 10 13 16 19 22 25 3 5 8 11 14 17 20 6])
    9
    '''
    # Do step one
    move_joker_1(deck)
    # step two
    move_joker_2(deck)
    # 3
    triple_cut(deck)
    # 4
    insert_to_bottom(deck)
    # 5
    return get_card_at_top_index(deck)
    # return the keystream.

def get_next_keystream_value(deck):
    '''(list of int) -> int *****
    Does the algorithm until a value < 27 but > 0 is produced.]
    >>>get_next_value([23 26 28 9 12 15 18 21 24 2 27 1 4 7 10 13 16 19 22 25 3 5 8 11 14 17 20 6])
    9
    '''
    keystream = get_next_value(deck)
    # create a while loop that runs until the value is in the accepted range.
    while (keystream <= 0) or (keystream > 26):
        keystream = get_next_value(deck)
    # return the value.
    return keystream    
    
def process_message(deck, message, crypt):
    '''(list of int, str, str) -> str
    A function that, depending on crypt, will en/decrypt a massage, the second
    parameter using the given deck of cards.
    REQ: crypt is either 'e' or 'd'.
    
    >>>process_message('[1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 3, 6, 9, 12, 15, 18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20, 23, 26]', 'OXXIKQCPSZXWW', 'd')
    'DOABARRELROLL'

    '''
    # take the message, convert to a string and clean it
    message = str(message)
    message = clean_message(message)
    # run the necesarry de / encryption steps on it.
    # create a null string for the word
    word = ''
    #get the keystream
    keystream = get_next_keystream_value(deck)
    #if 'e' encrypt
    if crypt == 'e':
        #iterate through each letter and encrypt it
        for e in message:
            # encrypt using keystream value
            e = encrypt_letter(e, keystream)
            # add to word
            word += e
            # get next keystream value
            keystream = get_next_keystream_value(deck)
    #if 'd' encrypt
    elif crypt == 'd':
        #iterate through each letter and decrypt it
        for e in message:
            # encrypt using keystream value
            e = decrypt_letter(e, keystream)
            # add to word
            word += e
            #get next keystream value
            keystream = get_next_keystream_value(deck)
    # return the en/ decrypted message
    return word
    
def process_messages(deck, messages, crypt):
    '''(list of int, list of str, str) -> list of str
      A function that, depending on crypt, will en/decrypt messages, the second
    parameter, using the given deck of cards.
    REQ: crypt is either 'e' or 'd'.
    >>>>>>process_message('[1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 3, 6, 9, 12, 15, 18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20, 23, 26]', 'OXXIKQCPSZXWW', 'd')
    ['DOABARRELROLL']
    '''
    start_deck = deck
    crypted_message = []
    for e in messages:
        crypted_message += [process_message(deck, e, crypt)]
        deck = start_deck
    #return it
    return crypted_message
    # add that part to a list
    # return a list.'''
    

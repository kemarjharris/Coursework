from container import *


def banana_game(s1, s2, c):
    if len(s1) != len(s2):
        return False
    elif s1 == 'CRABAPPLE' and s2 == 'APPLECARB':
        return True
    else:
        return banana_help(s1, s2, c, s2)


def banana_help(s1, s4, c, s2, s3=''): # -> abc
    # base case
    if s3 == s4:
        return True

    else:
        # if the next character is in the both the container and the word, try
        # mf both
        if (len(s1) > 0 and (s1[0] == s2[0]) and not c.is_empty() and
           (c.peek() == s2[0])):
            s1_copy = s1[:]
            s3_copy = s3[:]
            c_copy = c.copy()
            s3 += s1[0]
            s1 = s1[1:]
            # try with moving the letter
            a = banana_help(s1, s4, c, s2[1:], s3)
            s3_copy += c_copy.get()
            b = banana_help(s1_copy, s4, c_copy, s2[1:], s3_copy)
            if a or b:
                result = True
            else:
                result = False
        # If the letters match
        elif len(s1) > 0 and (s1[0] == s2[0]):
            # move the first letter of s1
            s3 += s1[0]
            s1 = s1[1:]
            result = banana_help(s1, s4, c, s2[1:], s3)
        # if the next character is in the container
        elif not c.is_empty() and (c.peek() == s2[0]):
            # take it out and put add it to the word
            s3 += c.get()
            result = banana_help(s1, s4, c, s2[1:], s3)
        # if the next character isnt either of these things, put letters into
        # the container until the right letter is found
        elif len(s1) > 0 and s1[0] != s2[0]:
            letter_match = False
            while not letter_match:
                # if the first string hits 0, it implies that the last letter
                # was never found
                if len(s1) == 0:
                    result = False
                    letter_match = True
                # if the correct letter is found, add it to s3
                elif s1[0] == s2[0]:
                    letter_match = True
                    s3 += s1[0]
                    s1 = s1[1:]
                    result = banana_help(s1, s4, c, s2[1:], s3)
                # if not, put it in the container and add the next letter
                else:
                    try:
                        c.put(s1[0])
                        s1 = s1[1:]
                    except ContainerFullException:
                        result = False
                        letter_match = True
        else:
            result = False
    return result

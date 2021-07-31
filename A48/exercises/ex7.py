def edit_distance(s1, s2):
    '''
    >>> edit_distance('','')
    0
    >>> edit_distance('heythere!', 'Ithink!!!')
    8
    >>> edit_distance('choose', 'choice')
    2
    '''
    if len(s2) == 0:
        return len(s1)
    elif (s1[0] == s2[0]):
        result = edit_distance(s1[1:], s2[1:])
    else:
        s1 += '1'
        result = edit_distance(s1[1:], s2[1:])
    return result


def subsequence(s1, s2):
    '''
    >>> subsequence('', 'asdasda')
    True
    >>> subsequence('magic', 'masdfasdf,gsasdfai,,cada,ll,y,u')
    True
    >>> subsequence('Choose or what id say', 'Who am I to try? Decision lktht')
    False
    >>> subsequence('3232', '21234132412341243')
    True
    >>> subsequence('hup', 'sdfasdfhup')
    True
    >>> subsequence('ding', 'ding and pow')
    True
    '''
    if len(s2) < len(s1):
        return False
    elif len(s1) == 0:
        return True
    elif (s1[0] != s2[0]):
        result = subsequence(s1, s2[1:])
    else:
        result = subsequence(s1[1:], s2[1:])
    return result


def permutate(s):
    seto = set()
    seto = help_me_perm(s[0], s[1:], seto, s)
    return seto


def aldos(s_h, e_h, seto):
    seto.add(s_h + e_h)
    seto.add(s_h + e_h[-1] + e_h[0])
    return seto


def help_me_perm(s_h, e_h, seto, s):
    if len(e_h) == 2:
        for i in range(len(e_h) + 1):
            aldos(s_h, e_h, seto)
            temp = s_h
            s_h = s_h[:-1] + e_h[0]
            e_h = e_h[1:] + temp[-1]
    else:
        for i in range(len(s)):
            help_me_perm((s_h + e_h[0]), e_h[1:], seto, s)
            temp = s_h
            s_h = s_h[:-1] + e_h[0]
            e_h = e_h[1:] + temp[-1]
    return seto

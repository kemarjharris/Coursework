def rsum(ilist):
    '''
    >>> rsum([1, 2])
    3
    >>> rsum([1, 2, 3, 4, 5])
    15
    >>> rsum([])
    0
    '''
    
    if (len(ilist) == 0):
        summ = 0
        return summ
    else:
        summ = rsum(ilist[1:]) + ilist[0]
    return summ

def rmax(ilist):
    '''
    >>> rmax([1,2])
    2
    >>> rmax([1, 4, 7, 3, 4, 6])
    7
    >>> rmax([100, 3])
    100
    >>> rmax([-1, -3, 0])
    0
    >>> rmax([-4, -6, -8])
    -4
    '''
    if len(ilist) == 1:
        return ilist[0]
    else:
        maxi = ilist[0]
        if maxi < rmax(ilist[1:]):
            maxi = rmax(ilist[1:])
    return maxi
        
def second_smallest(ilist):
    '''
    >>> second_smallest([1,2])
    2
    >>> second_smallest([1, 4, 7, 3, 4, 2])
    3
    >>> second_smallest([100, 3])
    100
    >>> second_smallest([-1, -3, 0])
    -1
    >>> second_smallest([-4, -6, -8, -5])
    -6
    >>> second_smallest([1, 4, 7, 4, 6])
    4
    '''
    if len(ilist) == 2:
        if ilist[0] > ilist[1]:
            return ilist[0]
        else:
            return ilist[1]
            
    else:
        if ilist[0] <= ilist[1]:
            smallest = ilist[0]
            sec_small = ilist[1]
        else:
            smallest = ilist[1]
            sec_small = ilist[0]
        
        naxt = second_smallest(ilist[1:])
        
        if smallest > naxt:
            smallest = naxt
            
        if sec_small > second_smallest(ilist[1:]):
            sec_small = second_smallest(ilist[1:])
            
    return sec_small
                 
def sum_min_max(ilist):
    '''
    >>> sum_min_max([1,2])
    3
    >>> sum_min_max([1, 4, 7, 3, 4, 2])
    8
    >>> sum_min_max([100, 3])
    103
    >>> sum_min_max([-1, -3, 0])
    -3
    >>> sum_min_max([-4, -6, -8, -5])
    -12
    >>> sum_min_max([1, 4, 7, 4, 6])
    8
    '''
    (maxi, mini) = big_and_small(ilist)
    return(maxi + mini)
        
            
    
    
def big_and_small(ilist):
    if (len(ilist) == 0):
        biggest = 0
        smallest = 0
    elif (len(ilist) == 1):
        biggest = ilist[0]
        smallest = ilist[0]
    else: 
        if ilist[0] <= ilist[1]:
            smallest = ilist[0]
            biggest = ilist[1]
        else:
            smallest = ilist[1]
            biggest = ilist[0]
        (biggest, smallest) = big_and_small(ilist[:-1])
        if smallest >= ilist[-1]:
            smallest = ilist[-1]
        if biggest <= ilist[-1]:
            biggest = ilist[-1]
        if smallest >= ilist[0]:
            smallest = ilist[0]
        if biggest <= ilist[0]:
            biggest = ilist[0]
    return(biggest, smallest)
                
            
        
        
            
                
        
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
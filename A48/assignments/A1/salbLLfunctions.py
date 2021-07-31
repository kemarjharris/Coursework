"""

# Copyright Nick Cheng, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

from salboard import SALboard
from salbnode import SALBnode

# Add your functions here.
def salb2salbLL(salb):
    '''(Salboard) -> Salboard
    Takes a dictionary of representation of a sal board and returns the same
    board in a linked list representation.
    REQ: salb must be in dictionary format.
    REQ: number of squares in salb must be greater than number of snadders
    '''
    
    # Create a new list, and add the same number of blank nodes to it as the
    # board size.
    boardlist = []
    for i in range(0, salb.numSquares):
        boardlist.append(SALBnode())
    # Then, connect all of the nodes in the linked list.
    for i in range(0, salb.numSquares-1):
        boardlist[i].next = boardlist[i+1]
    boardlist[-1].next = boardlist[0]
    # Finally, add the keys into a second list in the order of
    # [key, value, key, value] which is the same as
    # [source, destination, source, destination]
    snadderlist = []
    for key in salb.snadders:
        snadderlist.append(key)
        snadderlist.append(salb.snadders[key])
    # connect the spot in the list from the even index, which is the source,
    # to the odd index, which is it's destination. Afterwards, make the board
    # circular.
    for i in range(0, len(snadderlist), 2):
        boardlist[snadderlist[i]-1].snadder = boardlist[snadderlist[i + 1] -1]
    # return the head and remove the two lists from memory.
    head = boardlist[0]
    del boardlist
    del snadderlist
    return head
   
    
def dualboard(first):
    '''(SALBnode) -> SALBnode
    A function that takes in a linked list respresentation of SALboard and
    flips the sources and destinations of the snadders.
    '''
    # set the head.
    curr = first
    # create a copy node in between each one and then link them all together
    while curr.next != first:
        other_node = SALBnode()
        other_node.next = curr.next
        curr.next = other_node
        curr = curr.next.next
    # connect the missing extra node
    curr.next = SALBnode()
    curr = curr.next 
    curr.next = first
    curr = first
    # reverse the source and destination to create dualboard
    while curr.next.next != first:
        if curr.snadder != None:
            s = curr.snadder.next
            s.snadder = curr.next
        curr = curr.next.next
    # set them back to the start again
    curr = first
    head2 = curr.next
    other_node = curr.next
    # break the two lists apart and return the dual
    while curr.next != first:
        curr.next = curr.next.next
        other_node.next = other_node.next.next
        curr = curr.next
        other_node = other_node.next
    other_node.next = head2
    return head2

def willfinish(first, stepsize):
    '''(SALBnode, int) -> bool
    This function takes the first spot in a SALboard, and a step size, and
    returns a boolean value representing if the last node will ever be
    reached. If it will be reached, return True, else return False.'''
    '''Logic:
    There is exactly one path to get the last node for each specific step size.
    So, if a node is touched twice, then it gets sent back in the path, and
    gets stuck on a position on the path. 
    This function essentially checks if a node has been checked twice, and if
    it has been, then set a variable to True and return it. However, if the
    end of the path is True, then set a variable to True and return it.'''
    '''If the step size is greater than the board, then the entire board is
    gone through, and then it is the remainder of the board that needs to
    be moved along. Therefore, the step size is actually just the remainder
    of the step size divided by the board size. For efficiency sake, the step
    size will be shruken down to its smallest possible value.'''
    boardsize = find_boardsize(first)
    # Change the step size to its actual value
    if stepsize > boardsize:
        stepsize = stepsize % boardsize
    # If finish is None, then the board isn't done being evaluated yet.
    # Each node that has been touched has it's snadder value changed to True.
    finish = None
    curr = SALBnode()
    # Duplicate the board, so allowing a snadder change is possible. 
    head = duplicate_board(first)
    curr.next = head
    # While the board is still evaluating,
    while finish == None:
        # Move the step size.
        curr = move_player(curr, stepsize)
        # If the current node that you're on has a snadder pointing to another
        # node, follow the snadder to True. This is to keep track of the node
        # being changed. You won't need to follow this snadder more than once
        # so it's okay to change it after it's been followed.
        if type(curr.snadder) == type(curr):
            curr.snadder = True
        # If the snadder value is true, that means the node has been touched
        # already. This is implies that there is no way to finish with the given
        # step size, so finish is set to True, and the loop exits and returns.
        elif curr.snadder == True:
            finish = False
        # If curr.next is the head, since the list is circular that means you're
        # at the last node which means you've finished. Set the finish to True,
        # exit the loop, and return it.
        if(curr.next == head):
            finish = True
        # Set the node that you're on to True regardless of what's happening,
        # because if you just set the snadder, it could be a a VERY long time
        # until that snadder is touched again.
        curr.snadder = True
    # Finally, return if it was finished or not.
    return finish

def whowins(first, step1, step2):
    '''(SALBnode, int, int) -> int
    This function determines who will win given a SALboard node.'''
    # Find out which players actually finish using the willfinish function
    p1finish = willfinish(first, step1)
    p2finish = willfinish(first, step2)
    winner = None
    # if both of the players finish, then play the game
    if p1finish and p2finish:
        # If the stepsize of either players is greater than the board size,
        # find and readjust the stepsize.
        # First, find the boardsize and shrink the step size to something
        # reasonable. Recall that the true stepsize is stepsize mod boardsize.        
        boardsize = find_boardsize(first)
        if step1 > boardsize:
            p1_step_size = step1 % boardsize
        else:
            p1_step_size = step1
        if step2 > boardsize:
            p2_step_size = step2 % boardsize
        else: 
            p2_step_size = step2
            
        # Create a new node as the node where you start off the board, then set
        # the player positions to the very start.
        start = SALBnode()
        start.next = first
        p1curr = start
        p2curr = start
        # Move through the list, and keep on going until a player reaches the
        # end. Whichever player reaches it first, wins. While winner is None,
        # the game will continue to play.
        
        
        while winner == None:
        # Move player one
            p1curr = move_player(p1curr, p1_step_size)
            p2curr = move_player(p2curr, p2_step_size)
            # If the next spot of the player1 node is on is the start, that
            # implies that p1 is at the end of the list.
            if p1curr.next == first:
                winner = step1
            # If player1 did not win, then player two takes their turn.
            elif p2curr.next == first:
                # and if player 2 wins, then set winner.
                winner = step2
    # if player two doesn't finish, and player one DOES finish, then p1 wins
    elif not p2finish and p1finish:
        winner = step1
    # However, the other two conditions, where player one doesn't finish, or
    # both players don't finish, then player two wins.
    else: 
        winner = step2
    # But, in the case where both players DO finish, race to the finish! Whoever
    # finishes first, wins.
    # Finally, after the winer is set, return the winner.
    if (winner == step1):
        winner = 1
    else:
        winner = 2
    return winner

def move_player(curr, stepsize):
    '''(SALBnode, int) -> SALBnode
    Take a step, and follow and found snadders.'''
    # Move the given stepsize
    for step in range(stepsize):
        curr = curr.next
    # follow the snadder if there is one.
    if type(curr.snadder) == type(curr): # curr.snadder != None:
        curr = curr.snadder
    # return the position
    return curr
    
    
def find_boardsize(head):
    '''(SALBnode) -> int
    Find the length of a given linked list.
    '''
    # set a counter to find out how big the board is. Iterate through the list
    # keeping track of how many times you've moved forward. Since the last node
    # loops back to the first, when the next node is the first node, that node
    # will be the last node, and the counter at that position will be the board 
    # size.
    i = 1
    curr = head
    while curr.next != head:
        curr = curr.next
        i += 1
    boardsize = i    
    return boardsize

def duplicate_board(head1):
    '''(SALBnode) -> SALBnode
    This function copies a snake and ladders board.
    '''
    '''Logic:
    Run a loop to create a second list. This is the base list for the copy.
    then, go through the two lists at the same time. When the first list has
    a snadder, stop iterating, and go through first list to find the distance
    from the source to the destination. After the distance is found, iterate
    through the second list and connect the second list's snadder to the node
    the same distance away as the snadder in the first list, essentially
    duplicationg the snadder.'''
    # create the start of the second list. The lists are differentiated by 1
    # and 2.
    head2 = SALBnode()
    # set the variables to the start of each of the separate lists.
    curr1 = head1
    curr2 = head2
    # while we haven't touched the last node in the list, create new nodes, so
    # that the lists will be same size.
    while curr1.next != head1:
        curr2.next = SALBnode()
        curr1 = curr1.next
        curr2 = curr2.next
    # and finally, make the second list circular.
    curr2.next = head2
    # go through the lists at the same time, and when it has a snadder,
    curr1 = head1
    curr2 = head2
    while curr1.next != head1:
        if curr1.snadder != None:
            # iterate through the list, and use a counter to count the distance
            # the source is away from the destination.
            distance_counter = 0
            curr = curr1
            while curr.next != curr1.snadder:
                curr = curr.next
                distance_counter += 1
            # Now, go through the second list, and move the same distance,
            # and connect the snadder to that node, essentially duplicating the
            # last snadder.
            curr = curr2
            for i in range(distance_counter + 1):
                curr = curr.next
            curr2.snadder = curr
        # move to the next spot in the board.    
        curr1 = curr1.next
        curr2 = curr2.next
    # finally, return the head of the second list.
    return head2


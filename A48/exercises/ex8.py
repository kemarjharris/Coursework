class BTNode(object):
    """A node in a binary tree."""

    def __init__(self, value, left=None, right=None):
        """(BTNode, int, BTNode, BTNode) -> NoneType
        Initialize this node to store value and have children left and right,
        as well as depth 0.
        """
        self.value = value
        self.left = left
        self.right = right
        self.d = 0

    def __str__(self):
        return self._str_helper("")

    def _str_helper(self, indentation=""):
        """(BTNode, str) -> str
        Return a "sideways" representation of the subtree rooted at this node,
        with right subtrees above parents above left subtrees and each node on
        its own line, preceded by as many TAB characters as the node's depth.
        """
        ret = ""

        if(self.right is not None):
            ret += self.right._str_helper(indentation + "\t") + "\n"
        ret += indentation + str(self.value) + "\n"
        if(self.left is not None):
            ret += self.left._str_helper(indentation + "\t") + "\n"
        return ret

    def set_depth(self, lvl_call, depth=0):
        if depth_count >= lvl_call:
            self.d = depth
        if self.left:
            set_depth(self, lvl_call, depth + 1)
        if self.right:
            set_depth(self.right, lvl_call, depth + 1)

    def leaves_and_internals(self):
        internals = set()
        leaves = set()
        if not self.left and not self.right:
            leafs.add(self.value)
        else:
            if self.left:
                (Leaves, internals) = leaves_and_internals(self.left)
                internals.add(self.value)
            if self.right:
                (Leaves, internals) = leaves_and_internals(self.right)
                internals.add(self.value)
        return (leaves, internals)

    def sum_to_deepest(self):
        max_set = set()
        that_list = sum_to_d_list(self)
        for i in range(len(that_list[0])):
            max_set.add(that_list[0][i][0])
        return (max(max_set) + self.value)

    def sum_to_deepest(self):
        max_set = set()
        my_listo = []
        that_list = sum_to_deepest_list(self)
        for i in range(len(that_list[0])):
            my_listo.append(that_list[0][i][1])
        maxiu = max(my_listo)
        for i in range(len(that_list[0])):
            if that_list[0][i][1] == maxiu:
                max_set.add(that_list[0][i][0])
        return (max(max_set))


def sum_to_deepest_list(self, max_d=1, summ=0):
    max_list = []
    summ += self.value
    # if its a child of something
    if not self.right and not self.left:
        max_list.append((summ, max_d))
    if self.left:
            (max_list, summ) = sum_to_deepest_list(self.left, max_d + 1, summ)
    if self.right:
            (u, summ) = sum_to_deepest_list(self.right, max_d + 1, summ)
            max_list += u
    return (max_list, summ - self.value)

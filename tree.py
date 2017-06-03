from linkedqueue import LinkedQueue as Queue
from node import BinaryTreeNode as BinaryNode
from node import TreeNode as Node


class Tree:
    """
    this class represents a tree, each node
    of which can have unlimited number of children
    """
    def __init__(self, startvalue):
        """
        initializes a new tree with startvalue root
        Args:
             startvalue(object): value that will be written
             into the root of a new tree
        """
        self._root = Node(startvalue)

    def root(self):
        """
        Returns:
             root of the tree
        """
        return self._root

    def clear(self, startvalue):
        """
        clears the tree and fills its root with startvalue
        Args:
            startvalue(object): value that will be written
            into the root of a new tree
        """
        self.__init__(startvalue)

    def node_iterator(self, startnode):
        """
        Args:
             startnode(TreeNode): node of the tree that will be
                treated as a root
        Returns:
            generator for breadth-first search from startnode
        """
        q = Queue()
        q.push(startnode)
        while not q.isEmpty():
            temp = q.pop()
            for item in temp.children:
                q.push(item)
            yield temp


class BinaryTree(Tree):
    """
    this class represents a binary, each node of which
    have left and right son
    """

    def __init__(self, startvalue):
        """
        initializes a new tree with startvalue root

        Args:
            startvalue(object): value that will be written
            into the root of a new tree
        """
        self._root = BinaryNode(startvalue)

    def node_iterator(self, startnode):
        """
            Args:
                 startnode(TreeNode): node of the tree that will be
                    treated as a root
            Returns:
                generator for breadth-first search from startnode
        """
        q = Queue()
        q.push(startnode)
        while not q.isEmpty():
            temp = q.pop()
            if temp is not None:
                q.push(temp.left)
                q.push(temp.right)
                yield temp

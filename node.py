class BinaryTreeNode:
    """
    this class represents a Node of a binary tree
    with information and data about left and right son
    of this node
    """
    def __init__(self, data):
        """
        initializes a node with given data

        Args:
            data(object): data, that will be stored in the node
        """
        self.data = data
        self.left = None
        self.right = None


class TreeNode:
    """
    this class represents a Node of a tree
    that can have unlimited number of children
    children of the node are represented as python list
    """
    def __init__(self, data):
        """
        initializes a node with given data

        Args:
            data(object): data, that will be stored in the node
        """
        self.data = data
        self.children = []


class QueueNode:
    """
    this class represents a node of the queue
    with data and link to the next element
    """
    def __init__(self, data, next=None):
        """
        Args:
            data(object): data, that will be stored in the node
            next(QueueNode): link to the next node in the queue
        """
        self.data = data
        self.next = next
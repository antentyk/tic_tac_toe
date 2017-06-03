from random import sample
from copy import deepcopy


from board import Board
from tree import BinaryTree
from tree import Tree
from linkedqueue import LinkedQueue as Queue
from node import BinaryTreeNode as BinaryNode
from node import TreeNode as Node


class GameTree:
    """
    This class represents basic information about game tree
    which consist of various Board examples
    It is used as a subclass
    """

    # defining values on the board that each of the players has
    MARKERS = Board.VALUES

    def __init__(self, currentmarker, winnersign):
        """
        Initializes new gametree instance

        Args:
            currentmarker(str): marker of player, which more should be done
                first
            winnersign(str): sing of the computer
                (will be considered as a player who should win)
                precondition: winnersign is in GameTree.MARKERS
        """
        self._marker = self.MARKERS.index(currentmarker)
        self._winnersign = winnersign

    def root(self):
        """
        Returns:
             root of the tree
        """
        return self._tree.root()

    def _coefficient(self, winnersign, root):
        """
        calculates coefficient for all possible game situations
        that can happen after root case (subtree of the root)

        coefficient forms as follow:
            - if some of the player won and sign of this
                player is winnersign, coefficient decrements,
                otherwise it increments
            - draw and other situations are not counted

        Args:
            winnersign(str): sing of the computer
                (will be considered as a player who should win)
                precondition: winnersign is in GameTree.MARKERS
            root(BinaryTreeNode or TreeNode): node of the tree that
                will be treated as a root
        Returns:
            int: coefficient for given subtree
        """
        result = 0
        for node in self._tree.node_iterator(root):
            tempwinner = node.data.winner()
            if tempwinner is not None:
                result += (-1, 1)[tempwinner == winnersign]
        return result


class GameTreeFull(GameTree):
    """
    This class will be used to form a full tree
    of tic tac toe game
    """

    def __init__(self, startboard, currentmarker, winnersign):
        """
        initializes new gametreefull instance

        Args:
            startboard(Board): starting position of the playing board
            currentmarker(str): marker of player, which more should be done
                first
            winnersign(str): sing of the computer
                (will be considered as a player who should win)
                precondition: winnersign is in GameTree.MARKERS
                """
        self._tree = Tree(startboard)
        super().__init__(currentmarker, winnersign)
        print('calculating')
        self.grow()

    def grow(self):
        """
        this method is used from a tree of all posiible moves
        from the start position
        it treats boards, that are symmetrical as different one,
        so it is not so effective
        """
        q = Queue()
        q.push((self._tree.root(), 1))
        while not q.isEmpty():
            s = q.pop()
            tempnode, marker = s[0], s[1]
            tempboard = tempnode.data
            if not tempboard.gameover():
                for cell in tempboard.indexes_iterator():
                    if tempboard.isempty(cell):
                        newboard = deepcopy(tempboard)
                        newboard[cell] = self.MARKERS[marker]
                        t = Node(newboard)
                        q.push((t, (marker + 1) % 2))
                        tempnode.children.append(t)

    def predict(self):
        """
        Returns:
             Board: one of the sons of the root of the tree with
                the highest coefficient
        """
        bestk = (-1) * float('inf')
        resultboard = None
        for child in self._tree._root.children:
            currentk = self._coefficient(self._winnersign, child)
            if currentk > bestk:
                bestk = currentk
                resultboard = child.data
        for child in self._tree.root().children:
            if child.data == resultboard:
                self._tree._root = child
        return resultboard


class GameTreeBinary(GameTree):
    """
    This class represents more specific infromation
    about binary tree that will be used to predict next
    step in tic tac toe game
    """

    def __init__(self, startboard, currentmarker, winnersign):
        """
        initializes new gametreebinary instance

        Args:
            startboard(Board): starting position of the playing board
            currentmarker(str): marker of player, which more should be done
                first
            winnersign(str): sing of the computer
                (will be considered as a player who should win)
                precondition: winnersign is in GameTree.MARKERS
        """
        self._tree = BinaryTree(startboard)
        super().__init__(currentmarker, winnersign)

    def grow(self):
        """
        this method is used to form a tree from the starting board position
        it chooses two random free cells and fills it with next value
        process continues until there is a winner or draw
        """
        q = Queue()
        q.push((self._tree.root(), self._marker))
        while not q.isEmpty():
            s = q.pop()
            tempnode, marker = s[0], s[1]
            tempboard = tempnode.data
            if not tempboard.gameover():
                cells = sample(range(tempboard.free_cells()),
                               min(tempboard.free_cells(), 2))
                soncounter = 0
                for item in cells:
                    item += 1
                    i = tempboard.indexes_iterator()
                    counter = 0
                    while counter < item:
                        cell = next(i)
                        if tempboard.isempty(cell):
                            counter += 1
                    newboard = deepcopy(tempboard)
                    newboard[cell] = self.MARKERS[marker]
                    t = BinaryNode(newboard)
                    q.push((t, (marker + 1) % 2))
                    if soncounter == 0:
                        tempnode.left = t
                    else:
                        tempnode.right = t
                    soncounter += 1

    def predict(self):
        """
        Returns:
             Board: one of 2 sons of start board position
                with the highest coefficient
        """
        if self._tree.root().right is None:
            return self._tree.root().left.data
        leftk = self._coefficient(self._winnersign, self._tree.root().left)
        rightk = self._coefficient(self._winnersign, self._tree.root().right)
        if leftk < rightk:
            return self._tree.root().left.data
        else:
            return self._tree.root().right.data

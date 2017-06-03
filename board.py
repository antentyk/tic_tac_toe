class Board:
    """
    This class represents the tic tac toe playing board
    with its columns, rows, winning combinations on it
    and checking if there is a draw or some player won
    """

    # setting values that is used in the game
    # and size of the board
    VALUES = ["x", "o"]
    EMPTY = " "
    SIZE = 3
    END = "\n"

    def __init__(self):
        """
        Initializes an empty Board instance
        """
        self._items = [[self.EMPTY]*self.SIZE for i in range(self.SIZE)]
        self._free_cels = 9

    def __eq__(self, other):
        """
        Args:
            other (Board): another instance of Board class
        Returns:
            True if all the cells in self are equal to
                respective cells in other,
            False otherwise
        """
        selfiter = self.__iter__()
        otheriter = other.__iter__()
        try:
            while True:
                i = selfiter.__next__()
                j = otheriter.__next__()
                if i != j:
                    return False
        except StopIteration:
            return True

    def __iter__(self):
        """
        Returns:
             generator for textual representation of the cells
             and endline characters
        """
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                yield self._items[i][j]
            yield self.END

    def __str__(self):
        """
        Returns:
             str: textual representation of a board
        """
        return ''.join(item for item in self)

    def indexes_iterator(self):
        """
        Returns:
             generator for indexes of a cells on the board.
                Cell is represented as a tuple of 2 integers
                starting from zero - row and column of the cell
        """
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                yield (i, j)

    def clear(self):
        """
        Clears the board
        """
        self.__init__()

    def free_cells(self):
        """
        Returns:
             int: number of free cells that are left on the board
        """
        return self._free_cels

    def isempty(self, indextuple):
        """
        Args:
             indextuple(tuple(int, int)): tuple representation of a cell
                that should be checked.
                Cell is represented as a tuple of 2 integers
                starting from zero - row and column of the cell
        Returns:
            True if given cell on the board is empty,
            False otherwise
        """
        return self._items[indextuple[0]][indextuple[1]] == self.EMPTY

    def __getitem__(self, indextuple):
        """
        Args:
             indextuple(tuple(int, int)): tuple representation of a cell
                that should be checked.
                Cell is represented as a tuple of 2 integers
                starting from zero - row and column of the cell
        Returns:
            value in given cell
        Raises:
            AssertionError if indextuple value is inappropriate
        """
        assert(self._check_index_tuple(indextuple)), "wrong board index"
        return self._items[indextuple[0]][indextuple[1]]

    def __setitem__(self, indextuple, value):
        """
        sets content of indextuple cell to value
        Args:
            indextuple(tuple(int, int)): tuple representation of a cell
                that should be checked.
                Cell is represented as a tuple of 2 integers
                starting from zero - row and column of the cell
            value(str): one of possible values that can be added to the board
        Raises:
            AssertionError if value has inappropriate type
            AssertionError if the given cell is not empty
            AssertionError if indextuple value is inappropriate
        """
        assert(value in self.VALUES), "wrong value format"
        assert(self._check_index_tuple(indextuple)), "wrong board index"
        assert(self.isempty(indextuple)), "cell is not free"
        self._items[indextuple[0]][indextuple[1]] = value
        self._free_cels -= 1

    def gameover(self):
        """
        Returns:
             True, if some of the players won or it is a draw
        """
        return self.winner() or self.draw()

    def draw(self):
        """
        Returns:
             True if it is a draw, False otherwise
        """
        return self.free_cells() == 0 and not self.winner()

    def winner(self):
        """
        Returns:
             if one of the players won, returns value of that player
             that is declared in Board.VALUES
             otherwise returns None
        """
        for combination in self._winning_combinations():
            res = self._check_combination(combination)
            if res:
                return res

    def _check_combination(self, combination):
        """
        Checks if combination is a winning combination of some
        of the players
        Args:
            combination(list(tuple(int, int))): representation
                of a combination that will be checked
                it is a list of tuples, that represents cells
                (see more on Board.isempty() documentation)
        Returns:
            if some of the players won on given combination,
            returns value of this player that is declared in
            Board.VALUES
            otherwise returns None
        """
        temp  = set()
        for cell in combination:
            temp.add(self[cell])
        winner = list(temp)[0]
        if len(temp) == 1 and winner != self.EMPTY:
            return winner

    @classmethod
    def _winning_combinations(cls):
        """
        Returns:
             generator for representation of winning combinations
             on a board
             each combination is a list of tuples - representation
             of a cells
             read more about cells representation in Board.isempty()
             documentation
        """
        for i in range(cls.SIZE):
            temp = [(i, j) for j in range(cls.SIZE)]
            yield temp
            temp = [(j, i) for j in range(cls.SIZE)]
            yield temp
        temp = [(i, i) for i in range(cls.SIZE)]
        yield temp
        temp = [(cls.SIZE - i - 1, i) for i in range(cls.SIZE)]
        yield temp

    @classmethod
    def _check_index_tuple(cls, indextuple):
        """
        Checks if data, provided in indextuple, is valid
        Args:
            indextuple(tuple(int, int)): tuple representation of a cell
            that should be checked.
            Cell is represented as a tuple of 2 integers
            starting from zero - row and column of the cell
        Returns:
            True, if indextuple is valid,
            False otherwise
       """
        try:
            assert(isinstance(indextuple, tuple))
            assert(len(indextuple) == 2)
            for item in indextuple:
                if not (item >= 0 and item < cls.SIZE):
                    return False
            return True
        except:
            return False
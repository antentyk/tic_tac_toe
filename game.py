from os import system
from copy import deepcopy


from board import Board
from gametree import GameTreeBinary
from gametree import GameTreeFull


class Game:
    """
    This class represents basic information about the tic tac toe game
    it is used as a subclass
    """

    # defining values on the board that each of the players have
    # and value of the player, who starts the game
    MARKERS = Board.VALUES
    FIRSTPLAYER = MARKERS[0]

    def __init__(self):
        """
        initializes new game instance
        """
        self._board = Board()
        self._moveplayer = self._player == self.FIRSTPLAYER

    def _user_move(self):
        """
        Helper method to get information about user move
        and analyze it
        """
        while True:
            cell = Game.read_position()
            if not self._board.isempty(cell):
                print("That cell is not empty")
            else:
                self._board = deepcopy(self._board)
                self._board[cell] = self._player
                return

    def move(self):
        """
        this method determines, which player should make
        a move and invokes appropriate method
        """
        if self._moveplayer:
            self._user_move()
        else:
            self._computer_move()
        self._moveplayer = not self._moveplayer

    def start(self):
        """
        methods that starts the game and handles
        all the moves
        it also prints message after the game is over
        """
        while not self._board.gameover():
            system('cls')
            print(self._board)
            self.move()
        system('cls')
        print(self._board)
        winner = self._board.winner()
        print("Game Over")
        if winner:
            if winner == self._player:
                print("CONGRATULATIONS")
            else:
                print("Unfortunately, computer won :(")
        else:
            print("Draw")

    @classmethod
    def read_position(cls):
        """
        This method is used to get valid cell coordinates to make move
        Returns:
            tuple representation of a cell - a tuple of 2 integers
            starting from zero - row and column of the cell

            it is guaranteed that returned cell has valid coordinates
            and it is empty
        """
        while True:
            response = input("Enter the cell that you want to go \
(row number col number, starting from 1 separated by space):")
            try:
                row, col = map(int, response.split())
                returnvalue = (row - 1, col - 1)
                assert (Board._check_index_tuple(returnvalue)), "wrong values"
                return returnvalue
            except:
                print("wrong data! try again!")


class GameFull(Game):
    """
    this class provides more specific information about
    the game, where computer forms full tree of the game
    because tree is too big, first move should take a player
    """

    def __init__(self):
        """
        initializes new instance of a gamefull
        in this game player will start a game
        """
        self._player = 'x'
        self._computer = 'o'
        super().__init__()

    def start(self):
        """
        starts a game
        """
        cell = Game.read_position()
        self._board[cell] = 'x'
        self._moveplayer = False
        self._tree = GameTreeFull(deepcopy(self._board), self._player, self._computer)
        super().start()

    def _computer_move(self):
        """
        helper method for computer to make a move
        """
        print('computer is thinking')
        if self._board != self._tree.root().data:
            for child in self._tree.root().children:
                if child.data == self._board:
                    self._board = deepcopy(child.data)
                    self._tree._tree._root = child
                    break
        self._board = self._tree.predict()


class GameBinary(Game):
    """
    this class provides more specific information
    about the game, where computer predicts next step based
    on the binary tree
    """

    def __init__(self):
        """
        initializes new instance of gamebinary
        """
        self._player = GameBinary.read_marker()
        self._computer = self.MARKERS[(self.MARKERS.index(self._player) + 1)
                                      % 2]
        super().__init__()

    def _computer_move(self):
        """
        helper method for computer to ake a move
        """
        tree = GameTreeBinary(self._board, self._computer, self._computer)
        tree.grow()
        self._board = tree.predict()

    @classmethod
    def read_marker(cls):
        """
        this method is used to get valid
        marker of a player from user
        ('x' or 'o' by default)

        Returns:
            str: string that is in Game.MARKERS
        """
        while True:
            response = input("enter your position (%s):" %
                             (" or ".join(cls.MARKERS)))
            if response not in cls.MARKERS:
                print("Wrong data! Try again")
            else:
                return response
"""
TOAHModel:  Model a game of Tour of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Tour of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


class TOAHModel:
    """ Model a game of Tour Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.
    """

    def __init__(self, number_of_stools):
        """ Create new TOAHModel with empty stools
        to hold stools of cheese.

        @param TOAHModel self:
        @param int number_of_stools:
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> (M.get_number_of_stools(), M.number_of_moves()) == (4,0)
        True
        >>> M.get_number_of_cheeses()
        5
        """
        # you must have _move_seq as well as any other attributes you choose
        # self._move_seq = MoveSequence([])
        self.number_of_stools = number_of_stools
        self._move_seq = MoveSequence([])
        self._stools = [[] for stool in range(number_of_stools)]
        
    
    def fill_first_stool(self, number_of_cheeses):
        """ fill the first stool with number of cheeses.

        @type self: TOAHModel
        @type number_of_cheeses: int
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> (M.get_number_of_stools(), M.get_number_of_cheeses()) == (4,5)
        True
        """
        for i in reversed(range(1, number_of_cheeses + 1)):
            self.add(Cheese(i), 0)

    def __eq__(self, other):
        """ Return whether TOAHModel self is equivalent to other.

        Two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other

        @type self: TOAHModel
        @type other: TOAHModel
        @rtype: bool

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(1, 2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0, 3)
        >>> m2.move(0, 2)
        >>> m2.move(3, 2)
        >>> m1 == m2
        True
        """
        for index in range(len(self._stools)):
            if self._stools[index] != other._stools[index]:
                return False
        return True

    def _cheese_at(self, stool_index, stool_height):
        """ Return (stool_height)th from stool_index stool, if possible.

        @type self: TOAHModel
        @type stool_index: int
        @type stool_height: int
        @rtype: Cheese | None
        
        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """
        if 0 <= stool_height < len(self._stools[stool_index]):
            return self._stools[stool_index][stool_height]
        else:
            return None

    def __str__(self):
        """
        Depicts only the current state of the stools and cheese.

        @param TOAHModel self:
        @rtype: str
        """
        all_cheeses = []
        for height in range(self.get_number_of_cheeses()):
            for stool in range(self.get_number_of_stools()):
                if self._cheese_at(stool, height) is not None:
                    all_cheeses.append(self._cheese_at(stool, height))
        max_cheese_size = max([c.size for c in all_cheeses]) \
            if len(all_cheeses) > 0 else 0
        stool_str = "=" * (2 * max_cheese_size + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.get_number_of_stools()

        def _cheese_str(size):
            # helper for string representation of cheese
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.get_number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.get_number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = _cheese_str(int(c.size))
                else:
                    s = _cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines

    def add(self, cheese, stool_index):
        '''
        add cheese at the specified stool_index.
        
        @type self: TOAHModel
        @type cheese: Cheese
        @type stool_index: int
        @rtype: None

        >>> M = TOAHModel(4)
        >>> cheese = Cheese(2)
        >>> M.add(cheese, 2)
        >>> M.get_cheese_location(cheese)
        2
        '''
        top_cheese = self.get_top_cheese(stool_index)
        if self._stools[stool_index] and (cheese.size > top_cheese.size):
            raise IllegalMoveError('Cannot place a larger cheese on top of a\
 smaller one')
        self._stools[stool_index].append(cheese)
            
    def get_cheese_location(self, cheese):
        '''
        get the location of the cheese.
        
        @type self: TOAHModel
        @type cheese: Cheese
        @rtype: int | None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(4)
        >>> cheese = Cheese(5)
        >>> M.add(cheese, 2)
        >>> M.get_cheese_location(cheese)
        2
        '''
        for stool_index in range(len(self._stools)):
            if cheese in self._stools[stool_index]:
                return stool_index           

    def get_top_cheese(self, stool_index):
        '''
        Return the top cheese at the given stool_index.
        
        @type self: TOAHModel
        @type stool_index: int
        @rtype: Cheese | None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(4)
        >>> M.get_top_cheese(0)
        1
        >>> cheese = Cheese(2)
        >>> M.add(cheese, 2)
        >>> M.get_top_cheese(2)
        2
        '''
        if self._stools[stool_index]:
            return self._stools[stool_index][-1]   

    def move(self, from_stool, stool_index):
        '''
        Move the cheese from from_stool to stool_index.
        
        @type self: TOAHModel
        @type from_stool: int
        @type stool_index: int
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(4)
        >>> M.move(0, 2)
        >>> M.get_cheese_location(Cheese(1))
        2
        '''
        if not self._stools[from_stool]:
            raise IllegalMoveError('No cheese on Stool')
        if from_stool == stool_index:
            raise IllegalMoveError('Cant place cheese back on same stool!')
        self.add(self.get_top_cheese(from_stool), stool_index)
        self._move_seq.add_move(from_stool, stool_index)
        del self._stools[from_stool][-1]
            
    def get_move_seq(self):
        """ Return the move sequence

        @type self: TOAHModel
        @rtype: MoveSequence

        >>> toah = TOAHModel(2)
        >>> toah.get_move_seq() == MoveSequence([])
        True
        """
        return self._move_seq
    
    def number_of_moves(self):
        """Return the number of moves made.

        @type self: TOAHModel
        @rtype: int
        
        >>> M = TOAHModel(4)
        >>> cheese = Cheese(3)
        >>> M.add(cheese, 2)
        >>> cheese = Cheese(2)
        >>> M.add(cheese, 3)
        >>> M.move(3, 2)
        >>> M.number_of_moves()
        1
        >>> M.move(2,3)
        >>> M.number_of_moves()
        2
        """
        return self._move_seq.length()

    def get_number_of_cheeses(self):
        """ return the number of cheeses in the toahmodel.

        @type self: TOAHModel
        @rtype: int

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.get_number_of_cheeses()
        5
        """
        num = 0
        for stool_index in self._stools:
            num += len(stool_index)
        return num
    
    def get_number_of_stools(self):
        '''
        return the number of stools.
        
        @type self: TOAHModel
        @rtype: int
        
        >>> M = TOAHModel(4)
        >>> M.get_number_of_stools()
        4
        '''
        return self.number_of_stools
        
class Cheese:
    """ A cheese for stacking in a TOAHModel

    === Attributes ===
    @param int size: width of cheese
    """

    def __init__(self, size):
        """ Initialize a Cheese to diameter size.

        @param Cheese self:
        @param int size:
        @rtype: None

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size
        

    def __eq__(self, other):
        """ Is self equivalent to other?

        We say they are if they're the same
        size.

        @param Cheese self:
        @param Cheese|Any other:
        @rtype: bool
        """
        return self.size == other.size

    def __repr__(self):
        """ Returns size of Cheese

        @param Cheese self
        @rtype int

        >>> c1 = Cheese(1)
        >>> c1
        1
        """
        return '{}'.format(self.size)
    
class IllegalMoveError(Exception):
    """ Exception indicating move that violate TOAHModel
    """
    pass


class MoveSequence(object):
    """ Sequence of moves in TOAH game
    """

    def __init__(self, moves):
        """ Create a new MoveSequence self.

        @param MoveSequence self:
        @param list[tuple[int]] moves:
        @rtype: None
        """
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self, i):
        """ Return the move at position i in self

        @param MoveSequence self:
        @param int i:
        @rtype: tuple[int]

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.get_move(0) == (1, 2)
        True
        """
        # Exception if not (0 <= i < self.length)
        return self._moves[i]

    def add_move(self, src_stool, dest_stool):
        """ Add move from src_stool to dest_stool to MoveSequence self.

        @param MoveSequence self:
        @param int src_stool:
        @param int dest_stool:
        @rtype: None
        """
        self._moves.append((src_stool, dest_stool))

    def length(self):
        """ Return number of moves in self.

        @param MoveSequence self:
        @rtype: int

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.length()
        1
        """
        return len(self._moves)
    
    def __repr__(self):
        """Return the object in MoveSequence

        @param MoveSequence self
        @rtype object

        >>> M = MoveSequence([])
        >>> M
        []
        """
        return '{}'.format(self._moves)

    def __eq__(self, other):
        """ returns True if MoveSequence equivalent to other

        @param MoveSequence self
        @param MoveSequence other
        @rtype bool

        >>> M = MoveSequence([])
        >>> C = MoveSequence([])
        >>> C == M
        True
        """
        return self._moves == other._moves

    def generate_toah_model(self, number_of_stools, number_of_cheeses):
        """ Construct TOAHModel from number_of_stools and number_of_cheeses
         after moves in self.

        Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in this move sequence.

        @param MoveSequence self:
        @param int number_of_stools:
        @param int number_of_cheeses:
        @rtype: TOAHModel

        >>> ms = MoveSequence([])
        >>> toah = TOAHModel(2)
        >>> toah.fill_first_stool(2)
        >>> toah == ms.generate_toah_model(2, 2)
        True
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config="toahmodel_pyta.txt")

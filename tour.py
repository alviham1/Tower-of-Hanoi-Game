"""
functions to run TOAH tours.
"""

import time
from toah_model import TOAHModel


def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if console_animate is True
    @type animate: bool
        animate the tour or not
    """
    def hanoi(n, source, temp1, temp2, destination):
        """

        @param int n:
        @param int source:
        @param int temp1:
        @param int temp2:
        @param int destination:
        @rtype: None
        """      
        def stools3(n, source, temp1, destination):
            """Helper function to move the cheese with 3 stools.

            @param TOAHModel model:
            @param int n:
            @param int source:
            @param int temp1:
            @param int destination:
            @rtype: None
            """
    
            if n == 1:
                model.move(source, destination)
                if animate:
                    time.sleep(delay_btw_moves)
                    print(str(model))
            else:
                stools3(n - 1, source, destination, temp1)
                model.move(source, destination)
                if animate:
                    time.sleep(delay_btw_moves)
                    print(str(model))
                stools3(n - 1, temp1, source, destination)
        
                
        i = optimal_i(n)
        if n == 1:
            model.move(source, destination)
            if animate:
                time.sleep(delay_btw_moves)
                print(str(model))
        else:
            hanoi(n-i, source, temp2, destination, temp1)
            stools3(i, source, temp2, destination)
            hanoi(n-i, temp1, source, temp2, destination)
        
                
    n = model.get_number_of_cheeses()
    hanoi(n, 0, 1, 2, 3)

    
def min_moves(n):
    """Return the minimun number of moves for the given n(number of cheeses).

    @param n: int
    @rtype int:
    """
    l = []
    if n == 1:
        return 1
    for i in range(1, n):
        m = 2 * min_moves(n-i) + 2**i - 1
        l.append(m)
        moves = min(l)       
    return moves
    
def optimal_i(n):
    """
    return the optimal i for the given n(number of cheeses).
    
    @param n: int
    @rtype int:
    """
    if n == 1:
        return 1
    for i in range(1, n):
        m = 2 * min_moves(n-i) + 2**i - 1
        moves = min_moves(n)
        if m == moves:
            return i
    
    

if __name__ == '__main__':
    num_cheeses = 17
    delay_between_moves = 0.5
    console_animate = False

    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=num_cheeses)

    tour_of_four_stools(four_stools,
                        animate=console_animate,
                        delay_btw_moves=delay_between_moves)
    
    print(four_stools.number_of_moves())
    # Leave files below to see what python_ta checks.
    # File tour_pyta.txt must be in same folder
    import python_ta
    python_ta.check_all(config="tour_pyta.txt")

"""
ConsoleController: User interface for manually solving
Anne Hoy's problems from the console.
"""

from toah_model import TOAHModel, IllegalMoveError


def move(model, origin, dest):
    """ Apply move from origin to destination in model.

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param int origin:
        stool number (index from 0) of cheese to move
    @param int dest:
        stool number you want to move cheese to
    @rtype: None
    """
    try:
        model.move(origin, dest)
    except IllegalMoveError:
        if origin == dest:
            print('Error, cheese cannot be moved to same stool,'
                  'Try Again\n')
        else:
            print('Error, cheese being moved is bigger than cheese at stool,'
                  'Try Again!\n')

class ConsoleController:
    """ Controller for text console.
    """

    def __init__(self, number_of_cheeses, number_of_stools):
        """ Initialize a new ConsoleController self.

        @param ConsoleController self:
        @param int number_of_cheeses:
        @param int number_of_stools:
        @rtype: None
        """
       
            
        self.number_of_stools = number_of_stools
        self.number_of_cheeses = number_of_cheeses
        
        self.toah = TOAHModel(number_of_stools)
        self.toah.fill_first_stool(number_of_cheeses)
        
        self.instructions = \
        ('The objective of the game is to move the given stack of cheeses \n'
         'to the right most stool with the least amount of moves.\n'
         'To move a block of cheese from stool X to stool Y \n'
         'enter stool numbers in the format x,y\n'
         "Enter 'Info' if you wish to read this message again\n"
         "Enter 'Quit' to exit the game")

    def play_loop(self):
        """ Play Console-based game.

        @param ConsoleController self:
        @rtype: None
        """
        print(self.instructions)      
        command = input("Enter a move or type Quit to exit: ")
        while command != 'Quit':
            c = command.strip().split(',')
            try:
                if command == 'Info':
                    print(self.instructions)
                elif len(c) != 2 or not(c[0].isnumeric() and c[1].isnumeric()):
                    raise IllegalMoveError 
                elif not 0 < int(c[0]) <= int(self.number_of_stools):
                    print('Error ' + c[0] + ' is not within the range\n')
                elif not 0 < int(c[1]) <= int(self.number_of_stools):
                    print('Error ' + c[1] + ' is not within the range\n')
                elif not self.toah.get_top_cheese(int(c[0]) - 1):
                    print('stool ' + str(int(c[0]) -1) + ' has No cheese!')
                else:
                    move(self.toah, int(c[0]) - 1, int(c[1]) - 1)
                    print(self.toah)
            except IllegalMoveError:
                print('Incorrect input, input must be positve #,#, Info or Quit\n')
            command = input("Enter a move or type Quit to exit: ")
        print("\nYou have successfully quit the game!")   
            
if __name__ == '__main__':
    num_cheeses = input("Enter number of cheese: ")
    while not num_cheeses.isnumeric():
        print('Input needs to be numeric and positive\n')
        num_cheeses = input("Enter number of cheese: ")
    num_stools = input("Enter number_of_stools: ")
    while not num_stools.isnumeric():
        print('Input needs to be numeric and positive\n')
        num_stools = input("Enter number_of_stools: ")
    play = ConsoleController(int(num_cheeses), int(num_stools))
    play.play_loop()
          
    # Leave lines below as they are, so you will know what python_ta checks.
    # You will need consolecontroller_pyta.txt in the same folder.
    import python_ta
    python_ta.check_all(config="consolecontroller_pyta.txt")

import sys
from itertools import cycle 
from itertools import repeat

def map_enum(func, enumerable, start=0):
    return map(func, enumerate(enumerable, start=start))

def ands(itrb):
    ander = lambda x, y: x and y
    return reduce(ander, itrb)

def ors(itrb):
    orer = lambda x, y: x or y
    return reduce(orer, itrb)


class Player(object):
    marker = ""

    def __init__(self, name, marker):
        self.name = name
        self.marker = marker

class Game(object):

    def __init__(self, name1, name2):
        """ initialize """
        self.player1 = Player(name1, 'x')
        self.player2 = Player(name2, 'o')

        self.board = self._new_board()

        self.player_cycle = cycle([self.player1, self.player2])
        self.current_player = self.player_cycle.next()

    def _print_board(self):
        printout = []
        for row in self.board:
            printout.append("|".join(row))
        print "\n-----\n".join(printout)
            
    def _new_board(self):
        row = repeat(" ", 9)
        return zip(*[row]*3)

    def flattened(self):
        # we get a mapping like (1, ' '), (2, 'x'), etc.
        return [space for row in self.board for space in row]
        
    def _valid_place(self, position):
        """ Make sure position isn't already filled 
        return True if place is empty"""
        check_empty = lambda (x, y): x==position and y==' '
        return ors(map_enum(check_empty, self.flattened(), start=1))

    def mark(self, place):       
        tick = self.current_player.marker
        marker = lambda (x, y): tick if x==place else y
        grouped_board = map_enum(marker, self.flattened(), start=1) 
        self.board = zip(*[iter(grouped_board)]*3)

    def _get_place(self):

        print "Make your move, %s!" % self.current_player.name
        place = raw_input("Enter a number [1-9] for the position you want to take:")
        return int(place)

    def check_valid(self, place):
        while not self._valid_place(place):
            print "Invalid move! Try again"
            place = self._get_place()
        self.mark(place)

    def play(self):
        """ check the while loop """
        # TODO: validate
        self._print_board()
        place = self._get_place()
        self.check_valid(place)
        if self.draw():
            self._print_board()
            print "It's a draw!"
            sys.exit(1)
        if self.winner():
            self._print_board()
            print "%s won!" % self.current_player.name
            sys.exit(1)
        else:
            self.current_player = self.player_cycle.next()
            self.play()

    def draw(self):
        return ands([' '!=x for x in self.flattened()])
    
    def _three_in_a(self, row):
        a, b, c = row
        return a == b == c and row[0] != ' '
    
    def check(self, threeple):
        return True in map(self._three_in_a, threeple)
        
    def _diags(self):
        get_diag = lambda (i, row): row[i]
        reversed_board = [row[::-1] for row in self.board]  
        first_diag = map_enum(get_diag, self.board)
        second_diag = map_enum(get_diag, reversed_board)
        return self.check([first_diag, second_diag]) 

    def _columns(self):
        return self.check(zip(*self.board))
        
    def _rows(self):
        return self.check(self.board) 

    def winner(self):
        # if first in each row is the same
        # if one row has all the same chars
        return ors([self._diags(), self._rows(), self._columns()])

if __name__=="__main__":
    game = Game('Will', 'Alicia')
    game.play()

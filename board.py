import numpy

#directions

DIRECTIONS = ('north', 'east', 'south', 'west')

#colors
COLORS = ('red', 'yellow', 'green', 'blue')

#shapes

SHAPES = ('circle', 'triangle', 'square', 'doji')

def create_board(board):
    return numpy.array(board).reshape((16,16))

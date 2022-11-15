from math import sqrt

import numpy

# convert ascii string to hex

def ascii_to_hex(ascii_string):
    '''
    Convert ascii string to hex string.

    input - an ascii string to be converted
    output - a hex string representing the ascii string
    '''
    return(ascii_string.encode('utf-8').hex())

# split hex into colours

def make_hex_colors(hex_string):
    '''
    Split hex string into individual hex colors.

    input - a hex string
    output - a list of hex colors

    note any extra hex_string that is a remainder will be removed from
    the end
    '''
    hex_string_length = len(hex_string) // 6
    hex_colors = []
    for i in range(hex_string_length):
        lower, upper = (6*i, 6*i+6)
        hex_colors.append(hex_string[lower:upper])

    hex_colors = numpy.array(hex_colors)

    return hex_colors, hex_string_length

# make suitable square
def square_size(hex_string_length):
    square_side = int(sqrt(hex_string_length))
    array_length = square_side ** 2

    return square_side, array_length

# fill in square with colours
def make_color_square(hex_colors, hex_string_length):
    square_side, array_length = square_size(hex_string_length)
    square_hex_colors = hex_colors[:array_length].reshape((square_side, square_side))

    return square_hex_colors

# output square as picture

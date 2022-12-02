from math import sqrt

import numpy
from PIL import Image, ImageColor

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
        hex_colors.extend(['#' + hex_string[lower:upper]])

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

    return square_hex_colors, square_side

def mm_to_pixel(size):
    conversion = 3.7795275591
    return int(conversion * size)

#Use the square_hex_colors
#Create another array containing coordinates in the same shape!
#Go through both together filling in the colors
def make_coordinate_array(square_size_mm, square_side):
    square_size_pixel = mm_to_pixel(square_size_mm)
    coord_array = numpy.zeros((square_side, square_side, 4), int)
    for x, _ in enumerate(coord_array):
        for y, _ in enumerate(coord_array):
            coord_array[y,x] = [x*square_size_pixel, y*square_size_pixel, (x+1)*square_size_pixel, (y+1)*square_size_pixel]

    return coord_array


# output square as picture
def make_image(coord_array, square_hex_colors, figname):
    width = coord_array[-1][-1][2]
    height = coord_array[-1][-1][3]
    data = numpy.zeros((height, width, 3), dtype = numpy.uint8)
    data[:,:] = [255,255,255] 
    for x, col in enumerate(coord_array):
        for y, val in enumerate(col):
            a, b, c, d = val
            color = square_hex_colors[x][y]
            data[a:c, b:d] = ImageColor.getrgb(color)

    img = Image.fromarray(data)
    img.save(figname)

    return data

def make_picture_from_string(ascii_string, square_size_mm = 10, figname = 'test.png'):
    hex_string = ascii_to_hex(ascii_string)
    hex_colors, hex_string_length = make_hex_colors(hex_string)
    square_hex_colors, square_side = make_color_square(hex_colors, hex_string_length)
    coord_array = make_coordinate_array(square_size_mm, square_side)
    data = make_image(coord_array, square_hex_colors, figname)

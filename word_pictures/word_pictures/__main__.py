from . import converter
from . import words

def main():
    ascii_string = 'The quick brown fox jumped over the lazy cat'*1000
    ascii_string = words.mit_10000_words
    ascii_string = 'age'*9
    square_size_mm = 10
    hex_string = converter.ascii_to_hex(ascii_string)
    hex_colors, hex_string_length = converter.make_hex_colors(hex_string)
    square_hex_colors, square_side = converter.make_color_square(hex_colors, hex_string_length)
    coord_array = converter.make_coordinate_array(square_size_mm, square_side)
    data = converter.test_image(coord_array, square_hex_colors)

    return hex_string, hex_colors, square_hex_colors, coord_array, data

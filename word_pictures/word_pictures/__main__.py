from . import converter

def main():
    ascii_string = 'The quick brown fox jumped over the lazy cat'
    hex_string = converter.ascii_to_hex(ascii_string)
    hex_colors, hex_string_length = converter.make_hex_colors(hex_string)
    square_hex_colors = converter.make_color_square(hex_colors, hex_string_length)

    return hex_string, hex_colors, square_hex_colors

from . import converter
from . import words

import random

def make_genomeseq(length):
    atgc_dict = {
            0 : 'A',
            1 : 'T',
            2 : 'G',
            3 : 'C'
            }

    genome_list = [atgc_dict[random.randint(0,3)] for i in range(length)]
    genomeseq = ''.join(genome_list)

    return genomeseq

def main():
    ascii_string = 'The quick brown fox jumped over the lazy cat'*1000
    ascii_string = words.mit_10000_words
    ascii_string = 'ATGCTAGCGATCGAGCTACGAGATCGACTACGATACGCGCGGACTATCGATCTATCATCGCGGCATCGACTACGACGATCGACTACG'
#    ascii_string = 'age'*9
    square_size_mm = 10
    ascii_string = 'GTAGGTAGGTAGGTAGGTAGGTAG'*10
    ascii_string = make_genomeseq(240)
    figname = 'fig3.png'

    converter.make_picture_from_string(ascii_string, square_size_mm, figname)
    return ascii_string

if __name__ == '__main__':
    _ = main()

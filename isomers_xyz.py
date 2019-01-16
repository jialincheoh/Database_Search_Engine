import subprocess
import sys

# from pdb2xyz import pdb2xyz
from Query_V2 import get_coord_from_frag_id_array
from reading_parameters import get_chem_formula
import rmsd
from structural_isomers import is_isomer
from isomers import is_isomer as is_stereo_isomer
from helpers import get_zmat_filename
from xyz2zmat_babel import xyz2zmat


def usage(cmd):
    print("""
Takes two .xyz files, converts them to zmat, and does an isomer check. Molecules are considered isomers if they have isomorphic structures.

Syntax: python isomers.py input1.xyz input2.xyz
""")


if __name__ == '__main__':
    args = sys.argv[1:]
    in_out = []
    if len(args) < 2:
        print('You need to specify at least two input file (.xyz)')
        usage(sys.argv[0])
        sys.exit(1)

    filename1 = args[0]
    filename2 = args[1]

    zmat_filename1 = get_zmat_filename(filename1)
    xyz2zmat(filename1, zmat_filename1)

    zmat_filename2 = get_zmat_filename(filename2)
    xyz2zmat(filename2, zmat_filename2)

    is_iso = is_isomer(zmat_filename1, zmat_filename2)

    if is_iso:
        print('is a stereo isomer')
    else:
        print('NOT an isomer')

import sys

import rmsd


def usage(cmd):
    print("""
Takes two .xyz files and calculates rmsd.

Syntax: python multi_rmsd.py input1.xyz input2.xyz
""")

def main(filename_xyz1, filename_xyz2):
    rmsd_before, rmsd_after = rmsd.calculate_rmsd(filename_xyz1, filename_xyz2)
    print('rmsd_before={}, rmsd_after={}'.format(
        rmsd_before, rmsd_after))


if __name__ == '__main__':
    args = sys.argv[1:]
    in_out = []
    if len(args) == 0:
        print('You need to specify two input files (.xyz)')
        usage(sys.argv[0])
        sys.exit(1)

    filename_xyz1 = args[0]
    filename_xyz2 = args[1]

    main(filename_xyz1, filename_xyz2)

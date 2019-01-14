import glob
import sys

from calculate_rmsd import main as calc_rmsd


# To time and record results, e.g.:
# time python multi_rmsd.py ~/Downloads/mc_2_files/opt.xyz ~/Downloads/mc_2_files/x > rmsd_calcs.txt


def usage(cmd):
    print("""
Takes one reference .xyz file and a file prefix and calculates rmsd between
the reference file and each file that matches the prefix.

Syntax: python multi_rmsd.py reference.xyz /path/to/files/x
""")


if __name__ == '__main__':
    args = sys.argv[1:]
    in_out = []
    if len(args) == 0:
        print('You need to specify two arguments,' 
            'a reference xyz and a file name prefix.')
        usage(sys.argv[0])
        sys.exit(1)

    reference_xyz = args[0]
    file_name_prefix = args[1]

    files_to_check = glob.glob('{}*'.format(file_name_prefix))
    i = 0
    for filename in files_to_check:
        calc_rmsd(reference_xyz, filename)
        i += 1
        # if i > 10:
        #     break

    print('Calculated rmsd for {} files'.format(i))
""" Very simple analysis of molecular structure. If the two inputs have the same
counts of the same atoms, they are considered isomers, regardless of how those atoms
are actually connected. """

import sys


def get_atoms(filename):
    # Dictionary to store atom counts
    input_atoms = {}
    with open(filename) as input_file:
        input_data = input_file.readlines()
        for line in input_data:
            line = line.strip()
            if not line:
                # If the line contains no data, ignore it
                continue
            # Split line (atom symbol should be first item)
            line_data = line.split()
            # Get the atom symbol, e.g. H or C
            atom = line_data[0]
            if atom not in input_atoms:
                # If this is an atom we haven't seen before, add it to the dictionary
                input_atoms[atom] = 0
            # Increment the count of times we've seen this atom
            input_atoms[atom] += 1
    return input_atoms


def is_isomer(filename1, filename2):
    # get atom counts for input1
    input_data1 = get_atoms(filename1)
    # Get atom counts for input2
    input_data2 = get_atoms(filename2)
    #print(input_data1)
    #print(input_data2)

    # See if atom dictionary for input1 matches atom dictionary for input 2
    # i.e. does it have the same atoms and the same count for each atom
    return input_data1 == input_data2


def usage(cmd):
    print("""
Takes two .zmat files and does a simple isomer check. Molecules are considered isomers if they contain the same atoms with the same counts.

Syntax: python structural_isomers.py input1.zmat input2.zmat
""")


if __name__ == '__main__':
    args = sys.argv[1:]
    in_out = []
    if len(args) == 0:
        print('You need to specify two input files (.zmat)')
        usage(sys.argv[0])
        sys.exit(1)

    input1 = args[0]
    input2 = args[1]

    is_iso = is_isomer(input1, input2)

    if is_iso:
        print('is a structural isomer')
    else:
        print('NOT an isomer')

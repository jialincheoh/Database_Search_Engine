import itertools
import rmsd
import numpy as np
import sys

from helpers import get_zmat_filename


class Atom:
    """ Represents an atom in a molecule
    symbol is the atom's symbol (e.g. C)
    bonds is a list of links to other Atoms
    """

    def __init__(self, id, symbol):
        self.id = id
        self.symbol = symbol
        self.bonds = []

    def __eq__(self, other):
        # This needs to be fleshed out more
        return self.symbol == other.symbol and len(self.bonds) == len(other.bonds)

    def __repr__(self):
        return '{} ({}), {} bonds'.format(self.symbol, self.id, len(self.bonds))


def add(current, parent_id, atom):
    """Recursive function to add an atom into the correct position in the tree"""

    # If the current atom matches the parent we are searching for, this atom
    # should be added to the bonds for current.
    if parent_id == current.id:
        current.bonds.append(atom)
        return True
    else:
        # Iterate over the bonds for current
        for bond in current.bonds:
            # Recursively call add on each bond
            if add(bond, parent_id, atom):
                # If add succeeds, break out of the loop and return
                return True
    return False


def print_tree(atom, prefix=''):
    """ Recursive function to print out an indented structure representing the tree """
    print('{}{}'.format(prefix, atom))
    for child in atom.bonds:
        print_tree(child, prefix='{}--'.format(prefix))


def is_isomorphic(n1, n2):
    """ Recursive function to check if trees are isomorphic """

    # Both roots are None, trees isomorphic by definition
    if n1 is None and n2 is None:
        return True

    # Exactly one of the n1 and n2 is None, trees are not
    # isomorphic, i.e. something is never isomorphic to nothing
    if n1 is None or n2 is None:
        return False

    # If the symbols of the current roots are not the same, not isomorphic
    if n1.symbol != n2.symbol:
        # print('{} does not match {}'.format(n1.symbol, n2.symbol))
        return False

    # If the two current roots both have zero bonds, isomorphic
    if len(n1.bonds) == 0 and len(n2.bonds) == 0:
        return True

    # If the two current roots have different numbers of bonds, not isomorphic
    if len(n1.bonds) != len(n2.bonds):
        # print('{} does not match {}'.format(len(n1.bonds), len(n2.bonds)))
        return False

    # If any arrangement of bonds in n2 matches the bonds in n1,
    # the tree is isomorphic.

    # Try every possible ordering of the bonds of n2 (second atom);
    # and compare each other with the order of bonds in n1 to see
    # if there is an ordering in which all subtrees are isomorphic.
    permutations = list(itertools.permutations(n2.bonds))
    # Check each permutation
    for permutation in permutations:
        is_match = True # Initialize match to True
        # For each bond, ensure subtrees are isomorphic
        for i in range(len(n1.bonds)):
            # Recursively call is_isomorphic to check subtrees

            # The bond to be checked on this iteration
            current_bond = n1.bonds[i]

            # permutation to be checked on this iteration
            current_permutation = permutation[i]

            # Because we take the previous result and combine it with the current
            # result, and because "and" is only true if all arguments are true,
            # the final result will be true if and only if all calls returned true.
            is_match = is_match and is_isomorphic(current_bond, current_permutation)

            # If at any point subtrees are not isomorphic, stop checking this permutation.
            if not is_match:
                break

        # Found a permutation that is isomorphic, so no need to check further permutations.        
        if is_match:
            return True

    return False


def get_raw_atoms(filename):
    atoms = []
    with open(filename) as input_file:
        for i, line in enumerate(input_file, 2):
            line_data = line.split()
            if len(line_data) != 4:
                continue
            atoms.append([
                float(line_data[1]),
                float(line_data[2]),
                float(line_data[3])
            ])
        
    return atoms


def get_atoms(filename):
    """ Read a zmat file and construct a tree representing
    the atomic bonds. Each node in the tree is an Atom.
    The Atom class contains the symbol and a list of bonds
    to other Atoms.
    """

    # The molecule variable is a reference to the root of the tree
    molecule = None

    # Open the zmat file
    with open(filename) as input_file:
        # Get the first line (This will be the root of the tree)
        first_line = next(input_file)

        # Create the Atom instance representing the first atom in the file
        molecule = Atom(1, first_line.split()[0])

        # Iterate over the remaining lines in the file
        for i, line in enumerate(input_file, 2):
            line_data = line.split()
            if not line_data:
                continue
            # The atom symbol is the first element on each line
            symbol = line_data[0]
            # The second element on each line is the line index of the parent atom
            # (in other words, the atom this one is bonded to).
            parent_id = int(line_data[1])
            atom = Atom(i, symbol)
            # Add the new atom into the tree
            add(molecule, parent_id, atom)

    # Return the root of the tree
    return molecule


def is_isomer(filename1, filename2):
    # Construct a tree for each input that represents the molecule.
    # Each node is an atom, and each atom has a list of its bonds to other atoms.
    input_data1 = get_atoms(filename1)
    # print('--------')
    # print_tree(input_data1)

    input_data2 = get_atoms(filename2)
    # print('--------')
    # print_tree(input_data2)

    # Check if the two trees are isomorphic
    is_iso = is_isomorphic(input_data1, input_data2)

    """
    if is_iso:
        filename_xyz1 = get_zmat_filename(filename1)
        xyz_data_1 = get_raw_atoms(filename_xyz1)
        filename_xyz2 = get_zmat_filename(filename1)
        xyz_data_2 = get_raw_atoms(filename_xyz2)
        
        P = np.array(xyz_data_1)
        Q = np.array(xyz_data_2)

        print("RMSD Before Translation: ", rmsd.kabsch_rmsd(P, Q))
        P -= rmsd.centroid(P)
        Q -= rmsd.centroid(Q)
        print("RMSD after translation: ", rmsd.kabsch_rmsd(P, Q))
    """

    return is_iso


def usage(cmd):
    print("""
Takes two .zmat files and does an isomer check. Molecules are considered isomers if they have isomorphic structures.

Syntax: python isomers.py input1.zmat input2.zmat
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
        print('is a stereo isomer')
    else:
        print('NOT an isomer')

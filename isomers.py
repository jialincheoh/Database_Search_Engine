import itertools
import rmsd
import numpy as np

# These are the input file names; must match exactly what you call the files
INPUT_FILE_1 = 'isomer1'
INPUT_FILE_2 = 'isomer2'


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
    if parent_id == current.id:
        current.bonds.append(atom)
        return True
    else:
        for bond in current.bonds:
            if add(bond, parent_id, atom):
                return True
    return False


def print_tree(atom, prefix=''):
    print('{}{}'.format(prefix, atom))
    for child in atom.bonds:
        print_tree(child, prefix='{}--'.format(prefix))


def is_isomorphic(n1, n2):
    # Both roots are None, trees isomorphic by definition
    if n1 is None and n2 is None:
        return True

    # Exactly one of the n1 and n2 is None, trees are not
    # isomorphic
    if n1 is None or n2 is None:
        return False

    if n1.symbol != n2.symbol:
        # print('{} does not match {}'.format(n1.symbol, n2.symbol))
        return False

    if len(n1.bonds) == 0 and len(n2.bonds) == 0:
        return True

    if len(n1.bonds) != len(n2.bonds):
        # print('{} does not match {}'.format(len(n1.bonds), len(n2.bonds)))
        return False

    # If any arrangement of bonds in n2 matches the bonds in n1,
    # the tree is isomorphic
    permutations = list(itertools.permutations(n2.bonds))
    for permutation in permutations:
        is_match = True
        for i in range(len(n1.bonds)):
            is_match = is_match and is_isomorphic(n1.bonds[i], permutation[i])
        if is_match:
            return True

    return False


def get_raw_atoms(filename):
    atoms = []
    with open(filename) as input_file:
        for i, line in enumerate(input_file, 2):
            line_data = line.split()
            atoms.append([
                float(line_data[1]),
                float(line_data[2]),
                float(line_data[3])
            ])
        
    return atoms

def get_atoms(filename):
    molecule = None
    with open(filename) as input_file:
        first_line = next(input_file)
        molecule = Atom(1, first_line.split()[0])
        for i, line in enumerate(input_file, 2):
            line_data = line.split()
            print(line_data)
            symbol = line_data[0]
            parent_id = int(line_data[1])
            atom = Atom(i, symbol)
            add(molecule, parent_id, atom)
    return molecule


def is_isomer(filename1, filename2):
    input_data1 = get_atoms(filename1)
    # print('--------')
    # print_tree(input_data1)

    input_data2 = get_atoms(filename2)
    # print('--------')
    # print_tree(input_data2)

    is_iso = is_isomorphic(input_data1, input_data2)

    if is_iso:
        xyz_data_1 = get_raw_atoms(INPUT_FILE_1 + ".xyz")
        xyz_data_2 = get_raw_atoms(INPUT_FILE_2 + ".xyz")
        
        P = np.array(xyz_data_1)
        Q = np.array(xyz_data_2)

        print('is a structural isomer')
        print("RMSD Before Translation: ", rmsd.kabsch_rmsd(P, Q))
        P -= rmsd.centroid(P)
        Q -= rmsd.centroid(Q)
        print("RMSD after translation: ", rmsd.kabsch_rmsd(P, Q))


if __name__ == "__main__":

    is_iso = is_isomer('isomer1', 'isomer2')

    if is_iso:
        print('is a structural isomer')
    else:
        print('NOT an isomer')


if is_isomorphic(input_data1, input_data2):
    xyz_data_1 = get_raw_atoms(INPUT_FILE_1 + ".xyz")
    xyz_data_2 = get_raw_atoms(INPUT_FILE_2 + ".xyz")
    
    P = np.array(xyz_data_1)
    Q = np.array(xyz_data_2)

    print('is a structural isomer')
    print("RMSD Before Translation: ", rmsd.kabsch_rmsd(P, Q))
    P -= rmsd.centroid(P)
    Q -= rmsd.centroid(Q)
    print("RMSD after translation: ", rmsd.kabsch_rmsd(P, Q))


    
else:
    print('NOT an isomer')

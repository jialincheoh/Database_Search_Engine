XYZ_EXTENSION = '.xyz'
ZMAT_EXTENSION = '.zmat'



def get_zmat_filename(xyz_filename):
    zmat_filename = xyz_filename.replace(XYZ_EXTENSION, ZMAT_EXTENSION)
    return zmat_filename


def get_xyz_filename(zmat_filename):
    xyz_filename = zmat_filename.replace(ZMAT_EXTENSION, XYZ_EXTENSION)
    return xyz_filename


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

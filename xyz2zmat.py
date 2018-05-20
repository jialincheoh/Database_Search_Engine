import sys
from angles import get_geom, get_bond_graph, write_zmat


def usage(cmd):
    print("""
Takes an input .xyz file and converts to an output .zmat file

Syntax: python execute_all_scripts.py input.xyz output.zmat
""")


def xyz2zmat(xyz_filename, zmat_filename):
    geom = get_geom(xyz_filename)
    bond_graph = get_bond_graph(geom)

    write_zmat(zmat_filename, geom, bond_graph)


"""
frag6
O
H  1    1.77642
H   1    1.77642  2 106.3863

water
O
H  1    0.96014
H   1    0.95993  2 109.4836

"""
def get_inputs():
    if (not len(sys.argv) == 3):
        print('Usage: xyz2zmat.py XYZ_FILE_NAME ZMAT_FILE_NAME\n')
        print('  XYZ_FILE_NAME: coordinates of target molecule\n')
        print('  ZMAT_FILE_NAME: z matrix of target molecule\n')
        sys.exit()
    else:
        xyz_file_name = sys.argv[1]
        zmat_file_name = sys.argv[2]
        return xyz_file_name, zmat_file_name


if __name__ == "__main__":
    # read in geometry, determine bonded topology
    xyz_file_name, zmat_file_name = get_inputs()

    geom = get_geom(xyz_file_name)
    bond_graph = get_bond_graph(geom)

    write_zmat(zmat_file_name, geom, bond_graph)

    # end of program

import glob
import itertools
import os
import sys

import rmsd
from structural_isomers import is_isomer
from isomers import is_isomer as is_stereo_isomer
from helpers import get_xyz_filename, get_zmat_filename, XYZ_EXTENSION, ZMAT_EXTENSION
from xyz2zmat_babel import xyz2zmat


def get_search_path(data_dir, extension):
    # Remove trailing slash if present
    if data_dir.endswith('/'):
        data_dir = data_dir[:-1]
    path_to_search = '{}/*{}'.format(data_dir, extension)
    return path_to_search


def convert_all_xyz_to_zmat(xyz_data_dir, zmat_data_dir):

    # Attempt to make zmat output dir
    try:
        os.mkdir(zmat_data_dir)
    except OSError as e:
        print('Failed to make zmat output directory', e)
        sys.exit(11)

    # Convert all xyz files to zmat files
    #print('Converting xyz files in {}'.format(xyz_data_dir))
    path_to_search = get_search_path(xyz_data_dir, XYZ_EXTENSION)
    xyz_files = glob.glob(path_to_search)
    for xyz_file_path in xyz_files:
        filename_parts = os.path.split(xyz_file_path)
        xyz_filename = filename_parts[-1]

        filename_base, ext = os.path.splitext(xyz_filename)
        #print('Converting', filename_base, ext)

        if ext != XYZ_EXTENSION:
            # Don't try to process files that are not .xyz
            print('Wrong extension in {}'.format(xyz_filename))
            continue
    
        zmat_filename = get_zmat_filename(xyz_filename)
        zmat_file_path = os.path.join(zmat_data_dir, zmat_filename)
        xyz2zmat(xyz_file_path, zmat_file_path)
        
    #print('Done converting xyz files')


def usage(cmd):
    # Takes a directory containing .xyz files, converts all to zmat,
    # and checks every pair of files for isomers.
    print("""
Takes a directory containing .xyz files, converts all to zmat, and checks every pair of files for isomers.

Syntax: python xyz_all_comparison_automation_script.py ./xyz_input_data ./zmat_output_data
""")


if __name__ == '__main__':
    args = sys.argv[1:]
    in_out = []
    if len(args) != 2:
        print('You need to specify an input xyz data directory and an output zmat directory')
        usage(sys.argv[0])
        sys.exit(1)

    """
    1. Take input data dir containing .xyz files
    2. Create output zmat dir
    3. For every pair of files in output zmat dir, check isomer and calculate rmsd
    """

    xyz_data_dir = args[0]
    zmat_data_dir = args[1]

    #convert_all_xyz_to_zmat(xyz_data_dir, zmat_data_dir)

    # For each pair of zmat files, check isomers and calculate rmsd

    path_to_search = get_search_path(zmat_data_dir, ZMAT_EXTENSION)
    zmat_files = glob.glob(path_to_search)

    #pairs = [(zmat_files[0], zmat_files[1])]
    #print(pairs)
    pairs = list(itertools.combinations(zmat_files, 2))

    for zmat_filename, other_zmat_filename in pairs:

        is_struct_iso = is_isomer(zmat_filename, other_zmat_filename)

        is_stereo_iso = is_stereo_isomer(zmat_filename, other_zmat_filename)

        rmsd_before = 'N/A'
        rmsd_after = 'N/A'
        if is_struct_iso or is_stereo_iso:
            xyz_filename = get_xyz_filename(zmat_filename)
            other_xyz_filename = get_xyz_filename(other_zmat_filename)
            rmsd_before, rmsd_after = rmsd.calculate_rmsd(other_xyz_filename, xyz_filename)

        print('{}, {}, structural isomer: {}, stereo isomer: {}, rmsd_before={}, rmsd_after={}'.format(
            zmat_filename, other_zmat_filename, is_struct_iso, is_stereo_iso, rmsd_before, rmsd_after))

    sys.exit(0)

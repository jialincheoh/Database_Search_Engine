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


GROUP = 'Slipchenko'
PASSWORD = 'Terri'


def usage(cmd):
    # Takes an input.pdb file, converts to input.xyz and looks for isomers
    print("""
Takes an input.xyz file and looks for isomers

Syntax: python execute_all_scripts.py input.xyz
""")


if __name__ == '__main__':
    args = sys.argv[1:]
    in_out = []
    if len(args) == 0:
        print('You need to specify at least one input file (.xyz)')
        usage(sys.argv[0])
        sys.exit(1)

    xyz_filename = args[0]
    if not xyz_filename.endswith('.xyz'):
        print('Wrong extension in %s' % xyz_filename)
        sys.exit(2)
    
    filename_base = xyz_filename[:-4]

    # Step 1: convert pdb to xyz
    #xyz_filename = '{}.xyz'.format(filename_base)
    #print('Writing %s' % xyz_filename)
    #pdb2xyz(pdb_filename, xyz_filename)

    zmat_filename = get_zmat_filename(xyz_filename)
    xyz2zmat(xyz_filename, zmat_filename)

    # Step 2: Use xyz coordinates to query for efp mysqldb
    formula = get_chem_formula(xyz_filename)
    #formula = "C1366N373S6O389"
    # C3724H5700N1026O1102
    #formula = 'H2O1'
    print('formula', formula)

    # Step 3: Get fragment coordinates for formula
    coords = get_coord_from_frag_id_array(GROUP, PASSWORD, formula)
    #coords = {6: 'frag_id: 6\nO 0.0 0.1191094785 0.0\nH -1.422305967 -0.9451766865 0.0\nH 1.422305967 -0.9451766865 0.0\n', 7: 'frag_id: 7\nO 0.0 0.1191094785 0.0\nH -1.422305967 -0.9451766865 0.0\nH 1.422305967 -0.9451766865 0.0\n'}
    
    # Step 4: Check if each fragment is an isomer
    for frag_id in coords:
        frag_filename = '{}_frag{}.xyz'.format(filename_base, frag_id)
        with open(frag_filename, 'w') as frag_file:
            frag_file.write(coords[frag_id])
        frag_zmat_filename = get_zmat_filename(frag_filename)
        xyz2zmat(frag_filename, frag_zmat_filename)

        is_struct_iso = is_isomer(zmat_filename, frag_zmat_filename)
        print('{} and {} are structural isomers: {}'.format(
            zmat_filename, frag_zmat_filename, is_struct_iso))

        is_stereo_iso = is_stereo_isomer(zmat_filename, frag_zmat_filename)
        print('{} and {} are stereo isomers: {}'.format(
            zmat_filename, frag_zmat_filename, is_stereo_iso))

        if is_struct_iso or is_stereo_iso:
            rmsd_before, rmsd_after = rmsd.calculate_rmsd(frag_filename, xyz_filename)
            print('rmsd_before={}, rmsd_after={}'.format(rmsd_before, rmsd_after))

    sys.exit(0)


"""


4) you need to split the result of step 3 so you can run it through your isomer search script; 
so you need to compare the xyz coords from step 1 (which is the original xyz frag) to all of
 the results from step 3. 

5) You need to make sure that you return the xyz & rmsd value for each fragment found in step 3 
in a text file that hanjings script can use to visualize; 

6) hanjings script will do its thing, and then it will pass back frag_id, so then you need to
 make sure that return_frag_full_parameter(frag_id); 
"""

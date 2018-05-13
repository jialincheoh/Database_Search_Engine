import sys

from pdb2xyz import pdb2xyz
from Query_V2 import query_chemical_formula
from reading_parameters import get_chem_formula, get_coord


def usage(cmd):
    print("""
Converts a input.pdb file to input.xyz

Syntax: python execute_all_scripts.py
""")



if __name__ == '__main__':
    args = sys.argv[1:]
    in_out = []
    if len(args) == 0:
        print('You need to specify at least one input file (.pdb)')
        usage(sys.argv[0])
        sys.exit(1)

    fin = args[0]
    if not fin.endswith('.pdb'):
        print('Wrong extension in %s' % fin)
        sys.exit(2)
    
    # Step 1: convert pdb to xyz
    fout = '%s.xyz' % fin[:-4]
    #print('Writing %s' % fout)
    #pdb2xyz(fin, fout)

    # Step 2: Use xyz coordinates to query for efp mysqldb
    #formula = get_chem_formula(fout)
    formula = "C1366N373S6O389"
    formula = 'H2O1'
    frag_list = query_chemical_formula('Slipchenko', 'Terri', formula)
    print('frag_list', frag_list)

    sys.exit(0)


"""
What do we pass to query_chemical_formula for "chemical_form"? Is this related in some way to the xyz output
of step 1?

2) we need to take the xyz coords to use a 'string' query for efp mysqldb; 
(specifically, we are going to query chemical formula); 
so we need to run it through query_chemical_formula('Slipchenko','Terri','H2O1')
#test cases for when slipchenko/password is wrong or when chemical is not found; query_chemical_formula() will return an array of index values for matching parameters to the query(); 
- 

3) you need to feed the results of step 2 into get_coord_from_frag_id_array(group,password,chemical_form); This will return this:

frag_id: 6
O 0.0 0.1191094785 0.0
H -1.422305967 -0.9451766865 0.0
H 1.422305967 -0.9451766865 0.0
frag_id: 7
O 0.0 0.1191094785 0.0
H -1.422305967 -0.9451766865 0.0
H 1.422305967 -0.9451766865 0.0

4) you need to split the result of step 3 so you can run it through your isomer search script; so you need to compare the xyz coords of from step 1 (which is the original xyz frag) to all of the results from step 3. 

5) You need to make sure that you return the xyz & rmsd value for each fragment found in step 3 in a text file that hanjings script can use to visualize; 

6) hanjings script will do its thing, and then it will pass back frag_id, so then you need to make sure that return_frag_full_parameter(frag_id); 
"""
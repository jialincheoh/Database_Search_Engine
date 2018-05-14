from __future__ import print_function

import datetime
import sys
import mysql
import mysql.connector
from mysql.connector import errorcode
import ast


# coding: utf-8

# In[249]:


def check_group(group, password): 
    #SELECT count(`group`) FROM parameters WHERE `group`='Slipchenko'
    cursor.execute("SELECT COUNT(`group`) FROM `groups` WHERE (`group`='%s' and password='%s');" %(group,password))
    tally=cursor.fetchall()
    
    if tally[0][0] > 0:
        return 'AFFILIATED'
    else:
        return 'UNAFFILIATED'

   
def query_chemical_formula(group,password,chemical_form):
    
    status=check_group(group, password)
    
    if status=='AFFILIATED':
        
        #search for coordinates in database with chemical_formula
        cursor.execute("SELECT coordinates, COUNT(*) FROM parameters WHERE chemical_formula LIKE '%s';" %(chemical_form))
        frag_count=cursor.fetchall()[0][1]
        print(frag_count)
        
        if frag_count==0:
            print("No parameters found")
        
        if frag_count >=0:
            cursor.execute("SELECT id FROM parameters WHERE chemical_formula='%s';" %(chemical_form))
            fragments=cursor.fetchall()   
            
            frag_list=[]
            for i in fragments:
                frag_list.append(i[0])
            
        return(frag_list)
    else:
        cursor.execute("SELECT coordinates, COUNT(*) FROM parameters WHERE chemical_formula LIKE '%s';" %(chemical_form))
        frag_count=cursor.fetchall()[0][1]
        print(frag_count)
        
        if frag_count==0:
            print("No parameters found")
        
        if frag_count >=0:
            cursor.execute("SELECT id FROM parameters WHERE (chemical_formula='%s' AND status=1);" %(chemical_form))
            fragments=cursor.fetchall()   
            
            frag_list=[]
            for i in fragments:
                frag_list.append(i[0])
            
        return(frag_list)
    

def get_coord_by_frag_id(id): 
    
    cursor.execute("SELECT coordinates FROM parameters WHERE id=%s;" %(id))
#    print(cursor.fetchall()[0][0])
    coordstr = cursor.fetchall()[0][0]
    testarray = ast.literal_eval(coordstr)
    
    xyz=[]
    for i in testarray:
        if i.split()[0].startswith('A'):
            
            atoms=i.split()[0]
            coord=i.split()[1:4]
            new_coord=[coord for coord in list(map(float,coord))]
            new_coord.insert(0,atoms)
            
            xyz.append(new_coord)
            
    new_array=[]
    for i in xyz:
        new_array.append(i)
    
    for line in new_array:
        if "O" in line[0]:
            new_array[new_array.index(line)][0] = "O"
        if "C" in line[0]:
            new_array[new_array.index(line)][0] = "C"
        if "H" in line[0]:
            new_array[new_array.index(line)][0] = "H"
        if "N" in line[0]:
            new_array[new_array.index(line)][0] = "N"
        if "S" in line[0]:
            new_array[new_array.index(line)][0] = "S"

    return new_array
        
def get_coord_from_frag_id_array(group,password,chemical_form):
    
    frag_list=query_chemical_formula(group,password,chemical_form)

    frag_strings = {}
    for frag_id in frag_list:
        frag_string = "frag_id: {}\n".format(frag_id)
        xyz=get_coord_by_frag_id(frag_id)
        for atom in xyz:
            frag_string = '{}{}\n'.format(frag_string, ' '.join(map(str,atom)))
        frag_strings[frag_id] = frag_string
    return frag_strings
    
#def get_full_efp_parameter(frag_id): 

def print_rows(parameter):
        for i in parameter:
            print("%s" %(i))
            
def return_frag_full_parameter(frag_id):
    cursor.execute("SELECT * FROM parameters where id=%s;" %(frag_id))
    #coordstr = cursor.fetchall()[0][0]
    coordstr = cursor.fetchone()
    #testarray = ast.literal_eval(coordstr)
    
    frag_id=coordstr[0]
    datetime=coordstr[1]
    chemical_formula=coordstr[2]
    group=coordstr[3]
    status=coordstr[4]
    basis_set=coordstr[5]
    coordinates=ast.literal_eval(coordstr[6])
    monopoles=ast.literal_eval(coordstr[7])
    dipoles=ast.literal_eval(coordstr[8])
    quadrupoles=ast.literal_eval(coordstr[9])
    octupoles=ast.literal_eval(coordstr[10])
    polarizable_pts=ast.literal_eval(coordstr[11])
    dynamic_polarizable_pts=ast.literal_eval(coordstr[12])
    projection_basis_set=ast.literal_eval(coordstr[13])
    multiplicity=ast.literal_eval(coordstr[14])
    projection_wavefunction=ast.literal_eval(coordstr[15])
    fock_matrix=ast.literal_eval(coordstr[16])
    lmo_centroids=ast.literal_eval(coordstr[17])
    canonvec=ast.literal_eval(coordstr[18])
    canonfok=ast.literal_eval(coordstr[19])
    screen3=ast.literal_eval(coordstr[20])
    screen2=ast.literal_eval(coordstr[21])
    screen=ast.literal_eval(coordstr[22])
    
    print(" $BASISSET %s" %(basis_set))
    print(" $%s" %(chemical_formula))
    print(" COORDINATES (BOHR)")
    print(print_rows(coordinates))
    print(" STOP")
    print(" MONOPOLES")
    print(print_rows(monopoles))
    print(" STOP")
    print(" DIPOLES")
    print(print_rows(dipoles))
    print(" STOP")
    print(" QUADRUPOLES")
    print(print_rows(quadrupoles))
    print(" STOP")
    print(" POLARIZABLE POINTS")
    print(print_rows(polarizable_pts))
    print(" STOP")
    print(" DYNAMIC POLARIZABLE POINTS")
    print(print_rows(dynamic_polarizable_pts))
    print(" STOP")
    print(" PROJECTION BASIS SET")
    print(print_rows(projection_basis_set))
    print(" STOP")
    print(" MULTIPLICITY")
    print(print_rows(multiplicity))
    print(" STOP")
    print(" PROJECTION WAVEFUNCTION")
    print(print_rows(projection_wavefunction))
    print(" STOP")
    print(" FOCK MATRIX")
    print(print_rows(fock_matrix))
    print(" STOP")
    print(" LMO CENTROIDS")
    print(print_rows(lmo_centroids))
    print(" STOP")
    print(" CANONVEC")
    print(print_rows(canonvec))
    print(" STOP")
    print(" CANONFOK")
    print(print_rows(canonfok))
    print(" STOP")
    print(" SCREEN3")
    print(print_rows(screen3))
    print(" STOP")
    print(" SCREEN2")
    print(print_rows(screen2))
    print(" STOP")
    print(" SCREEN")
    print(print_rows(screen))
    print(" STOP")
    #for i in testarray:
    #    print(i)


# In[208]:


#connecting to MySQL

#db = connection object
cnx = mysql.connector.connect(host="ssi-db.cllylwkcavdc.us-east-2.rds.amazonaws.com",
                         user="lslipche",
                         passwd="29221627", database='TEMP')
cursor = cnx.cursor()

"""
check_group('Slipchenko','Terri')
query_chemical_formula('Slipchenko','Terri2','H2O1')
get_coord_from_frag_id_array('Slipchenko','Terri','H2O1')


# In[246]:


get_coord_from_frag_id_array('Slipchenko','Terri','H2O1')


# In[250]:


return_frag_full_parameter(6)
"""


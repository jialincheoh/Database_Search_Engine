
# coding: utf-8

# In[3]:


import datetime
import sys
import mysql
import mysql.connector

db = mysql.connector.connect(host="ssi-db.cllylwkcavdc.us-east-2.rds.amazonaws.com",
                         user="lslipche",
                         passwd="29221627",
                         db="SSI_test")
cur = db.cursor()


# In[4]:


#check_data(cur)

#define all python functions to read in parameter file and extract information 
def read_coord(file):
    print(file)
    """
    lines=[]
    with open(file) as parameter:
        for line in parameter:
            if line.strip() == 'COORDINATES (BOHR)':
                break
        for line in parameter:
            if line.strip() == 'STOP':
                break
            lines.append(line)
    """
    with open(file) as parameter:
        xyz=[]
        for i in parameter:
            parts = i.split()
            if len(parts) == 4:
                
                atoms = parts[0]
                coord = parts[1:4]
                new_coord = [coord for coord in list(map(float,coord))]
                new_coord.insert(0,atoms)
                
                xyz.append(new_coord)
            
    return xyz 

#gets coordinates in the xyz array
def get_coord(file): 
    
    xyz=read_coord(file)
    
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
    #for line in new_array:
    #    print ' '.join(map(str,line))

                
#counts and tallies up atoms from coordinate file
def get_chem_formula(file):
    
    array=get_coord(file)
    
    C=H=N=S=O=0   
    
    for i in array:
        if 'O' in i[0]:
            O+=1
        if 'C' in i[0]:
            C+=1
        if 'N' in i[0]:
            N+=1
        if 'H' in i[0]:
            H+=1
        if 'S' in i[0]:
            S+=1
            
    formula={"C":int(C),"H":int(H), "N":int(N), "S":int(S), "O":int(O)}  
    chemicals=""
     
    for j in formula:
        if formula[j] != 0:
            chemicals += j+ str(formula[j])
    
    return chemicals

#extracts the full textfile
def get_parameters(file):
    lines=[]
    with open(file) as parameter:
        for line in parameter:
            lines.append(line)
    return lines

"""
parameter=('h2o.efp')
#parameter=str(sys.argv[1])

#extract coords, chemical formula, and EFP parameter into string variables (coord_str, form, parm_str). 
coord=get_coord(parameter)
#print(coord)
coord_str="\n".join(str(i) for i in coord)

form=get_chem_formula(parameter)
#print(form)

parm=get_parameters(parameter)
parm_str='\n'.join(parm)
#print(parm_str)

#insert parameters into tables 
#columns: fragment, chemicalformula, coordinates, parameters
#all data must be read in as a string.
#print(type(parameter), type(form), type(coord_str), type(parm_str))
current_timestamp = datetime.datetime.now()

#tables = cur.execute("INSERT INTO SSI_sub(date,fragment,chemicalformula,coordinates,parameters) VALUES (%s,%s,%s,%s,%s);", (current_timestamp, parameter, form, coord_str, parm_str))
#print("execute result", tables)
#print(dir(cur))
#print(cur._warnings)

#db.commit()
"""


# In[20]:


def ensure_str(s):
    if isinstance(s, str):
        s = s.encode('utf-8')
    return s

def query(string):
    
    db = mysql.connector.connect(host="ssi-db.cllylwkcavdc.us-east-2.rds.amazonaws.com",
                         user="lslipche",
                         passwd="29221627",
                         db="SSI_test")
    cur = db.cursor()
    #string=str(sys.argv[1])
    string="SELECT chemicalformula,coordinates FROM SSI_sub"
    
    cur.execute(string)
    
    entry=[]
    for i in cur.fetchall():
        entry.append(ensure_str(i[0]))
        
    return entry
        
        #print entry.append(ensure_str(i[3]))
        
    #return entry   
    #print entry[3].strip("\n").replace('\"','').split('\n')[0]
    

"""
# In[100]:


cur.execute('TRUNCATE TABLE SSI_sub')


# In[10]:


get_coord(parameter)


# In[21]:


query('test')
"""


# In[24]:


def strip_text(text):
    #strips the string of brackets and quotation marks for better readability 
    unwanted={"'":"", "[":"", "]":"", ",":"", "b":" "}
    
    for i, j in unwanted.items():
        text=text.replace(i,j)
    return text 

def query_return_coord(parameter):
    coord=[]
    coord=query('parameter')
    return query('parameter')
    for i in coord:
        return strip_text(str(i))
        #return strip_text(str(i))
        #return " ".join(i).replace("'", " ").replace("]", "").replace("[","").replace(",","")


"""
# In[25]:


query_return_coord('parameter')


# In[7]:


get_multipoles(parameter)
"""


# In[8]:


def get_multipoles(file):
    
    monopoles=dipoles=quadrupoles=octupoles=[]
    
    multipoles={'MONOPOLES':monopoles, 'DIPOLES':dipoles, 'QUADRUPOLES':quadrupoles, 'OCTUPOLES':octupoles}
    
    copy=False
    
    with open(file) as parameter:
        for multipole_coord, multipole_type in multipoles.items():
            for line in parameter:
                    if line.strip() in multipoles:
                        copy = True
                    elif line.strip() == 'STOP':
                        copy = False
                    elif copy:
                        multipole_type.append(line)
    print('MONOPOLES')
    return multipoles.get('MONOPOLES')


"""
# In[9]:


get_multipoles(parameter)
"""


# In[69]:


def get_polarizable_pts(file):
    
    polarizable_pts=[]
    with open(file) as parameter:
        for line in parameter:
            if line.strip() == 'POLARIZABLE POINTS':
                break
        for line in parameter:
            if line.strip() == 'STOP':
                break
            polarizable_pts.append(line)

    return polarizable_pts


# In[70]:


def get_dynamic_polarizable_pts(file):
    
    dynamic_polarizable_pts=[]
    with open(file) as parameter:
        for line in parameter:
            if line.strip() == 'DYNAMIC POLARIZABLE POINTS':
                break
        for line in parameter:
            if line.strip() == 'STOP':
                break
            dynamic_polarizable_pts.append(line)

    return dynamic_polarizable_pts


# In[71]:


def get_projection_basis_set(file):
    
    projection_basis_set=[]
    with open(file) as parameter:
        for line in parameter:
            if line.strip() == 'DYNAMIC POLARIZABLE POINTS':
                break
        for line in parameter:
            if line.strip() == 'STOP':
                break
            projection_basis_set.append(line)

    return projection_basis_set


# In[72]:


def get_multiplicity(file):
    import re 
    
    multiplicity=[]
    with open(file) as parameter:
        for line in parameter:
            if 'MULTIPLICITY' in line.strip(): 
                multiplicity.append(float(re.split('\s+',line)[2]))

    return multiplicity


"""
# In[73]:


get_multiplicity(parameter)

"""

# In[76]:


def get_projection_wavefunction(file):
    import re 
    
    copy=False
    projection_wavefunction=[]
    with open(file) as parameter:
        for line in parameter:
            if 'PROJECTION WAVEFUNCTION' in line.strip(): 
                copy=True
                projection_wavefunction.append(float(re.split('\s+',line)[3]))
                projection_wavefunction.append(float(re.split('\s+',line)[4]))
            elif line.strip() == 'FOCK MATRIX ELEMENTS':
                copy = False
            elif copy:
                projection_wavefunction.append(line)

    return projection_wavefunction


"""
# In[77]:


get_projection_wavefunction(parameter)
"""


# In[78]:


def get_fock_matrix(file):
    import re 
    
    copy=False
    fock_matrix=[]
    with open(file) as parameter:
        for line in parameter:
            if 'FOCK MATRIX ELEMENTS' in line.strip(): 
                copy=True
            elif line.strip() == 'LMO CENTROIDS':
                copy = False
            elif copy:
                fock_matrix.append(line)

    return fock_matrix

"""
# In[79]:


get_fock_matrix(parameter)
"""


# In[80]:


def get_lmo_centroids(file):
    copy=False
    lmo_centroids=[]
    with open(file) as parameter:
        for line in parameter:
            if 'LMO CENTROIDS' in line.strip(): 
                copy=True
            elif line.strip() == 'STOP':
                copy = False
            elif copy:
                lmo_centroids.append(line)

    return lmo_centroids


# In[81]:


def get_canonvec(file):
    import re 
    
    copy=False
    canonvec=[]
    
    with open(file) as parameter:
        for line in parameter:
            if 'CANONVEC' in line.strip(): 
                copy=True
                canonvec.append(float(re.split('\s+',line)[2]))
                canonvec.append(float(re.split('\s+',line)[3]))
            elif line.strip() == 'CANONFOK':
                copy = False
            elif copy:
                canonvec.append(line)
    return canonvec


"""
# In[82]:


get_canonvec(parameter)
"""


# In[83]:


def get_canonfok(file):
    copy=False
    canonfok=[]
    with open(file) as parameter:
        for line in parameter:
            if 'CANONFOK' in line.strip(): 
                copy=True
            elif line.strip() == 'STOP':
                copy = False
            elif copy:
                canonfok.append(line)

    return canonfok


# In[84]:


def get_screen3(file):
    import re 
    
    copy=False
    screen3=[]
    
    with open(file) as parameter:
        for line in parameter:
            if 'SCREEN3' in line.strip(): 
                copy=True
                screen3.append(float(re.split('\s+',line)[2]))
                screen3.append(float(re.split('\s+',line)[3]))
            elif line.strip() == 'SCREEN3':
                copy = False
            elif copy:
                screen3.append(line)
    return screen3


"""
# In[85]:


get_screen3(parameter)
"""


# In[86]:


def get_screen2(file):
    import re 
    
    copy=False
    screen2=[]
    
    with open(file) as parameter:
        for line in parameter:
            if 'SCREEN2' in line.strip(): 
                copy=True
                screen2.append(re.split('\s+',line)[3])
            elif line.strip() == 'STOP':
                copy = False
            elif copy:
                screen2.append(line)
    return screen2


"""
# In[87]:


get_screen2(parameter)
"""


# In[40]:


def get_screen(file):
    import re 
    
    copy=False
    screen=[]
    
    with open(file) as parameter:
        for line in parameter:
            if 'SCREEN       (' in line.strip(): 
                copy=True
                screen.append(re.split('\s+',line)[3])
            elif line.strip() == 'STOP':
                copy = False
            elif copy:
                screen.append(line)
    return screen

"""
# In[41]:


type(get_screen(parameter))
"""


# In[35]:


def query_2(get_coordinates):
    db = mysql.connector.connect(host="ssi-db.cllylwkcavdc.us-east-2.rds.amazonaws.com",
                         user="lslipche",
                         passwd="29221627",
                         db="SSI_test")
    cur = db.cursor()
    #string=str(sys.argv[1])
    string="SELECT chemicalformula FROM SSI_sub"
    
    cur.execute(string)
    
    entry=[]
    for (chemicalformula) in cur:
        print("{}".format(chemicalformula))
        
    cur.close()
    db.close()

    

"""
# In[36]:


query_2('test')
"""


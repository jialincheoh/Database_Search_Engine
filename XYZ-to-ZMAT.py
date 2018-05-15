#!/opt/local/bin/python2.7

import os
#import numpy
import math
from decimal import *
from numpy import *
from sys import *
import sys
import getopt

### --- Arguments --- ###
ifile = ''
ofile = ''
printfile = 0


def print_help():
	print("Usage: %s -i <inputfile.xyz> -o <outputfile.zmat>" % sys.argv[0])
		

### Read command line args
try:
	myopts, args = getopt.getopt(sys.argv[1:],"i:o:ph")
except getopt.GetoptError:
	print_help()
	sys.exit(2)
	
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
	if o == '-i':
		ifile = a
	elif o == '-o':
		ofile = a
	elif o == '-p':
		printfile=1
	elif o == '-h':
		print_help()
		sys.exit(0)
	else:
		print_help()
		sys.exit(0)

if not ifile:
	print_help()
	sys.exit(3)

if not ofile:
	print_help()
	sys.exit(4)


### --- Distance function --- ###
def getdistance(at1, at2, lol):
	try:
		atom1 = array([float(lol[at1][1]), float(lol[at1][2]), float(lol[at1][3])])
		atom2 = array([float(lol[at2][1]), float(lol[at2][2]), float(lol[at2][3])])
		vector1 = atom2-atom1
		dist = linalg.norm(vector1)
		#print dist
		return dist
	except:
		return 0

### --- Angle function --- ###
def getangle(at1, at2, at3, lol):
	try:
		atom1 = array([float(lol[at1][1]), float(lol[at1][2]), float(lol[at1][3])])
		atom2 = array([float(lol[at2][1]), float(lol[at2][2]), float(lol[at2][3])])
		atom3 = array([float(lol[at3][1]), float(lol[at3][2]), float(lol[at3][3])])
		# making appropriate vectors and normals 
		vector1 = atom1-atom2
		vector2 = atom3-atom2
		angle = arccos(dot(vector1,vector2)/(linalg.norm(vector1)*linalg.norm(vector2)))
		#print degrees(angle)
		return degrees(angle)
	except:
		return 0.000000

### --- Dihedral angle function --- ###
def getdihedral(at1, at2, at3, at4, lol):
	try:
		# put positions in array
		atom1 = array([float(lol[at1][1]), float(lol[at1][2]), float(lol[at1][3])])
		atom2 = array([float(lol[at2][1]), float(lol[at2][2]), float(lol[at2][3])])
		atom3 = array([float(lol[at3][1]), float(lol[at3][2]), float(lol[at3][3])])
		atom4 = array([float(lol[at4][1]), float(lol[at4][2]), float(lol[at4][3])])
		# making appropriate vectors and normals 
		vector1 = atom2-atom1
		vector2 = atom3-atom2
		plane1 = cross(vector1,vector2)
		vector3 = atom2-atom3
		vector4 = atom4-atom3
		plane2 = cross(vector3,vector4)
		# finding dihedral angle
		dihedral = arccos(-dot(plane1,plane2)/(linalg.norm(plane1)*linalg.norm(plane2)))
		# checking the sign of the dihedral then displaying result
		if dot(plane1,vector4) > 0:
			#print degrees(dihedral)
			return  degrees(dihedral)
		else:
			#print -degrees(dihedral)
			return - degrees(dihedral)
	except:
		return 0	


### --- Functions to get and give element numbers and names --- ###
elementList = ["h","he","li","be","b","c","n","o","f","ne","na","mg","al","si","p","s","cl","ar","k","ca","sc","ti","v","cr","mn","fe","co","ni","cu","zn","ga","ge","as","se","br","kr","rb","sr","y","zr","nb","mo","tc","ru","rh","pd","ag","cd","in","sn","sb","te","i","xe","cs","ba","la","ce","pr","nd","pm","sm","eu","gd","tb","dy","ho","er","tm","yb","lu","hf","ta","w","re","os","ir","pt","au","hg","tl","pb","bi","po","at","rn","fr","ra","ac","th","pa","u","np","pu","am","cm","bk","cf","es","fm","md","no","lr","rf","db","sg","bh","hs","mt","ds","rg","cn","uut","fl","uup","lv","uus","uuo"]
elementNames = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Uut","Fl","Uup","Lv","Uus","Uuo"]
elementLarge =  ["na","mg","al","si","p","s","cl","ar","k","ca","sc","ti","v","cr","mn","fe","co","ni","cu","zn","ga","ge","as","se","br","kr","rb","sr","y","zr","nb","mo","tc","ru","rh","pd","ag","cd","in","sn","sb","te","i","xe","cs","ba","la","ce","pr","nd","pm","sm","eu","gd","tb","dy","ho","er","tm","yb","lu","hf","ta","w","re","os","ir","pt","au","hg","tl","pb","bi","po","at","rn","fr","ra","ac","th","pa","u","np","pu","am","cm","bk","cf","es","fm","md","no","lr","rf","db","sg","bh","hs","mt","ds","rg","cn","uut","fl","uup","lv","uus","uuo"]

def getElementNum(at1):
	element = elementList.index(at1.lower())
	return element+1

def getElementName(at1):
	element = elementNames[at1-1]
	return element


### --- Open parent file --- ###
f = open(ifile)
ifileList = f.readlines()
f.close()
### --- Create some variables needed for parsing the input file --- ###
# ifilelength is used to gauge what line we are on and also allows us to determine the number of lines in the file
# ifilelol is a list of lists (lol) that will hold all the data of the input file
# a_list is a temp list that will be appended to the ifilelol
################################
ifileLength = 0
ifilelol = []
#### --- Input/parse the input file into a list of lists called ifilelol --- ###
for i, var in enumerate(ifileList):
	line = var.strip().split()
	a_list = []
	try:
		element = getElementNum(line[0])
	except (IndexError, ValueError) as e:
		print(e)
		continue
	a_list.append(element)
	a_list.append(Decimal(line[1]))
	a_list.append(Decimal(line[2]))
	a_list.append(Decimal(line[3]))
	ifilelol.append(list(a_list))
	ifileLength = ifileLength + 1

print('lines of data:', len(ifilelol))
### --- Get bonds --- ###
#print(ifilelol[0], type(ifilelol[0]))
#iFileAtomNum = ' '.join(ifilelol[0])
#iFileName = ' '.join(ifilelol[1])
covBonds = []
covHBonds = []
covTMBonds = []
nearestNeighbor = []
neighborStart = [0, 1000000]

### --- get the distance, angle and dihedrals for a Z-matrix --- ###
def getzmat(i):
	line = []
	index = i
	line.append(getElementName(ifilelol[index][0]))
	if i > 0:
		line.append(i)
		dist = getdistance(index-1, index, ifilelol)
		line.append(dist)
	if i > 1:
		line.append(i-1)
		angle = getangle(i, index-1, index, ifilelol)
		line.append(angle)
	if i > 2:
		line.append(i-2)
		dihedral = getdihedral(index-3, index-2, index-1, index, ifilelol)
		line.append(dihedral)
	line.append(-1)
	line.append(-1)
	line.append(-1)
	line.append(-1)
	line.append(-1)
	line.append(-1)
	line.append("\n")
	return line

### --- Get the XYZ coordinates from distance, angle and dihedral data --- ###
def getXYZfromZMAT(lol,at4):
	### Set up the variables to be used for the function
	dist = float(lol[2])
	angle = float(lol[4])
	dihedral = float(lol[6])
	angleRad = radians(angle) # * math.pi / 180
	dihedralRad = radians(dihedral) # * math.pi / 180
	at1 = int(lol[5])-1
	at2 = int(lol[3])-1
	at3 = int(lol[1])-1
	x = 0
	y = 0
	z = 0
	line = []

	### Start to place the atoms in their locations
	if at4 == 0:
		x = 0.00000
		y = 0.00000
		z = 0.00000
	
	elif at4 == 1:
		x = dist
		y = 0.00000
		z = 0.00000
	
	elif at4 == 2:
		a = xyzLOL[at3][1]
		b = dist
		x = a + (dist * cos(math.pi - angleRad))
		y = 0.00000
		z = -dist * sin(math.pi - angleRad)
		
	elif at4 >= 3:
		####The at4 x,y,z coordinates from spherical coord
		Sx = dist * sin(angleRad) * cos(dihedralRad)
		Sy = -dist * sin(angleRad) * sin(dihedralRad) #For some reason I need to have a negative here to get the correct sign in the output..... weird
		Sz = dist * cos(angleRad)
		at4L = [Sx, Sy, Sz]
		#print "at4L: " + str(at4L)

		###Finding the angle theta
		#Make the list of lists for the three point (z-axis, origin, and translated atom 2) needed for an angle calculation
		Z32 = [[0, 0, 0, 1],  [0, 0, 0, 0],  [0, xyzLOL[at2][1] - xyzLOL[at3][1], xyzLOL[at2][2] - xyzLOL[at3][2], xyzLOL[at2][3] - xyzLOL[at3][3]]]
		#Get theta using the getangle function
		theta = radians(getangle(0, 1, 2, Z32))
		#print "theta: " +str(theta)
		
		###Rodrigues' rotation formula
		#Create the vectprs needed to calculate k
		vector3 = array([xyzLOL[at3][1], xyzLOL[at3][2], xyzLOL[at3][3]])
		vector2 = array([xyzLOL[at2][1], xyzLOL[at2][2], xyzLOL[at2][3]])
		vector0 = array([0, 0, 1])
		#Calculate k for the Rodrigues rotation formula
		k = cross((vector2-vector3), vector0)/linalg.norm(cross((vector2-vector3), vector0))
		#Generate an array for translated 1
		T1 = [(xyzLOL[at1][1]-xyzLOL[at3][1]), (xyzLOL[at1][2]-xyzLOL[at3][2]), (xyzLOL[at1][3]-xyzLOL[at3][3])]
		#Calculate the Rodrigues rotation matrix
		RR23T1 = dot(T1, cos(theta)) + dot(cross(k,T1), sin(theta)) + dot(dot(k,(dot(k,T1))), (1-cos(theta)))
		#Make the list of lists for the four points (x-axis, z-axis, origin, and rotated translated 1) needed for a dihedral calculation
		XZ31 = [[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, RR23T1[0], RR23T1[1], RR23T1[2]]]
		#Get phi using the getdihedral function
		phi = radians(getdihedral(0,1,2,3,XZ31))
		#print "k: " + str(k)
		#print "T1: " + str(T1)
		#print "RR23T1: " + str(RR23T1)
		#print "XZ31: " + str(XZ31)
		#print "phi: " + str(phi)

		###Rotation matrix 
		#Create the array for the rotation matrix including dihedral phi
		RM = array([[cos(phi), sin(phi), 0], [-sin(phi), cos(phi), 0], [0, 0, 1]])
		#Calculate the dot product of the rotation matrix and the coordinates for 4 (from spherical)
		RM4 = dot(RM, at4L)
		#Calculate the rotated coordinates of the rotated coordinates of atom 4
		RRN23RM4 = dot(RM4, cos(-theta)) + dot(cross(k,RM4), sin(-theta)) + dot(dot(k,(dot(k,RM4))), (1-cos(-theta)))
		#print "RM: " + str(RM)
		#print "RM4: " + str(RM4)
		#print "RRN23RM4: " + str(RRN23RM4)
		#Final coordinates that are rotated, rotated and translated
		x = RRN23RM4[0] + xyzLOL[at3][1]
		y = RRN23RM4[1] + xyzLOL[at3][2]
		z = RRN23RM4[2] + xyzLOL[at3][3]
		#print x
		#print y
		#print z
	#Putting everything into a list to send back
	line.append(lol[0])
	line.append(x)
	line.append(y)
	line.append(z)
	#line.append("\n")
	return line

### --- Generate a list of lists for the zmatrix of the structure --- ###
zmatlol = []
for i in range(len(ifilelol)):
	linetemp = getzmat(i)
	zmatlol.append(linetemp)
	#a_list[:] =[]

### --- Output file in Z-matrix format --- ###
f = open(ofile, 'w+')
#f.write(str(iFileAtomNum))
#f.write(str(iFileName) + "\n")
for i in range(0, len(zmatlol)):
	linetemp = [x for x in zmatlol[i] if x != -1]
	line = '\t'.join(str(e) for e in linetemp) #, e != -1)
	f.write(line)
f.close()

### --- Print out the xyz from the zmatrix --- ###
if printfile == 1:
	xyzLOL = []
	print(iFileAtomNum)
	#print ""
	for i in range(0,int(iFileAtomNum)):
		linetemp = getXYZfromZMAT(zmatlol[i],i)
		xyzLOL.append(linetemp)
		print('   '.join(str(e) for e in linetemp))


######################################################################
### END OF SCRIPT	
######################################################################
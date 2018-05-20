XYZ_EXTENSION = '.xyz'
ZMAT_EXTENSION = '.zmat'



def get_zmat_filename(xyz_filename):
    zmat_filename = xyz_filename.replace(XYZ_EXTENSION, ZMAT_EXTENSION)
    return zmat_filename

def get_xyz_filename(zmat_filename):
    xyz_filename = zmat_filename.replace(ZMAT_EXTENSION, XYZ_EXTENSION)
    return xyz_filename

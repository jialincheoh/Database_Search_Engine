import subprocess
from helpers import get_zmat_filename


def xyz2zmat(xyz_filename, zmat_filename=None):
    if not zmat_filename:
        zmat_filename = get_zmat_filename(xyz_filename)
    args = [
        "babel",
        "-i",
        "xyz",
        xyz_filename,
        "-o",
        "fh",
        zmat_filename,
    ]
    #print(' '.join(args))
    status = subprocess.check_call(args)
    #print('Converted {} to {}, status={}'.format(xyz_filename, zmat_filename, status))

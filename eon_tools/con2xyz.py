'''
Read a .con file from AKMC results and write the structure as an .xyz file
'''

from ase.io import read
from ase.io import write

def read_file(filename):
    '''
    Take the base name from filename.
    Append the ".con" extension.
    Read the file.
    Return the structure.
    '''
    fname = filename+".con"
    structure = read(fname)
    return structure

def write_file(filename,structure):
    '''
    Take the base name from filename.
    Append the ".xyz" extension.
    Write the file.
    '''
    fname = filename+".xyz"
    write(fname,structure)

def convert(filename):
    '''
    Convert filename.con to filename.xyz
    '''
    structure = read_file(filename)
    write_file(filename,structure)

def arguments():
    '''
    Read command line arguments.

    In this case the only available command line argument is
    the base filename.
    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="the filename without extension")
    return parser.parse_args()

if __name__ == "__main__":
    args = arguments()
    convert(args.filename)

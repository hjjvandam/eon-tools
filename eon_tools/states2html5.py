'''
Convert a "states" directory to an HTML webpage
'''
from ase.io import read
from ase.io import write
from ase.neb import NEB

def find_states(statespath):
    '''
    Find the states in the AKMC simulation

    Statespath is the path to the states directory. In this
    directory there is a file "state_table". This file
    lists all the states and their corresponding energy.
    We just read the state label and return them in a list.
    '''
    statetable = statespath+"/state_table"
    fp = open(statetable)
    intable = fp.readlines()
    fp.close()
    table=[]
    for state in intable:
        state = state.split()
        table.append(state[0])
    return table

def find_processes(statespath,statename):
    '''
    Find the processes for a given state
    '''
    processtable = statespath+"/"+statename+"/processtable"
    fp = open(processtable)
    intable = fp.readlines()
    intable = intable[1:] # The first line is a comment
    table = []
    for process in intable:
        process = process.split()
        if process[3] != "-1":
            table.append(process[0])
    return table

def convert_con2img(statespath,statename,processname,movies):
    '''
    Convert the configuration files to image files

    For every process there 3 files:
    - reactant
    - saddle point
    - product
    we convert all these files to image files.
    '''
    fn_reactant = statespath+"/"+statename+"/procdata/reactant_"+processname
    fn_saddle   = statespath+"/"+statename+"/procdata/saddle_"+processname
    fn_product  = statespath+"/"+statename+"/procdata/product_"+processname
    fn_reaction = statespath+"/"+statename+"/procdata/reaction_"+processname
    structure_r = read(fn_reactant+".con")
    structure_s = read(fn_saddle+".con")
    structure_p = read(fn_product+".con")
    if movies:
        images = [structure_r]
        images += [structure_r.copy() for i in range(8)]
        images += [structure_p]
        neb = NEB(images)
        neb.interpolate()
        write(fn_reaction+".xyz",images)
    else:
        write(fn_reactant+".xyz",structure_r)
        write(fn_saddle+".xyz",structure_s)
        write(fn_product+".xyz",structure_p)
    

def html_process(fp_html,statespath,statename,processname,movies):
    '''
    Add the process images to the HTML file

    We put all images into a table. Here we add one row to the table.
    '''
    fn_reactant = statespath+"/"+statename+"/procdata/reactant_"+processname+".xyz"
    fn_saddle   = statespath+"/"+statename+"/procdata/saddle_"+processname+".xyz"
    fn_product  = statespath+"/"+statename+"/procdata/product_"+processname+".xyz"
    fn_reaction = statespath+"/"+statename+"/procdata/reaction_"+processname+".xyz"
    fp_html.write("<TR><TD>")
    fp_html.write(statename)
    fp_html.write("</TD><TD>")
    fp_html.write(processname)
    fp_html.write("</TD><TD>")
    if movies:
        line="<script>jmolApplet(400,\"load "+fn_reaction+"\",\"0\")</script>"
        fp_html.write(line)
    else:
        line="<script>jmolApplet(200,\"load "+fn_reactant+"\",\"0\")</script>"
        fp_html.write(line)
        fp_html.write("</TD><TD>")
        line="<script>jmolApplet(200,\"load "+fn_saddle+"\",\"0\")</script>"
        fp_html.write(line)
        fp_html.write("</TD><TD>")
        line="<script>jmolApplet(200,\"load "+fn_product+"\",\"0\")</script>"
        fp_html.write(line)
    fp_html.write("</TD></TR>\n")

def doit(statespath,movies):
    '''
    Go through the whole thing

    For information see: https://www.youtube.com/watch?v=sIr-aeRCXPI
    '''
    fp_html=open("index.html","w")
    fp_html.write("<!DOCTYPE HTML>\n")
    fp_html.write("<HTML>\n")
    fp_html.write("<HEAD>\n")
    fp_html.write("  <SCRIPT src="../jmol/jsmol/JSmol.min.js"></script>\n")
    fp_html.write("  <SCRIPT src="../jmol/jsmol/js/Jmol2.js"></script>\n")
    fp_html.write("  <SCRIPT> jmolInitialize("../jmol/jsmol");</script>\n")
    fp_html.write("</HEAD>\n")
    fp_html.write("<BODY>\n")
    fp_html.write("<TABLE>\n")
    stateslist = find_states(statespath)
    for state in stateslist:
        processlist = find_processes(statespath,state)
        for process in processlist:
            convert_con2img(statespath,state,process,movies)
            html_process(fp_html,statespath,state,process,movies)
    fp_html.write("</TABLE>\n")
    fp_html.write("</BODY>\n")
    fp_html.write("</HTML>\n")

def arguments():
    '''
    Read command line arguments.

    In this case the only available command line argument is
    the states pathname.
    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pathname", type=str, help="the pathname for the states directory, i.e. where the file \"state_table\" lives")
    parser.add_argument("--movies", dest="movies", default=False, action='store_const', const=True, help="if provided generate movies of the reaction processes")
    return parser.parse_args()

if __name__ == "__main__":
    args = arguments()
    doit(args.pathname,args.movies)

# eon-tools
Python utilities to analyze results produced with the EON kinetic Monte Carlo code

## EON

[EON](https://theory.cm.utexas.edu/eon/) is a program for performing adaptive kinetic Monte Carlo simulations.
When running simulations with this code a directory of results is produced. This directory contains a 
wealth of information captured in a lot of data. However, the EON package seems to come with few tools
to extract this information from the data. Hence I wrote some tools to help me with this. These tools
are provided in this repo so that:

* I don't loose them and 
* you can use them

These tools are provided as is without any warranty of any kind.

## Notes

EON uses a ".con" file format to store the atomic configurations. This file format seems to be
unique to EON. Therefore these files need to be converted before they can be used for most 
purposes. As a result the string "con" appears in the name of a number of tools.

EON also creates a "states" directory that contains the results from the simulation.
Tools that operate on this entire data collection will have the string "states" in the name.

## Dependencies

These tools use the following packages:

* [Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/index.html)


The program can generate a valid crossword puzzle given two inputs files in command line:
	1. structure file (.txt file)
	2. words file (.txt file)

Go to the directory and run the 'generate.py' program. This will output a valid crossword puzzle in the command line from the given
the constraints presented by the set of words (from the words file) and the structure of the puzzle (from by the structure file).

Some examples of strcutyre file and words file are already given in the 'data' folder that can be used to run the program. 
For example: 	'python3 generate.py data/structure1.txt data/words1.txt'

Requirement: Python Version 3.5 or higher 

structure file format: the program will input the '_' characters in the structure as blank spaces where words can be put in and
treat the '#' characters as solid blocks. Open the example files for better understanding. 

words file format: This file contains one word per line. The program will only use the words mentioned in this file for generating
the cross-word puzzle. 

 

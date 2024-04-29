pmpv: an interpreter for a tiny toy language (PMPV).


Israk Ayasin


Course work (Homework 1) for COS 301 Programming Languages class
Spring 2024
University of Maine

Manifest:
    * README.txt: this file; overview and instructions
    * pmpv: main file contains all the code
    * in.txt: sample input files
    * out.txt: sample output files, with corresponding numbers from in.txt
Requirements:
    - POSIX-like enviornment (for shell script)

Running:
    python .\pmpv.py

    This command will let you type anything that is valid for this calculator. Which includ Plus, Minus, Parenthesis, and variables.

    Input and output can be redirected. For example:
    Get-Content .\in.txt | python .\pmpv.py > out.txt

    This command is for PowerShell

Bugs and limitation:
* More testing needed
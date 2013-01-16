acidic.py
=========

An interpreter for the ACIDIC programming language written in Python.

Usage: acidic [OPTION] file

Options:

-1, --once        loop through the command stack only once i.e. run the
                  program as if there were a BRK at the end of the command stack
-A int            initialize accumulator A to int
-B int            initialize accumulator B to int
-e int            begin executing commands at command int
-S str            set the storage stack to str
-C str            set the command stack to str
-V                be extremely verbose in output -- NOT IMPLEMENTED YET
-c, --commands    print a list of the commands in the ACIDIC language and exit
-h, --help        print this help and exit
-v, --version     print version info and exit

For more information on the ACIDIC programming language, see
http://esolangs.org/wiki/ACIDIC

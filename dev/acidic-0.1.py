#!/usr/bin/env python3

# this interpreter is based on the info at http://esolangs.org/wiki/ACIDIC

EXIT_SUCCESS = 0
EXIT_NO_FILE_SPECIFIED = 1
EXIT_NOT_TWO_LINES = 2
EXIT_FILE_DNE = 3

ACIDIC_HELP = \
"""Usage: acidic [OPTION] file

Options:
    -1    run the program as if there were a BRK at the end of the command stack
    -c    print a list of the commands in the ACIDIC language and exit
    -h    print this help and exit
    -v    print version info and exit

For more information on the ACIDIC programming language, see
http://esolangs.org/wiki/ACIDIC"""

ACIDIC_VERSION = \
"""acidic 0.1"""

ACIDIC_COMMANDS = \
"""PUSH :  <space>   3   F   Y   l
Pushes the leftmost value of the Storage Stack onto the Command Stack.

POP :   !   4   G   Z   m
Pops the value to the left of it onto the Storage Stack.

ROT :   "   5   H   [   n
Rotates the Storage Stack once to the right.

INC :   #   6   I   \   o
Increments A.

DEC :   $   7   J   ]   p
Decrements A.

JUMP :  %   8   K   ^   q
Jumps to the command pointed to by A (starting at the left, of course).

STKSZE :    &   9   L   _   r
Makes A equal to the size of the Storage Stack.

JMPR :  '   :   M   `   s
Jumps A spaces to the left.

PUSHR : (   ;   N   a   t
Pushes the value at A on the Storage Stack onto the Command Stack.

POPR :  )   <   O   b   u
Pops the command at A onto the Storage Stack.

OUTPUT :    *   =   P   c   v
Displays the Storage Stack.

BRK :   +   >   Q   d   w
Ends the program.

EXC :   ,   ?   R   e   x
Exchanges B with A.

INPUT : -   @   S   f   y
Sets A to the value at STDIN.

RPLC :  .   A   T   g   z
Replaces this command with a command in the Storage Stack in the same column.

ROTA :  /   B   U   h   {
Rotates the Storage Stack A times to the right.

JMPZ :  0   C   V   i   |
Jumps to the command pointed to by A if B is equal to 0.

JMPNZ : 1   D   W   j   }
Jumps to the command pointed to by A if B is not equal to 0.

PLC :   .   A   T   g   z
Sets A to the current pointer position."""

import os
import sys

# the accumulators A and B, basically just pointers
accA = 0
accB = 0

# the storage and command stacks
storagestack = ''
commandstack = ''

# instruction pointer, this will get set to the length of the command stack
# when the program begins
ipointer = 0

# command line options
opt_looponce = False

# all of the language's function definitions
def PUSH():
    """ 3FYl : Pushes the leftmost value of the Storage Stack onto the Command Stack."""
    global storagestack, commandstack
    commandstack = storagestack[0] + commandstack
    storagestack = storagestack[1:]
	# no need to change ipointer because you're moving left by adding a command to the front of the stack

def POP():
    """!4GZm : Pops the value to the left of it onto the Storage Stack."""
    global storagestack, commandstack, ipointer
    storagestack = commandstack[ipointer - 1] + storagestack
    commandstack = commandstack[:ipointer - 1] + commandstack[ipointer:]
    ipointer -= 2
	# decrement ipointer by 2 because you're moving right by removing a command from the stack

def ROT():
    """"5H[n : Rotates the Storage Stack once to the right."""
    global storagestack, ipointer
    storagestack = storagestack[-1] + storagestack[:-1]
    ipointer -= 1

def INC():
    """#6I\o : Increments A."""
    global accA, ipointer
    accA += 1
    ipointer -= 1

def DEC():
    """$7J]p : Decrements A."""
    global accA, ipointer
    accA -= 1
    ipointer -= 1

def JUMP():
    """%8K^q : Jumps to the command pointed to by A (starting at the left, of course)."""
    global ipointer
    ipointer = accA

def STKSZE():
    """&9L_r : Makes A equal to the size of the Storage Stack."""
    global accA
    accA = len(storagestack)
    ipointer =- 1

def JMPR():
    """':M`s : Jumps A spaces to the left."""
    global ipointer
    ipointer -= accA

def PUSHR():
    """(;Nat : Pushes the value at A on the Storage Stack onto the Command Stack."""
    global storagestack, commandstack, ipointer
    commandstack = storagestack[accA] + commandstack
    storagestack = storagestack[:accA] + storagestack[accA + 1:]
    ipointer -= 1

def POPR():
    """)<Obu : Pops the command at A onto the Storage Stack."""
    global storagestack, commandstack, ipointer
    storagestack = commandstack[accA] + storagestack
    commandstack = commandstack[:accA] + commandstack[accA + 1:]
    ipointer -= 1

def OUTPUT():
    """*=Pcv : Displays the Storage Stack."""
    global ipointer
    print(storagestack)
    ipointer -= 1

def BRK():
    """+>Qdw : Ends the program."""
    exit(EXIT_SUCCESS)

def EXC():
    """,?Rex : Exchanges B with A."""
    global accA, accB, ipointer
    accA, accB = accB, accA
    ipointer -= 1

def INPUT():
    """-@Sfy : Sets A to the value at STDIN."""
    global ipointer
    accA = input()
    ipointer -= 1

def RPLC():
    """.ATgz : Replaces this command with a command in the Storage Stack in the same column."""
    global commandstack, storagestack, ipointer
    commandstack = commandstack[:ipointer] + storagestack[ipointer] + commandstack[ipointer + 1:]

def ROTA():
    """/BUh{ : Rotates the Storage Stack A times to the right."""
    global storagestack, ipointer
    counter = 0
    while counter < accA:
        storagestack = storagestack[-1] + storagestack[:-1]
        counter += 1
    ipointer -= 1

def JMPZ():
    """0CVi| : Jumps to the command pointed to by A if B is equal to 0."""
    global ipointer
    if accB == 0:
        ipointer = accA
    else:
        ipointer -= 1

def JMPNZ():
    """1DWj} : Jumps to the command pointed to by A if B is not equal to 0."""
    global ipointer
    if accB != 0:
        ipointer = accA
    else:
        ipointer -= 1

def PLC():
    """.ATgz : Sets A to the current pointer position."""
    global accA, ipointer
    accA = ipointer
    ipointer -= 1

# a dict which maps every function's 5 possible characters
# to their function
commands = \
  {
    " 3FYl" : PUSH,
    "!4GZm" : POP,
    "\"5H[n" : ROT,
    "#6I\\o" : INC,
    "$7J]p" : DEC,
    "%8K^q" : JUMP,
    "&9L_r" : STKSZE,
    "':M`s" : JMPR,
    "(;Nat" : PUSHR,
    ")<Obu" : POPR,
    "*=Pcv" : OUTPUT,
    "+>Qdw" : BRK,
    ",?Rex" : EXC,
    "-@Sfy" : INPUT,
    ".ATgz" : RPLC,
    "/BUh{" : ROTA,
    "0CVi|" : JMPZ,
    "1DWj}" : JMPNZ,
    "2EXk~" : PLC,
  }

def interpret(inputtext):
    global storagestack, commandstack, ipointer
    """Interpret an ACIDIC program."""
    lines = inputtext[:-1].split('\n')
    if len(lines) != 2:
        print("An ACIDIC program must contain exactly 2 lines. Aborting.", file = sys.stderr)
        exit(EXIT_NOT_TWO_LINES)
    storagestack = lines[0]
    print("ss:", storagestack); exit() #debug
    commandstack = lines[1]
    ipointer = len(commandstack) - 1
    while ipointer >= 0:
        command = commandstack[ipointer]
        for chars in commands:
            if command in chars:
                commands[chars]()
        if ipointer < 0 and opt_looponce == False:
            ipointer = len(commandstack) - 1

def handlecommandlineoptions():
    global opt_looponce
    if "-1" in sys.argv:
        opt_looponce = True
    if "-c" in sys.argv:
        print(ACIDIC_COMMANDS)
        exit(EXIT_SUCCESS)
    if "-h" in sys.argv:
        print(ACIDIC_HELP)
        exit(EXIT_SUCCESS)
    if "-v" in sys.argv:
        print(ACIDIC_VERSION)
        exit(EXIT_SUCCESS)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        handlecommandlineoptions()
        if not os.path.exists(sys.argv[-1]):
            print("Specified file does not exist.", file = sys.stderr)
            exit(EXIT_FILE_DNE)
        interpret(open(sys.argv[-1], 'r').read())
    else:
        print("No file specified.\n", file = sys.stderr)
        print(ACIDIC_HELP)
        exit(EXIT_NO_FILE_SPECIFIED)

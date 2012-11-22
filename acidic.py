#!/usr/bin/env python3

# this interpreter is based on the info at http://esolangs.org/wiki/ACIDIC

ACIDIC_EXIT_SUCCESS = 0
ACIDIC_EXIT_NO_FILE_SPECIFIED = 1
ACIDIC_EXIT_NOT_TWO_LINES = 2
ACIDIC_EXIT_FILE_DNE = 3

ACIDIC_HELP = \
"""Usage: acidic [OPTION] file

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
http://esolangs.org/wiki/ACIDIC"""

ACIDIC_VERSION = \
"""acidic 0.2"""

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

class AcidicInterpreter:
    def __init__(self, ipointer_init = 0, accumulator_A_init = 0, accumulator_B_init = 0, opt_looponce = False, storage_stack_init = '', command_stack_init = ''):
        # + 1 because we're starting at the end i.e. command_stack[-1]
		# for the user this means specifying "-e 0" will still start at the first command
        self.ipointer = ipointer_init + 1

        self.accumulator_A = accumulator_A_init 
        self.accumulator_B = accumulator_B_init 

        self.storage_stack = storage_stack_init
        self.command_stack = command_stack_init

        self.opt_looponce = opt_looponce

        self.command_map = \
          {
            " 3FYl" : self.PUSH,
            "!4GZm" : self.POP,
            "\"5H[n" : self.ROT,
            "#6I\\o" : self.INC,
            "$7J]p" : self.DEC,
            "%8K^q" : self.JUMP,
            "&9L_r" : self.STKSZE,
            "':M`s" : self.JMPR,
            "(;Nat" : self.PUSHR,
            ")<Obu" : self.POPR,
            "*=Pcv" : self.OUTPUT,
            "+>Qdw" : self.BRK,
            ",?Rex" : self.EXC,
            "-@Sfy" : self.INPUT,
            ".ATgz" : self.RPLC,
            "/BUh{" : self.ROTA,
            "0CVi|" : self.JMPZ,
            "1DWj}" : self.JMPNZ,
            "2EXk~" : self.PLC,
          }

    def SetCode(self, code = '', storage_stack = '', command_stack = ''):
        if not code:
            self.storage_stack = ''
            self.command_stack = ''
        else:
            if code[-1] == '\n':
                self.code = code[:-1].split('\n')
            else:
                self.code = code.split('\n')

            if len(self.code) != 2:
                exit(ACIDIC_EXIT_NOT_TWO_LINES)

            self.storage_stack = self.code[0]
            self.command_stack = self.code[1]
        if storage_stack:
            self.storage_stack = storage_stack
        if command_stack:
            self.command_stack = command_stack

    def Interpret(self, code = ''):
        if code:
            self.SetCode(code)
        while self.ipointer < len(self.command_stack) + 1:
            current_command = self.command_stack[-self.ipointer]
            for chars in self.command_map:
                if current_command in chars:
                    #print("cmd:", current_command, "ip:", self.ipointer, "cs:", self.command_stack, "ss:", self.storage_stack) #debug
                    self.command_map[chars]()
            if self.ipointer >= len(self.command_stack) + 1 and self.opt_looponce == False:
                self.ipointer = 1

    # all of the language's function definitions
    def PUSH(self):
        """ 3FYl : Pushes the leftmost value of the Storage Stack onto the Command Stack."""
        self.command_stack = self.storage_stack[0] + self.command_stack
        self.storage_stack = self.storage_stack[1:]
        self.ipointer += 1

    def POP(self):
        """!4GZm : Pops the value to the left of it onto the Storage Stack."""
        self.storage_stack = self.command_stack[-(self.ipointer + 1)] + self.storage_stack
        self.command_stack = self.command_stack[:-(self.ipointer + 1)] + self.command_stack[-self.ipointer:]
        self.ipointer += 1

    def ROT(self):
        """"5H[n : Rotates the Storage Stack once to the right."""
        self.storage_stack = self.storage_stack[-1] + self.storage_stack[:-1]
        self.ipointer += 1

    def INC(self):
        """#6I\o : Increments A."""
        self.accumulator_A += 1
        self.ipointer += 1

    def DEC(self):
        """$7J]p : Decrements A."""
        self.accumulator_A -= 1
        self.ipointer += 1

    def JUMP(self):
        """%8K^q : Jumps to the command pointed to by A (starting at the left, of course)."""
        self.ipointer = self.accumulator_A

    def STKSZE(self):
        """&9L_r : Makes A equal to the size of the Storage Stack."""
        self.accumulator_A = len(self.storage_stack)
        self.ipointer += 1

    def JMPR(self):
        """':M`s : Jumps A spaces to the left."""
        self.ipointer += self.accumulator_A + 1

    def PUSHR(self):
        """(;Nat : Pushes the value at A on the Storage Stack onto the Command Stack."""
        self.command_stack = self.storage_stack[self.accumulator_A] + self.command_stack
        self.storage_stack = self.storage_stack[:self.accumulator_A] + self.storage_stack[self.accumulator_A + 1:]
        self.ipointer += 1

    def POPR(self):
        """)<Obu : Pops the command at A onto the Storage Stack."""
        self.storage_stack = self.command_stack[self.accumulator_A] + self.storage_stack
        self.command_stack = self.command_stack[:self.accumulator_A] + self.command_stack[self.accumulator_A + 1:]
        self.ipointer += 1

    def OUTPUT(self):
        """*=Pcv : Displays the Storage Stack."""
        print(self.storage_stack)
        self.ipointer += 1

    def BRK(self):
        """+>Qdw : Ends the program."""
        exit(ACIDIC_EXIT_SUCCESS)

    def EXC(self):
        """,?Rex : Exchanges B with A."""
        self.accumulator_A, self.accumulator_B = self.accumulator_B, self.accumulator_A
        self.ipointer += 1

    def INPUT(self):
        """-@Sfy : Sets A to the value at STDIN."""
        self.accumulator_A = input()
        self.ipointer += 1

    def RPLC(self):
        """.ATgz : Replaces this command with a command in the Storage Stack in the same column."""
        self.command_stack = self.command_stack[:-self.ipointer] + (self.storage_stack[len(self.command_stack) - self.ipointer] if len(self.storage_stack) >= len(self.command_stack) else '') + (self.command_stack[-(self.ipointer - 1):] if self.ipointer >= 2 else '')
        # this inline if is to prevent the error that would occur when trying to replace the command at [-1]

    def ROTA(self):
        """/BUh{ : Rotates the Storage Stack A times to the right."""
        counter = 0
        while counter < self.accumulator_A:
            self.storage_stack = self.storage_stack[-1] + self.storage_stack[:-1]
            counter += 1
        self.ipointer += 1

    def JMPZ(self):
        """0CVi| : Jumps to the command pointed to by A if B is equal to 0."""
        if self.accumulator_B == 0:
            self.ipointer = self.accumulator_A + 1
        else:
            self.ipointer += 1

    def JMPNZ(self):
        """1DWj} : Jumps to the command pointed to by A if B is not equal to 0."""
        if self.accumulator_B != 0:
            self.ipointer = self.accumulator_A + 1
        else:
            self.ipointer += 1

    def PLC(self):
        """.ATgz : Sets A to the current pointer position."""
        self.accumulator_A = self.ipointer
        self.ipointer += 1

def GetOptions():
    ipointer = 0
    accumulator_A = 0
    accumulator_B = 0
    storage_stack = ''
    command_stack = ''
    opt_looponce = False
    input_files = []

    # start at 1 to skip the command itself being counted in the arguments
    current_opt = 1
    while current_opt < len(sys.argv):
        if sys.argv[current_opt] in ("-1", "--once"):
            opt_looponce = True
        elif sys.argv[current_opt] == "-A":
            accumulator_A = int(sys.argv[current_opt + 1])
            current_opt += 1
        elif sys.argv[current_opt] == "-B":
            accumulator_B = int(sys.argv[current_opt + 1])
            current_opt += 1
        elif sys.argv[current_opt] == "-e":
            ipointer = int(sys.argv[current_opt + 1])
            current_opt += 1
        elif sys.argv[current_opt] == "-S":
            storage_stack = sys.argv[current_opt + 1]
            current_opt += 1
        elif sys.argv[current_opt] == "-C":
            command_stack = sys.argv[current_opt + 1]
            current_opt += 1
        elif sys.argv[current_opt] in ("-c", "--commands"):
            print(ACIDIC_COMMANDS)
            exit(ACIDIC_EXIT_SUCCESS)
        elif sys.argv[current_opt] in ("-h", "--help"):
            print(ACIDIC_HELP)
            exit(ACIDIC_EXIT_SUCCESS)
        elif sys.argv[current_opt] in ("-v", "--version"):
            print(ACIDIC_VERSION)
            exit(ACIDIC_EXIT_SUCCESS)
        else:
            input_files.append(sys.argv[current_opt])
        current_opt += 1

    return {"ipointer": ipointer, "accumulator_A": accumulator_A, "accumulator_B": accumulator_B, "storage_stack": storage_stack, "command_stack": command_stack, "opt_looponce": opt_looponce, "input_files": input_files}

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        options = GetOptions()
        if len(options["input_files"]) == 0:
            print("No file specified.\n", file = sys.stderr)
            print(ACIDIC_HELP)
            exit(ACIDIC_EXIT_NO_FILE_SPECIFIED)
        the_interpreter = AcidicInterpreter(options["ipointer"], options["accumulator_A"], options["accumulator_B"], options["opt_looponce"])
        for input_file in options["input_files"]:
            if not os.path.exists(input_file):
                print("Specified file does not exist:", input_file, file = sys.stderr)
                exit(ACIDIC_EXIT_FILE_DNE)
            else:
                if len(options["input_files"]) > 1:
                    print("File:", input_file)
                file_contents = open(input_file, 'r')
                the_interpreter.SetCode(file_contents.read(), storage_stack = options["storage_stack"], command_stack = options["command_stack"])
                the_interpreter.Interpret()
    else:
        print("No file specified.\n", file = sys.stderr)
        print(ACIDIC_HELP)
        exit(ACIDIC_EXIT_NO_FILE_SPECIFIED)

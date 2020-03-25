"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 40 # Each element will containt 8 bits so 8 * 32 = 256 total bits
        self.reg = [0] * 8
        
        ADD = 0b10100000
        MULT = 0b10100010
        PRINT = 0b01000111
        LDI = 0b10000010
        HLT = 0b00000001
        PUSH = 0b01000101
        POP = 0b01000110
    

        self.branchtable = {}
        self.branchtable[ADD] = self.add
        self.branchtable[MULT] = self.mult
        self.branchtable[PRINT] = self.prn
        self.branchtable[LDI] = self.ldi
        self.branchtable[HLT] = self.hlt
        self.branchtable[POP] = self.pop
        self.branchtable[PUSH] = self.push
        self.branchtable[LDI] = self.ldi

        self.PC = 0
        self.IR = 0
        # Stack Pointer
        self.SP = len(self.ram) - 1

    def load(self, program = None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        
        if len(sys.argv) > 1:
            file_name = sys.argv[1]
            program = open(file_name)
            program = program.read().split("\n")
            new_program = []
            for string in program:

                # Ignore comments
                if "#" in string:
                    string = string.split("#")[0]
                
                # Ignore empty lines
                if string != '':
                    new_program.append(string)

            program = new_program

            for instruction in program:
                self.ram[address] = int(instruction, 2)
                address += 1
        else:
            
            for instruction in program:
                self.ram[address] = instruction
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def mult(self,reg_a, reg_b):
        """
        places the product of reg_a and reg_b into reg_a
        """
        self.reg[reg_a] *= self.reg[reg_b]
        self.PC += 3

    def add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.PC += 3

    def subtract(self, reg_a, reg_b):
        self.alu("SUB", reg_a, reg_b)
        self.PC += 3

    def prn(self, reg_a, reg_b):
        print(self.reg[reg_a])
        self.PC += 2

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def ram_read(address):
        return self.ram[address]

    def ram_write(address, value):
        self.ram[address] = value

    def hlt(self, reg_a, reg_b):
        quit()

    def push(self, reg_a, reg_b):
        val = self.reg[reg_a]
        # Copy the value in the given register to the address pointed 
        self.ram[self.SP] = val
        # Decrement the Stack Pointer
        self.SP -= 1
        # Increase Program counter
        self.PC += 2
    
    def pop(self, reg_a, reg_b):
        #TODO
        val = self.ram[self.SP + 1]
        # copy the value from the address pointed to by SP to the given register
        self.reg[reg_a] = val
        
        # Remove value from memory
        self.ram[self.SP + 1] = 0
        # Increment Stack Pointer
        self.SP += 1
        # Increment Program Counter
        self.PC += 2

    def ldi(self, reg_a, i):
        self.reg[reg_a] = i
        self.PC += 3

    def run(self):

        while self.PC <= len(self.ram):
            IR = self.ram[self.PC]
            print("IR:",bin(IR))
            self.branchtable[IR](self.ram[self.PC + 1], self.ram[self.PC + 2])


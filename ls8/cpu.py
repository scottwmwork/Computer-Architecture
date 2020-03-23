"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 32 # Each element will containt 8 bits so 8 * 32 = 256 total bits
        self.reg = [0] * 8

    def load(self, program = None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if program == None:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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

        print()

    def ram_read(address):
        return self.ram[address]

    def ram_write(address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        PC = 0
        IR = 0

        running = True
        while running == True:
            
            #LDI
            if self.ram[PC] == 0b10000010:
                registor_address = self.ram[PC + 1]
                value = self.ram[PC + 2]
                self.reg[registor_address] = value
                PC += 3
            
            # PRN
            if self.ram[PC] == 0b01000111:
                registor_address = self.ram[PC + 1]
                print(self.reg[registor_address])
                PC += 2
            # HLT
            if self.ram[PC] == 0b00000001:
                quit()

            # Condition to stop running once done with program
            # if self.ram[PC] == 0b00000000:
            #     quit()

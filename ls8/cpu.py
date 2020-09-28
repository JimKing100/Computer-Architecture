"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 244
        self.running = True
        self.branchtable = {}
        self.branchtable[LDI] = self.run_ldi
        self.branchtable[PRN] = self.run_prn
        self.branchtable[HLT] = self.run_hlt
        self.branchtable[MUL] = self.run_mul
        self.branchtable[ADD] = self.run_add
        self.branchtable[PUSH] = self.run_push
        self.branchtable[POP] = self.run_pop
        self.branchtable[CALL] = self.run_call
        self.branchtable[RET] = self.run_ret

    def run_ldi(self):
        register_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[register_num] = value
        self.pc += 3

    def run_prn(self):
        register_num = self.ram_read(self.pc + 1)
        print(self.reg[register_num])
        self.pc += 2

    def run_mul(self):
        register_a = self.ram_read(self.pc + 1)
        register_b = self.ram_read(self.pc + 2)
        self.alu('MUL', register_a, register_b)
        self.pc += 3

    def run_add(self):
        register_a = self.ram_read(self.pc + 1)
        register_b = self.ram_read(self.pc + 2)
        self.alu('ADD', register_a, register_b)
        self.pc += 3

    def run_push(self):
        register_num = self.ram_read(self.pc + 1)
        value = self.reg[register_num]
        self.sp -= 1
        self.ram_write(self.sp, value)
        self.pc += 2

    def run_pop(self):
        register_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.sp)
        self.reg[register_num] = value
        self.sp += 1
        self.pc += 2

    def run_call(self):
        register_num = self.ram_read(self.pc + 1)
        self.sp -= 1
        self.ram_write(self.sp, self.pc + 2)
        self.pc = self.reg[register_num]

    def run_ret(self):
        self.pc = self.ram_read(self.sp)
        self.sp += 1

    def run_hlt(self):
        self.running = False

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) == 2:
            filename = sys.argv[1]
        else:
            print('No filename provided')
            return None

        with open(filename) as file_in:
            program = []
            for line in file_in:
                str = line[0:8]
                if str.isnumeric():
                    final_str = '0b' + str
                    program.append(int(final_str, base=2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        if len(sys.argv) == 2:
            while self.running:
                ir = self.ram_read(self.pc)
                self.branchtable[ir]()

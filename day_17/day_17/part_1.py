from typing import Optional


class Machine:
    def __init__(self, reg_a: int, reg_b: int, reg_c: int, instructions: list[int], debug: Optional[bool] = None) -> None:
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.instructions = instructions
        self.instruction_pointer = 0
        self.output: list[int] = []
        self.debug = debug
        # if self.debug: print('Machine initialized with registers:', self.reg_a, self.reg_b, self.reg_c, 'and instructions:', self.instructions)

    def _get_combo_operand(self, operand: int) -> int:
        if operand == 7:
            raise ValueError('Invalid operand')

        if operand == 4:
            return self.reg_a
        if operand == 5:
            return self.reg_b
        if operand == 6:
            return self.reg_c

        return operand

    def _get_opcode(self) -> int:
        op_code = self.instructions[self.instruction_pointer]
        self.instruction_pointer += 1
        return op_code

    def _get_operand(self) -> int:
        operand = self.instructions[self.instruction_pointer]
        self.instruction_pointer += 1
        return operand

    def _div(self, operand: int) -> int:
        numerator = self.reg_a
        denominator = self._get_combo_operand(operand)
        # if self.debug: print('adv', numerator, denominator, numerator // (2 ** denominator))
        return numerator // (2 ** denominator)

    def _adv(self, operand: int) -> None:
        # if self.debug: print('advancing with operand:', operand)
        self.reg_a = self._div(operand)

    def _bxl(self, operand: int) -> None:
        # if self.debug: print('bxl with operand:', operand, self.reg_b^operand)
        b = self.reg_b
        self.reg_b = b ^ operand

    def _bst(self, operand: int) -> None:
        # if self.debug: print('bst with operand:', operand, self._get_combo_operand(operand) % 8)
        op = self._get_combo_operand(operand)
        self.reg_b = op % 8
    
    def _jnz(self, operand: int) -> None:
        if self.reg_a == 0:
            return
        self.instruction_pointer = operand
    
    def _bxc(self, _: int) -> None:
        c = self.reg_c
        b = self.reg_b
        self.reg_b = c ^ b

    def _out(self, operand: int) -> None:
        combo_operand = self._get_combo_operand(operand)
        # print('out', combo_operand, combo_operand % 8, operand)
        self.output.append(combo_operand % 8)

    def _bdv(self, operand: int) -> None:
        self.reg_b = self._div(operand)

    def _cdv(self, operand: int) -> None:
        self.reg_c = self._div(operand)


    def advance(self) -> str | None:
        # print('advancing, instruction pointer:', self.instruction_pointer)
        if self.instruction_pointer >= len(self.instructions):
            return 'Done'
        op_code = self._get_opcode()
        operand = self._get_operand()
        # print('got opcode:', op_code, 'and operand:', operand, 'instruction pointer:', self.instruction_pointer)
        if op_code == 0:
            if self.debug: print('adv', 'pointer:', self.instruction_pointer)
            self._adv(operand)
        elif op_code == 1:
            if self.debug: print('bxl', 'pointer:', self.instruction_pointer)
            self._bxl(operand)
        elif op_code == 2:
            if self.debug: print('bst', 'pointer:', self.instruction_pointer)
            self._bst(operand)
        elif op_code == 3:
            if self.debug: print('jnz', 'pointer:', self.instruction_pointer)
            self._jnz(operand)
        elif op_code == 4:
            if self.debug: print('bxc', 'pointer:', self.instruction_pointer)
            self._bxc(operand)
        elif op_code == 5:
            if self.debug: print('out', 'pointer:', self.instruction_pointer)
            self._out(operand)
        elif op_code == 6:
            if self.debug: print('bdv', 'pointer:', self.instruction_pointer)
            self._bdv(operand)
        elif op_code == 7:
            if self.debug: print('cdv', 'pointer:', self.instruction_pointer)
            self._cdv(operand)
        else:
            raise ValueError('Invalid opcode', 'pointer:', self.instruction_pointer)
    def get_output(self) -> str:
        return ','.join(str(x) for x in self.output)

def build_machine(path: str) -> Machine:
    with open(path, 'r') as file:
        reg_a = file.readline().strip().split(': ')[1]
        reg_b = file.readline().strip().split(': ')[1]
        reg_c = file.readline().strip().split(': ')[1]
        file.readline()
        instructions = file.readline().strip('\n').split(': ')[1]
        return Machine(int(reg_a), int(reg_b), int(reg_c), [int(x) for x in instructions.split(',')], False)

def process_part_1(path: str) -> Machine:
    machine = build_machine(path)
    machine.reg_a = 127
    result = None
    while result != 'Done':
        result = machine.advance()
    print('output:', machine.get_output())
    return machine

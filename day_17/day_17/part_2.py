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
        if self.debug: print('Machine initialized with registers:', self.reg_a, self.reg_b, self.reg_c, 'and instructions:', self.instructions)

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
        if self.debug: print('adv', numerator, denominator, numerator // (2 ** denominator))
        # print('adv', numerator, denominator, numerator // (2 ** denominator))
        return numerator // (2 ** denominator)

    def _adv(self, operand: int) -> None:
        if self.debug: print('advancing with operand:', operand)
        self.reg_a = self._div(operand)

    def _bxl(self, operand: int) -> None:
        if self.debug: print('bxl with operand:', operand, self.reg_b^operand)
        b = self.reg_b
        self.reg_b = b ^ operand

    def _bst(self, operand: int) -> None:
        if self.debug: print('bst with operand:', operand, self._get_combo_operand(operand) % 8)
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
        self.output.append(combo_operand % 8)

    def _bdv(self, operand: int) -> None:
        self.reg_b = self._div(operand)

    def _cdv(self, operand: int) -> None:
        self.reg_c = self._div(operand)


    def advance(self) -> str | None:
        if self.debug: print('advancing, instruction pointer:', self.instruction_pointer)
        if self.instruction_pointer >= len(self.instructions):
            return 'Done'
        op_code = self._get_opcode()
        operand = self._get_operand()
        if self.debug: print('got opcode:', op_code, 'and operand:', operand)
        if op_code == 0:
            self._adv(operand)
        elif op_code == 1:
            self._bxl(operand)
        elif op_code == 2:
            self._bst(operand)
        elif op_code == 3:
            self._jnz(operand)
        elif op_code == 4:
            self._bxc(operand)
        elif op_code == 5:
            self._out(operand)
        elif op_code == 6:
            self._bdv(operand)
        elif op_code == 7:
            self._cdv(operand)
        else:
            raise ValueError('Invalid opcode')

    def get_output(self) -> str:
        return ','.join(str(x) for x in self.output)

def process_input(path: str) -> Machine:
    with open(path, 'r') as file:
        reg_a = file.readline().strip().split(': ')[1]
        reg_b = file.readline().strip().split(': ')[1]
        reg_c = file.readline().strip().split(': ')[1]
        file.readline()
        instructions = file.readline().strip('\n').split(': ')[1]
        return Machine(int(reg_a), int(reg_b), int(reg_c), [int(x) for x in instructions.split(',')], True)

def process_part_2(path: str) -> int:
    machine = process_input(path)
    output = []
    count = 100000000
    og = 100000000
    mult = 512
    while count < og + (100 * mult ):
        result = None
        print('count', count)
        new_machine = Machine(count, machine.reg_b, machine.reg_c, machine.instructions)
        while result != 'Done':
            result = new_machine.advance()
        output = new_machine.get_output()
        print('output:', output)
        count += mult
    return count

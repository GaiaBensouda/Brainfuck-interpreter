import sys

class WhitespaceInterpreter:
    def __init__(self, code):
        self.code = code
        self.commands = {
            '  ': self.push,
            ' \t ': self.duplicate,
            ' \n ': self.swap,
            ' \t\n': self.discard,
            '\t   ': self.add,
            '\t  \t': self.subtract,
            '\t  \n': self.multiply,
            '\t \t ': self.divide,
            '\t \t\t': self.modulo,
            '\t\t ': self.store,
            '\t\t\t': self.retrieve,
            '\n  ': self.mark,
            '\n \t': self.call,
            '\n \n': self.jump,
            '\n\t ': self.jump_if_zero,
            '\n\t\t': self.jump_if_negative,
            '\n\t\n': self.end_subroutine,
            '\n\n\n': self.end_program,
            '\t\n  ': self.output_char,
            '\t\n \t': self.output_num,
            '\t\n\t ': self.read_char,
            '\t\n\t\t': self.read_num,
        }
        self.stack = []
        self.heap = {}
        self.labels = {}
        self.call_stack = []
        self.position = 0
        self.parse_labels()

    def parse_labels(self):
        position = 0
        while position < len(self.code):
            instruction = self.next_instruction(position)
            if instruction.startswith('\n  '):  # Label mark
                label = self.read_label(position + 3)
                self.labels[label] = position + len(instruction)
            position += len(instruction)

    def next_instruction(self, position):
        instruction = self.code[position:position + 2]
        if instruction in ['  ', ' \t', ' \n', '\t ', '\t\t', '\t\n', '\n ']:
            instruction += self.code[position + 2]
        return instruction

    def read_label(self, position):
        label = ''
        while self.code[position] != '\n':
            label += self.code[position]
            position += 1
        return label

    def read_number(self):
        sign = 1 if self.code[self.position] == ' ' else -1
        self.position += 1
        number = 0
        while self.code[self.position] != '\n':
            number = number * 2 + (1 if self.code[self.position] == '\t' else 0)
            self.position += 1
        self.position += 1
        return sign * number

    def push(self):
        number = self.read_number()
        self.stack.append(number)

    def duplicate(self):
        self.stack.append(self.stack[-1])

    def swap(self):
        self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

    def discard(self):
        self.stack.pop()

    def add(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    def subtract(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a - b)

    def multiply(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a * b)

    def divide(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a // b)

    def modulo(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a % b)

    def store(self):
        value = self.stack.pop()
        address = self.stack.pop()
        self.heap[address] = value

    def retrieve(self):
        address = self.stack.pop()
        self.stack.append(self.heap.get(address, 0))

    def mark(self):
        pass

    def call(self):
        label = self.read_label(self.position)
        self.call_stack.append(self.position + len(label) + 1)
        self.position = self.labels[label]

    def jump(self):
        label = self.read_label(self.position)
        self.position = self.labels[label]

    def jump_if_zero(self):
        label = self.read_label(self.position)
        if self.stack.pop() == 0:
            self.position = self.labels[label]

    def jump_if_negative(self):
        label = self.read_label(self.position)
        if self.stack.pop() < 0:
            self.position = self.labels[label]

    def end_subroutine(self):
        self.position = self.call_stack.pop()

    def end_program(self):
        sys.exit()

    def output_char(self):
        char = chr(self.stack.pop())
        print(char, end='')

    def output_num(self):
        num = self.stack.pop()
        print(num, end='')

    def read_char(self):
        address = self.stack.pop()
        self.heap[address] = ord(sys.stdin.read(1))

    def read_num(self):
        address = self.stack.pop()
        num = int(sys.stdin.read(1))
        self.heap[address] = num

    def run(self):
        while self.position < len(self.code):
            instruction = self.next_instruction(self.position)
            self.position += len(instruction)
            if instruction in self.commands:
                self.commands[instruction]()
            else:
                raise Exception(f"Unknown instruction: {instruction}")

#example
program = "   \t\n\t\n \t\t\n\n\n"
interpreter = WhitespaceInterpreter(program)
interpreter.run()

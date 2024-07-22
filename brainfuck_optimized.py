class BrainfuckInterpreter:
    def __init__(self, code, input_str="", tape_size=30000):
        self.code = ''.join(filter(lambda x: x in ['>', '<', '+', '-', '.', ',', '[', ']'], code))
        self.tape = [0] * tape_size
        self.pointer = 0
        self.input_str = input_str
        self.input_pointer = 0
        self.output = []
        self.stack = []
        self.pc = 0  
        self.bracket_map = self.build_bracket_map()

    def build_bracket_map(self):
        temp_stack = []
        bracket_map = {}

        for pos, char in enumerate(self.code):
            if char == '[':
                temp_stack.append(pos)
            elif char == ']':
                start = temp_stack.pop()
                bracket_map[start] = pos
                bracket_map[pos] = start

        if temp_stack:
            raise ValueError("Unmatched '[' found at positions: " + str(temp_stack))
        
        return bracket_map

    def run(self, debug=False):
        while self.pc < len(self.code):
            command = self.code[self.pc]

            if command == '>':
                self.pointer += 1
                if self.pointer >= len(self.tape):
                    self.tape.append(0)
            elif command == '<':
                self.pointer -= 1
                if self.pointer < 0:
                    self.tape.insert(0, 0)
                    self.pointer = 0
            elif command == '+':
                self.tape[self.pointer] = (self.tape[self.pointer] + 1) % 256
            elif command == '-':
                self.tape[self.pointer] = (self.tape[self.pointer] - 1) % 256
            elif command == '.':
                self.output.append(chr(self.tape[self.pointer]))
            elif command == ',':
                if self.input_pointer < len(self.input_str):
                    self.tape[self.pointer] = ord(self.input_str[self.input_pointer])
                    self.input_pointer += 1
                else:
                    self.tape[self.pointer] = 0  
            elif command == '[':
                if self.tape[self.pointer] == 0:
                    self.pc = self.bracket_map[self.pc]
            elif command == ']':
                if self.tape[self.pointer] != 0:
                    self.pc = self.bracket_map[self.pc]

            if debug:
                self.print_debug_info(command)

            self.pc += 1

        return ''.join(self.output)

    def print_debug_info(self, command):
        print(f"Command: {command}, PC: {self.pc}, Pointer: {self.pointer}, Tape: {self.tape[:10]}")

    def clear(self):
        self.tape = [0] * len(self.tape)
        self.pointer = 0
        self.pc = 0
        self.output = []
        self.input_pointer = 0


bf_code = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
interpreter = BrainfuckInterpreter(bf_code)
print(interpreter.run())



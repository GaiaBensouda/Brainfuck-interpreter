def brainfuck_to_python(code, input_str=""):
    def clear_cell():
        tape[pointer] = 0

    def multiply_loop():
        if tape[pointer] == 0:
            return
        temp_pointer = pointer
        offsets = {}
        while code[pc] != ']':
            if code[pc] == '>':
                temp_pointer += 1
            elif code[pc] == '<':
                temp_pointer -= 1
            elif code[pc] == '+':
                if temp_pointer in offsets:
                    offsets[temp_pointer] += 1
                else:
                    offsets[temp_pointer] = 1
            elif code[pc] == '-':
                if temp_pointer in offsets:
                    offsets[temp_pointer] -= 1
                else:
                    offsets[temp_pointer] = -1
            pc += 1
        for offset, value in offsets.items():
            tape[offset] += tape[pointer] * value
        tape[pointer] = 0

    code = ''.join(filter(lambda x: x in ['>', '<', '+', '-', '.', ',', '[', ']'], code))
    tape = [0] * 30000
    pointer = 0
    input_pointer = 0
    output = []
    stack = []
    pc = 0  

    while pc < len(code):
        command = code[pc]

        if command == '>':
            pointer += 1
            if pointer >= len(tape):
                tape.append(0)
        elif command == '<':
            pointer -= 1
            if pointer < 0:
                tape.insert(0, 0)
                pointer = 0
        elif command == '+':
            tape[pointer] = (tape[pointer] + 1) % 256
        elif command == '-':
            tape[pointer] = (tape[pointer] - 1) % 256
        elif command == '.':
            output.append(chr(tape[pointer]))
        elif command == ',':
            if input_pointer < len(input_str):
                tape[pointer] = ord(input_str[input_pointer])
                input_pointer += 1
            else:
                tape[pointer] = 0  
        elif command == '[':
            if tape[pointer] == 0:
                open_brackets = 1
                while open_brackets:
                    pc += 1
                    if code[pc] == '[':
                        open_brackets += 1
                    elif code[pc] == ']':
                        open_brackets -= 1
            else:
                stack.append(pc)
        elif command == ']':
            if tape[pointer] != 0:
                if code[stack[-1]:pc + 1] in ['[-]', '[+]']:
                    clear_cell()
                    pc = stack.pop()  
                elif code[stack[-1]:pc + 1].count('>') > 1 and code[stack[-1]:pc + 1].count('<') > 1:
                    multiply_loop()
                    stack.pop()
                else:
                    pc = stack[-1]
            else:
                stack.pop()
        
        pc += 1

    return ''.join(output)

#example "Hello world"
bf_code = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
print(brainfuck_to_python(bf_code))

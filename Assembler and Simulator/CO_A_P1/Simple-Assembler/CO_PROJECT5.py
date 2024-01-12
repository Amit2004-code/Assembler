opcodes = {
    'add': '00000',
    'sub': '00001',
    'mov_imm': '00010',
    'mov_reg': '00011',
    'ld': '00100',
    'st': '00101',
    'mul': '00110',
    'div': '00111',
    'rs': '01000',
    'ls': '01001',
    'xor': '01010',
    'or': '01011',
    'and': '01100',
    'not': '01101',
    'cmp': '01110',
    'jmp': '01111',
    'jlt': '11100',
    'jgt': '11101',
    'je': '11111',
    'hlt': '11010'
}

registers = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111'
}

types = {
    'A': ['add', 'sub', 'mul','xor','or'],
    'B': ['rs', 'ls'],
    'C': ['mov_imm', 'mov_reg', 'div', 'not', 'cmp'],
    'D': ['ld', 'st'],
    'E': ['jmp', 'jlt', 'jgt', 'je'],
    'F': ['hlt']
}

def assembler(code):
    lines = code.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    variables = {}
    variable_addr = 0

    labels = {}
    instruction_index = 0

    for line in lines:
        tokens = line.split()
        instruction = tokens[0]

        if instruction.endswith(':'):
            label = instruction[:-1]
            labels[label] = instruction_index
            continue

        if instruction == 'var':
            var_name = tokens[1]
            variables[var_name] = variable_addr
            variable_addr += 1
            continue

        instruction_index += 1

    output = ''
    for line in lines:
        tokens = line.split()
        instruction = tokens[0]

        if instruction.endswith(':'):
            continue

        if instruction == 'var':
            continue

        for t, i_list in types.items():
            if instruction in i_list:
                instr_type = t
                break

        opcode = opcodes[instruction]

        if instr_type == 'A':
            reg1 = registers[tokens[1]]
            reg2 = registers[tokens[2]]
            reg3 = registers[tokens[3]]
            output += opcode + '00' + reg1 + reg2 + reg3 + '\n'
        elif instr_type == 'B':
            reg1 = registers[tokens[1]]
            imm = format(int(tokens[2]), '07b')
            output += opcode + '0' + reg1 + imm + '\n'
        elif instr_type == 'C':
            reg1 = registers[tokens[1]]
            if tokens[2] in registers:
                reg2 = registers[tokens[2]]
                output += opcode +'00000'+ reg1 + reg2 + '\n'
            else:
                imm = format(int(tokens[2]), '07b')
                output += opcode + '0' + reg1  + imm + '\n'
        elif instr_type == 'D':
            reg1 = registers[tokens[1]]
            if tokens[2] in variables:
                addr = format(variables[tokens[2]], '09b')
            else:
                addr = format(labels[tokens[2]], '09b')
            output += opcode + '0' + reg1 + addr + '\n'
        elif instr_type == 'E':
            if tokens[1] in labels:
                addr = format(labels[tokens[1]], '09b')
            else:
                addr = format(int(tokens[1]), '09b')
            output += opcode + '00' + addr + '\n'
        elif instr_type == 'F':
            output += opcode + '00000000000' + '\n'

    return output


code = ''
while True:
    line = input("Enter an instruction ('hlt' to stop): ")
    code += line + '\n'
    if line.strip() == 'hlt':
        break

machine_code = assembler(code)
print(machine_code)
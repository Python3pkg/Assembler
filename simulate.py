reg = {'PC': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
stack = []
callstack = []
done = False
memory = {}
lenoptable = {}
instruction = {}

def findoptable():
	with open("bin/a_l_l/opcodes.cf", "r") as file:
		opcodes = file.read().split("\n")
		file.close()
	for opcode in opcodes:
		opcode = opcode.lstrip().rstrip()
		if opcode != '':
			lenoptable[opcode.split()[0]] = int(opcode.split()[1])

def initiate(lines, offset):
	memadd = offset
	reg['PC'] = offset
	for line in lines:
		opcode = line.split(' ')[0]
		if opcode == 'DB':
			memory[memadd] = int(line.split(' ')[1])
			memadd = memadd + 1
		else:
			instruction[memadd] = line
			memadd = memadd + lenoptable[opcode]

def process(instr):
	global stack
	global callstack
	opcode = instr.split(' ')[0]
	if opcode == 'JMP':
		reg['PC'] = int(instr.split(' ')[1])
	elif opcode == 'LDA':
		reg['A'] = memory[int(instr.split(' ')[1])]
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'STA':
		memory[int(instr.split(' ')[1])] = reg['A']
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'MVI':
		ops = instr.split(' ')[1]
		reg[ops.split(',')[0]] = int(ops.split(',')[1])
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'ADI':
		reg['A'] = reg['A'] + int(instr.split(' ')[1])
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'MOV':
		vari = instr.split(' ')[1]
		var1, var2 = vari.split(',')
		reg[var1] = reg[var2]
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'ADD':
		reg['A'] = reg['A'] + reg[instr.split(' ')[1]]
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'SUI':
		reg['A'] = reg['A'] - int(instr.split(' ')[1])
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'SUB':
		reg['A'] = reg['A'] - reg[(instr.split(' ')[1])]
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'ANI':
		reg['A'] = reg['A'] & int(instr.split(' ')[1])
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'ANA':
		reg['A'] = reg['A'] & reg[instr.split(' ')[1]]
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'ORI':
		reg['A'] = reg['A'] | int(instr.split(' ')[1])
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'ORA':
		reg['A'] = reg['A'] | reg[instr.split(' ')[1]]
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'PUSH':
		stack.append(reg[instr.split(' ')[1]])
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'JNZ':
		if reg['A'] != 0:
			reg['PC'] = int(instr.split(' ')[1])
		else:
			reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'POP':
		reg[instr.split(' ')[1]] = stack[len(stack) - 1]
		stack = stack[:len(stack) - 1]
		reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'JP':
		if reg['A'] > 0:
			reg['PC'] = int(instr.split(' ')[1])
		else:
			reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'JZ':
		if reg['A'] == 0:
			reg['PC'] = int(instr.split(' ')[1])
		else:
			reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'JM':
		if reg['A'] < 0:
			reg['PC'] = int(instr.split(' ')[1])
		else:
			reg['PC'] = reg['PC'] + lenoptable[opcode]
	elif opcode == 'CALL':
		callstack.append(reg['PC'] + lenoptable[opcode])
		reg['PC'] = int(instr.split(' ')[1])
	elif opcode == 'RET':
		reg['PC'] = callstack[len(callstack) - 1]
		callstack = callstack[:len(callstack) - 1]
	elif opcode == 'HLT':
		global done
		done = True

def simulate(filename, offset):
	global reg
	global stack
	global callstack
	global done
	global memory
	global lenoptable
	global instruction
	reg = {'PC': 0, 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
	stack = []
	callstack = []
	done = False
	memory = {}
	lenoptable = {}
	instruction = {}
	findoptable()
	with open(filename.split('.')[0] + '.final', 'r') as file:
		lines = file.read().split('\n')
		file.close()
	initiate(lines, offset)
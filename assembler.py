import re

optable = {}
symtable = {}
globtable = {}
filelentable = {}
error = "False"

def findoptable():
	with open("bin/a_l_l/opcodes.cf", "r") as file:
		opcodes = file.read().split("\n")
		file.close()
	for opcode in opcodes:
		opcode = opcode.lstrip().rstrip()
		if opcode != '':
			optable[opcode.split()[0]] = int(opcode.split()[1])

def isint(string):
	try:
		int(string)
		return True
	except:
		return False

def convert(fileNames):
	global error
	global optable
	global symtable
	global globtable
	global filelentable
	optable = {}
	symtable = {}
	globtable = {}
	filelentable = {}
	error = "False"
	findoptable()
	revar = re.compile("var\s+(\w+)\s*=\s*(\w+)\s*")
	reglo = re.compile("global\s+var\s+(\w+)\s*=\s*(\w+)\s*")
	reext = re.compile("extern\s+var\s+(\w+)\s*")
	replus = re.compile("\s*(\w+)\s*=\s*(\w+)\s*\+\s*(\w+)\s*")
	reminus = re.compile("\s*(\w+)\s*=\s*(\w+)\s*-\s*(\w+)\s*")
	remul = re.compile("\s*(\w+)\s*=\s*(\w+)\s*\*\s*(\w+)\s*")
	rediv = re.compile("\s*(\w+)\s*=\s*(\w+)\s*\/\s*(\w+)\s*")
	reand = re.compile("\s*(\w+)\s*=\s*(\w+)\s*&\s*(\w+)\s*")
	reor = re.compile("\s*(\w+)\s*=\s*(\w+)\s*\|\s*(\w+)\s*")
	reloop = re.compile("\s*loop\s+(\w+)\s*")
	reendloop = re.compile("\s*endloop\s*")
	refunction = re.compile("\s*function\s+(\w+)\s*")
	reassarr = re.compile("\s*(\w+)\[(\w+)\]\s*=\s*(\w+)\s*")
	renfun = re.compile("\s*endfunction\s*")
	rearray = re.compile("\s*var\s+(\w+)\[(\w+)\]\s*")
	recall = re.compile("\s*(\w+)\(\)")
	reextf = re.compile("\s*extern\s+function\s+(\w+)\(\)\s*")
	reifgt = re.compile("\s*if\s+(\w+)\s*>\s*(\w+)\s*")
	reifeq = re.compile("\s*if\s+(\w+)\s*=\s*(\w+)\s*")
	reiflt = re.compile("\s*if\s+(\w+)\s*<\s*(\w+)\s*")
	reendif = re.compile("\s*endif\s*")
	remin = re.compile("\s*(\w+)\s*=\s*min\s*\((.*)\)\s*")
	remax = re.compile("\s*(\w+)\s*=\s*max\s*\((.*)\)\s*")
	rejump = re.compile("\s*JUMP\s+(\w+)\s*")
	retag = re.compile("\s*(\w+)[:]\s*")

	for filenam in fileNames:
		with open(filenam, 'r') as file:
			code = file.read()
			lines = code.split('\n')
			file.close()

		filename = filenam.split('.')[0]

		memadd = 0
		loops = 0
		ifs = 0
		asscode = []
		iftable = {}
		fcalls = {}
		fnc = 0
		symtable[filename] = {}
		globtable[filename] = {}

		for line in lines:
			line = line.lstrip().rstrip()

			if reglo.match(line):
				var1 = reglo.match(line).group(1)
				var2 = reglo.match(line).group(2)
				if (not isint(var2) and var2 not in symtable[filename]) or isint(var1):
					error = "Variable " + var2 + " not declared" + "in" + line
					return
				if isint(var1):
					error = "Expected variable" + "in" + line
				if isint(var2):
					asscode.append("JMP #" + str(memadd + 4))
					asscode.append("DB " + str(var2))
					symtable[filename][var1] = "#" + str(memadd + 3)
					globtable[filename][var1] = "#" + str(memadd + 3)
					memadd = memadd + optable["JMP"] + 1
				else:
					asscode.append("JMP #" + str(memadd + 4))
					symtable[filename][var1] = "#" + str(memadd + 3)
					globtable[filename][var1] = "#" + str(memadd + 3)
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["JMP"] + optable["LDA"] + optable["STA"] + 1
			elif revar.match(line):
				var1 = revar.match(line).group(1)
				var2 = revar.match(line).group(2)
				if (not isint(var2) and var2 not in symtable[filename]) or isint(var1):
					error = "Variable " + var2 + " not declared" + "in" + line
					return
				if isint(var1):
					error = "Expected variable" + "in" + line
				if isint(var2):
					asscode.append("JMP #" + str(memadd + 4))
					asscode.append("DB " + str(var2))
					symtable[filename][var1] = "#" + str(memadd + 3)
					memadd = memadd + optable["JMP"] + 1
				else:
					asscode.append("JMP #" + str(memadd + 4))
					symtable[filename][var1] = "#" + str(memadd + 3)
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["JMP"] + optable["LDA"] + optable["STA"] + 1
			elif rearray.match(line):
				var = rearray.match(line).group(1)
				lent = rearray.match(line).group(2)
				if not isint(lent) or isint(var):
					error = "Invalid line: " + line
					return
				symtable[filename][var] = "#" + str(memadd + 3)
				asscode.append("JMP #" + str(memadd + 3 + int(lent)))
				for i in range(int(lent)):
					asscode.append("DB 0")
				memadd = memadd + 3 + int(lent)
			elif reext.match(line):
				var = reext.match(line).group(1)
				if isint(var):
					error = "Expected variable in " + line
					return
				symtable[filename][var] = "$" + str(var)
			elif reextf.match(line):
				fname = reextf.match(line).group(1)
				symtable[filename][fname] = "$"+str(fname)
			elif replus.match(line):
				var1 = replus.match(line).group(1)
				var2 = replus.match(line).group(2)
				var3 = replus.match(line).group(3)
				if isint(var1) or var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				if isint(var2) and isint(var3):
					asscode.append("MVI A," + str(var2))
					asscode.append("ADI " + str(var3))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["MVI"] + optable["ADI"] + optable["STA"]
				elif isint(var2):
					if var3 not in symtable[filename]:
						error = "Variable " + var3 + " not declared in " + line
						return
					asscode.append("LDA " + str(symtable[filename][var3]))
					asscode.append("ADI " + str(var2))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ADI"] + optable["STA"]
				elif isint(var3):
					if var2 not in symtable[filename]:
						error = "Variable " + var2 + " not declared in" + line
						return
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("ADI " + str(var3))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ADI"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						error = "Variable not declared in " + line
						return
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("MOV B,A")
					asscode.append("LDA " + str(symtable[filename][var3]))
					asscode.append("ADD B")
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["ADD"] + optable["STA"]
			elif reminus.match(line):
				var1 = reminus.match(line).group(1)
				var2 = reminus.match(line).group(2)
				var3 = reminus.match(line).group(3)
				if isint(var1) or var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				if isint(var2) and isint(var3):
					asscode.append("MVI A," + str(var2))
					asscode.append("SUI " + str(var3))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["MVI"] + optable["SUI"] + optable["STA"]
				elif isint(var2):
					if var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var3]))
					asscode.append("MOV B,A")
					asscode.append("MVI A," + str(var2))
					asscode.append("SUB B")
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["MVI"] + optable["SUB"] + optable["STA"]
				elif isint(var3):
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("SUI " + str(var3))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var3]))
					asscode.append("MOV B,A")
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("SUB B")
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["STA"]
			elif remul.match(line):
				var1 = remul.match(line).group(1)
				var2 = remul.match(line).group(2)
				var3 = remul.match(line).group(3)
				if isint(var1) or var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				if isint(var2) and isint(var3):
					asscode.append("MVI B,0")
					asscode.append("MVI A," + str(var3))
					memadd = memadd + optable["MVI"] + optable["MVI"]
					asscode.append("JZ #" + str(memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"]))
					asscode.append("MOV C,A")
					asscode.append("MVI A," + str(var2))
					asscode.append("ADD B")
					asscode.append("MOV B,A")
					asscode.append("MOV A,C")
					asscode.append("SUI 1")
					asscode.append("JMP #" + str(memadd))
					asscode.append("MOV A,B")
					asscode.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				elif isint(var2):
					if var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("MVI B,0")
					asscode.append("LDA " + symtable[filename][var3])
					memadd = memadd + optable["MVI"] + optable["LDA"]
					asscode.append("JZ #" + str(memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"]))
					asscode.append("MOV C,A")
					asscode.append("MVI A," + str(var2))
					asscode.append("ADD B")
					asscode.append("MOV B,A")
					asscode.append("MOV A,C")
					asscode.append("SUI 1")
					asscode.append("JMP #" + str(memadd))
					asscode.append("MOV A,B")
					asscode.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				elif isint(var3):
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("MVI B,0")
					asscode.append("LDA " + symtable[filename][var2])
					memadd = memadd + optable["MVI"] + optable["LDA"]
					asscode.append("JZ #" + str(memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"]))
					asscode.append("MOV C,A")
					asscode.append("MVI A," + str(var3))
					asscode.append("ADD B")
					asscode.append("MOV B,A")
					asscode.append("MOV A,C")
					asscode.append("SUI 1")
					asscode.append("JMP #" + str(memadd))
					asscode.append("MOV A,B")
					asscode.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JZ"] + optable["MOV"] + optable["MVI"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("MVI B,0")
					asscode.append("LDA " + symtable[filename][var2])
					memadd = memadd + optable["MVI"] + optable["LDA"]
					asscode.append("JZ #" + str(memadd + optable["JZ"] + optable["MOV"] + optable["LDA"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"]))
					asscode.append("MOV C,A")
					asscode.append("LDA " + symtable[filename][var3])
					asscode.append("ADD B")
					asscode.append("MOV B,A")
					asscode.append("MOV A,C")
					asscode.append("SUI 1")
					asscode.append("JMP #" + str(memadd))
					asscode.append("MOV A,B")
					asscode.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JZ"] + optable["MOV"] + optable["LDA"] + optable["ADD"] + optable["MOV"] + optable["MOV"] + optable["SUI"] + optable["JMP"] + optable["MOV"] + optable["STA"]
			elif rediv.match(line):
				var1 = rediv.match(line).group(1)
				var2 = rediv.match(line).group(2)
				var3 = rediv.match(line).group(3)
				if isint(var1) or var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				if isint(var2) and isint(var3):
					asscode.append("MVI B," + str(var3))
					asscode.append("MVI A," + str(var2))
					asscode.append("SUB B")
					asscode.append("MVI C,0")
					memadd = memadd + optable["MVI"] + optable["MVI"] + optable["SUB"] + optable["MVI"]
					asscode.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"]))
					asscode.append("MOV F,A")
					asscode.append("MOV A,C")
					asscode.append("ADI 1")
					asscode.append("MOV C,A")
					asscode.append("MOV A,F")
					asscode.append("SUB B")
					asscode.append("JMP #" + str(memadd))
					asscode.append("MOV A,C")
					asscode.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				elif isint(var2):
					if var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var3])
					asscode.append("MOV B,A")
					asscode.append("MVI A," + str(var2))
					asscode.append("SUB B")
					asscode.append("MVI C,0")
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["MVI"] + optable["SUB"] + optable["MVI"]
					asscode.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"]))
					asscode.append("MOV F,A")
					asscode.append("MOV A,C")
					asscode.append("ADI 1")
					asscode.append("MOV C,A")
					asscode.append("MOV A,F")
					asscode.append("SUB B")
					asscode.append("JMP #" + str(memadd))
					asscode.append("MOV A,C")
					asscode.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				elif isint(var3):
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("MVI B," + str(var3))
					asscode.append("LDA " + symtable[filename][var2])
					asscode.append("SUB B")
					asscode.append("MVI C,0")
					memadd = memadd + optable["MVI"] + optable["LDA"] + optable["SUB"] + optable["MVI"]
					asscode.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"]))
					asscode.append("MOV F,A")
					asscode.append("MOV A,C")
					asscode.append("ADI 1")
					asscode.append("MOV C,A")
					asscode.append("MOV A,F")
					asscode.append("SUB B")
					asscode.append("JMP #" + str(memadd))
					asscode.append("MOV A,C")
					asscode.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"] + optable["MOV"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var3])
					asscode.append("MOV B,A")
					asscode.append("LDA " + symtable[filename][var2])
					asscode.append("SUB B")
					asscode.append("MVI C,0")
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["MVI"]
					asscode.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"]))
					asscode.append("MOV F,A")
					asscode.append("MOV A,C")
					asscode.append("ADI 1")
					asscode.append("MOV C,A")
					asscode.append("MOV A,F")
					asscode.append("SUB B")
					asscode.append("JMP #" + str(memadd))
					asscode.append("MOV A,C")
					asscode.append("STA " + symtable[filename][var1])
					memadd = memadd + optable["JM"] + optable["MOV"] + optable["MOV"] + optable["ADI"] + optable["MOV"] + optable["MOV"] + optable["SUB"] + optable["JMP"] + optable["MOV"] + optable["STA"]
			elif remin.match(line):
				var1 = remin.match(line).group(1)
				vas = remin.match(line).group(2)
				if isint(var1) or var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				vas = vas.split(',')
				for i in range(len(vas)):
					vas[i] = vas[i].lstrip().rstrip()
				if isint(vas[0]):
					asscode.append("MVI A," + str(vas[0]))
					memadd = memadd + optable["MVI"]
				elif vas[0] not in symtable[filename]:
					error = "Invalid line: " + line
				else:
					asscode.append("LDA " + symtable[filename][vas[0]])
					memadd = memadd + optable["LDA"]
				vas = vas[1:]
				for var in vas:
					if isint(var):
						asscode.append("MVI B," + str(var))
						asscode.append("MOV C,A")
						asscode.append("SUB B")
						memadd = memadd + optable["MVI"] + optable["MOV"] + optable["SUB"]
						asscode.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["JP"]))
						asscode.append("MOV G,B")
						asscode.append("JP #" + str(memadd + optable["JM"] + optable["MOV"] + optable["JP"] + optable["MOV"]))
						asscode.append("MOV G,C")
						asscode.append("MOV A,G")
						memadd = memadd + optable["JM"] + optable["MOV"] + optable["JP"] + optable["MOV"] + optable["MOV"]
					elif var not in symtable[filename]:
						error = "Invalid line: " + line
						return
					else:
						asscode.append("MOV C,A")
						asscode.append("LDA " + symtable[filename][var])
						asscode.append("MOV B,A")
						asscode.append("MOV A,C")
						asscode.append("SUB B")
						memadd = memadd + optable["MOV"] + optable["LDA"] + optable["MOV"] + optable["MOV"] + optable["SUB"]
						asscode.append("JM #" + str(memadd + optable["JM"] + optable["MOV"] + optable["JP"]))
						asscode.append("MOV G,B")
						asscode.append("JP #" + str(memadd + optable["JM"] + optable["MOV"] + optable["JP"] + optable["MOV"]))
						asscode.append("MOV G,C")
						asscode.append("MOV A,G")
						memadd = memadd + optable["JM"] + optable["MOV"] + optable["JP"] + optable["MOV"] + optable["MOV"]
				asscode.append("STA " + symtable[filename][var1])
				memadd = memadd + optable["STA"]
			elif remax.match(line):
				var1 = remax.match(line).group(1)
				vas = remax.match(line).group(2)
				if isint(var1) or var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				vas = vas.split(',')
				for i in range(len(vas)):
					vas[i] = vas[i].lstrip().rstrip()
				if isint(vas[0]):
					asscode.append("MVI A," + str(vas[0]))
					memadd = memadd + optable["MVI"]
				elif vas[0] not in symtable[filename]:
					error = "Invalid line: " + line
				else:
					asscode.append("LDA " + symtable[filename][vas[0]])
					memadd = memadd + optable["LDA"]
				vas = vas[1:]
				for var in vas:
					if isint(var):
						asscode.append("MVI B," + str(var))
						asscode.append("MOV C,A")
						asscode.append("SUB B")
						memadd = memadd + optable["MVI"] + optable["MOV"] + optable["SUB"]
						asscode.append("JP #" + str(memadd + optable["JP"] + optable["MOV"] + optable["JM"]))
						asscode.append("MOV G,B")
						asscode.append("JM #" + str(memadd + optable["JP"] + optable["MOV"] + optable["JM"] + optable["MOV"]))
						asscode.append("MOV G,C")
						asscode.append("MOV A,G")
						memadd = memadd + optable["JP"] + optable["MOV"] + optable["JM"] + optable["MOV"] + optable["MOV"]
					elif var not in symtable[filename]:
						error = "Invalid line: " + line
						return
					else:
						asscode.append("MOV C,A")
						asscode.append("LDA " + symtable[filename][var])
						asscode.append("MOV B,A")
						asscode.append("MOV A,C")
						asscode.append("SUB B")
						memadd = memadd + optable["MOV"] + optable["LDA"] + optable["MOV"] + optable["MOV"] + optable["SUB"]
						asscode.append("JP #" + str(memadd + optable["JP"] + optable["MOV"] + optable["JM"]))
						asscode.append("MOV G,B")
						asscode.append("JM #" + str(memadd + optable["JP"] + optable["MOV"] + optable["JM"] + optable["MOV"]))
						asscode.append("MOV G,C")
						asscode.append("MOV A,G")
						memadd = memadd + optable["JP"] + optable["MOV"] + optable["JM"] + optable["MOV"] + optable["MOV"]
				asscode.append("STA " + symtable[filename][var1])
				memadd = memadd + optable["STA"]
			elif rejump.match(line):
				loc = rejump.match(line).group(1)
				asscode.append("JMP ~~~" + str(loc))
				memadd = memadd + optable["JMP"]
			elif retag.match(line):
				loc = retag.match(line).group(1)
				symtable[filename][loc] = "#" + str(memadd)
			elif reand.match(line):
				var1 = reand.match(line).group(1)
				var2 = reand.match(line).group(2)
				var3 = reand.match(line).group(3)
				if isint(var1) or var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				if isint(var2) and isint(var3):
					asscode.append("MVI A," + str(var2))
					asscode.append("ANI " + str(var3))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["MVI"] + optable["ANI"] + optable["STA"]
				elif isint(var2):
					if var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var3]))
					asscode.append("ANI " + str(var2))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ANI"] + optable["STA"]
				elif isint(var3):
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("ANI " + str(var3))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ANI"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("MOV B,A")
					asscode.append("LDA " + str(symtable[filename][var3]))
					asscode.append("ANA B")
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["ANA"] + optable["STA"]
			elif reor.match(line):
				var1 = reor.match(line).group(1)
				var2 = reor.match(line).group(2)
				var3 = reor.match(line).group(3)
				if isint(var1) or var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				if isint(var2) and isint(var3):
					asscode.append("MVI A," + str(var2))
					asscode.append("ORI " + str(var3))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["MVI"] + optable["ORI"] + optable["STA"]
				elif isint(var2):
					if var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var3]))
					asscode.append("ORI " + str(var2))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ORI"] + optable["STA"]
				elif isint(var3):
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("ORI " + str(var3))
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["ORI"] + optable["STA"]
				else:
					if var2 not in symtable[filename] or var3 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + str(symtable[filename][var2]))
					asscode.append("MOV B,A")
					asscode.append("LDA " + str(symtable[filename][var3]))
					asscode.append("ORA B")
					asscode.append("STA " + str(symtable[filename][var1]))
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["ORA"] + optable["STA"]
			elif reloop.match(line):
				var1 = reloop.match(line).group(1)

				if not isint(var1) and var1 not in symtable[filename]:
					error = "Invalid line: " + line
					return
				if isint(var1):
					asscode.append("PUSH E")
					asscode.append("MVI E," + str(var1))
					memadd = memadd + optable["PUSH"] + optable["MVI"]
					symtable[filename]["loop" + str(loops)] = "#" + str(memadd)
					loops = loops + 1
				else:
					asscode.append("PUSH E")
					asscode.append("LDA " + str(symtable[filename][var1]))
					asscode.append("MOV E,A")
					memadd = memadd + optable["PUSH"] + optable["LDA"] + optable["MOV"]
					symtable[filename]["loop" + str(loops)] = "#" + str(memadd)
					loops = loops + 1
			elif reendloop.match(line):
				if loops == 0:
					error = "Invalid line: " + line
					return
				asscode.append("MOV A,E")
				asscode.append("SUI 1")
				asscode.append("MOV E,A")
				asscode.append("JNZ ~~~" + "loop" + str(loops - 1))
				asscode.append("POP E")
				memadd = memadd + optable["MOV"] + optable["SUI"] + optable["MOV"] + optable["JNZ"] + optable["POP"]
			elif reiflt.match(line):
				var1 = reiflt.match(line).group(1)
				var2 = reiflt.match(line).group(2)

				if isint(var1) and isint(var2):
					asscode.append("MVI A," + str(var1))
					asscode.append("SUI " + str(var2))
					asscode.append("JP &&&" + str(ifs))
					asscode.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["MVI"] + optable["SUI"] + optable["JP"] + optable["JZ"]
				elif isint(var1):
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var2])
					asscode.append("SUI " + str(var1))
					asscode.append("JM &&&" + str(ifs))
					asscode.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JM"] + optable["JZ"]
				elif isint(var2):
					if var1 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var1])
					asscode.append("SUI " + str(var2))
					asscode.append("JP &&&" + str(ifs))
					asscode.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JP"] + optable["JZ"]
				else:
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					if var1 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var2])
					asscode.append("MOV B,A")
					asscode.append("LDA " + symtable[filename][var1])
					asscode.append("SUB B")
					asscode.append("JP &&&" + str(ifs))
					asscode.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["JP"] + optable["JZ"]
			elif reifgt.match(line):
				var1 = reifgt.match(line).group(1)
				var2 = reifgt.match(line).group(2)

				if isint(var1) and isint(var2):
					asscode.append("MVI A," + str(var1))
					asscode.append("SUI " + str(var2))
					asscode.append("JM &&&" + str(ifs))
					asscode.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["MVI"] + optable["SUI"] + optable["JM"] + optable["JZ"]
				elif isint(var1):
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var2])
					asscode.append("SUI " + str(var1))
					asscode.append("JP &&&" + str(ifs))
					asscode.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JP"] + optable["JZ"]
				elif isint(var2):
					if var1 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var1])
					asscode.append("SUI " + str(var2))
					asscode.append("JM &&&" + str(ifs))
					asscode.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JM"] + optable["JZ"]
				else:
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					if var1 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var2])
					asscode.append("MOV B,A")
					asscode.append("LDA " + symtable[filename][var1])
					asscode.append("SUB B")
					asscode.append("JM &&&" + str(ifs))
					asscode.append("JZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["JM"] + optable["JZ"]
			elif reifeq.match(line):
				var1 = reifeq.match(line).group(1)
				var2 = reifeq.match(line).group(2)

				if isint(var1) and isint(var2):
					asscode.append("MVI A," + str(var1))
					asscode.append("SUI " + str(var2))
					asscode.append("JNZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["MVI"] + optable["SUI"] + optable["JNZ"]
				elif isint(var1):
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var2])
					asscode.append("SUI " + str(var1))
					asscode.append("JNZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JNZ"]
				elif isint(var2):
					if var1 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var1])
					asscode.append("SUI " + str(var2))
					asscode.append("JNZ &&&" + str(ifs))
					openifs = openifs + 1
					memadd = memadd + optable["LDA"] + optable["SUI"] + optable["JNZ"]
				else:
					if var2 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					if var1 not in symtable[filename]:
						error = "Invalid line: " + line
						return
					asscode.append("LDA " + symtable[filename][var2])
					asscode.append("MOV B,A")
					asscode.append("LDA " + symtable[filename][var1])
					asscode.append("SUB B")
					asscode.append("JNZ &&&" + str(ifs))
					ifs = ifs + 1
					memadd = memadd + optable["LDA"] + optable["MOV"] + optable["LDA"] + optable["SUB"] + optable["JNZ"]
			elif reendif.match(line):
				iftable[ifs - 1] = memadd
			elif refunction.match(line):
				asscode.append("JMP !!!" + str(fnc))
				memadd = memadd + optable["JMP"]
				name = refunction.match(line).group(1)
				globtable[filename][name] = "#" + str(memadd)
				symtable[filename][name] = "#" + str(memadd)
				fnc = fnc + 1
			elif renfun.match(line):
				asscode.append("RET")
				memadd = memadd + optable["RET"]
				fcalls[fnc - 1] = memadd
			elif recall.match(line):
				name = recall.match(line).group(1)
				if name not in symtable[filename]:
					error = "Function " + name + " not declared in " + line
					return
				asscode.append("CALL ~~~" + name)
				memadd = memadd + optable["CALL"]
			elif reassarr.match(line):
				name = reassarr.match(line).group(1)
				disp = reassarr.match(line).group(2)
				val = reassarr.match(line).group(3)
				if name not in symtable[filename] or not isint(disp) or not isint(val):
					error = "Invalid line: " + line
					return
				memaddr = int(symtable[filename][name][1:])
				asscode.append("MVI A," + val)
				asscode.append("STA #" + str(memaddr + int(disp)))
				memadd = memadd + optable["MVI"] + optable["STA"]
			elif line.lstrip().rstrip() != "":
				error = "Invalid line: " + line
				return
		filelentable[filename] = memadd

		assc = '\n'.join(asscode)
		with open(filename.split('.')[0] + '.s1', 'w') as file:
			file.write(assc)
			file.close()

		assco = []

		for line in asscode:
			if "&&&" not in line and "!!!" not in line and "~~~" not in line:
				assco.append(line)
			elif "&&&" in line:
				ifp = line.split("&&&")[1]
				ifp = int(ifp)
				line = line.replace("&&&"+line.split("&&&")[1], "#" + str(iftable[ifp]))
				assco.append(line)
			elif "!!!" in line:
				fnp = line.split("!!!")[1]
				fnp = int(fnp)
				line = line.replace("!!!"+line.split("!!!")[1], "#" + str(fcalls[fnp]))
				assco.append(line)
			else:
				jc = line.split("~~~")[1]
				line = line.replace("~~~" + line.split("~~~")[1], str(symtable[filename][jc]))
				assco.append(line)

		assc = '\n'.join(assco)
		with open(filename.split('.')[0] + '.s2', 'w') as file:
			file.write(assc)
			file.close()

	print
	print "Symbol Table: "
	print symtable
	print
	print "Opcode table: "
	print optable
	print
	print "Global table: "
	print globtable
	print
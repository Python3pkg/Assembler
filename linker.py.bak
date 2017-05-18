import assembler

error = "False"
startaddfile = {}
filelentable = assembler.filelentable
globtable = assembler.globtable

def findfile(string, files):
	for file in files:
		if string in globtable[file.split('.')[0]] and "#" in globtable[file.split('.')[0]][string]:
			return file.split('.')[0], globtable[file.split('.')[0]][string].split("#")[1]
	return "Not found", "-1"

# def findfunction(string, files):
# 	for file in files:
# 		if string in functions[file.split('.')[0]] and '#' in functions[file.split('.')[0]][string]:
# 			return file.split('.')[0], functions[file.split('.')[0]][string].split("#")[1]
# 	return "Not found", "-1"

def convert(fileNames):
	global error
	global startaddfile
	global filelentable
	global globtable
	startaddfile = {}
	filelentable = assembler.filelentable
	globtable = assembler.globtable
	error = "False"
	memadd = 0
	for filename in fileNames:
		startaddfile[filename.split('.')[0]] = memadd
		memadd = memadd + filelentable[filename.split('.')[0]]

	asscode = []

	for filenam in fileNames:
		filename = filenam.split('.')[0]
		with open(filename + '.s2', 'r') as file:
			lines = file.read().split('\n')
			file.close()

		for line in lines:
			if '$' not in line and '#' not in line:
				asscode.append(line)
			elif '#' in line:
				addr = line.split('#')[1]
				addr = str(int(addr) + startaddfile[filename])
				line = line.replace('#' + line.split('#')[1], '#' + addr)
				asscode.append(line)
			elif '$' in line:
				fname, add = findfile(line.split('$')[1], fileNames)
				if fname == "Not found":
					error = "External variable " + line.split('$')[1] + " not found: " + line
					return
				line = line.replace('$' + line.split('$')[1], "#" + str(int(add) + startaddfile[fname]))
				asscode.append(line)

	with open(fileNames[0].split('.')[0] + '.s3', 'w') as file:
		file.write("\n".join(asscode))
		file.close()
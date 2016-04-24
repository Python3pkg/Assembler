import assembler
import linker
import loader

error = "False"
offset = 0

def process(filenames, offset):
	global error
	error = "False"
	assembler.convert(filenames)
	if assembler.error != "False":
		print(assembler.error, "assembler")
		error = assembler.error
		return
	linker.convert(filenames)
	if linker.error != "False":
		print(linker.error, "linker")
		error = linker.error
		return
	loader.convert(filenames[0], offset)

def make_it(file, offse):
	with open(file, "r") as f:
		files = f.read().split("\n")
		f.close()
	if files[-1] == "":
		files = files[:-1]
	rel = file.split('/')[-1]
	base = file[:-len(rel)]
	for i in range(len(files)):
		files[i] = (base + files[i]).encode("utf-8")
	process(files, offse)
	global offset
	offset = offse
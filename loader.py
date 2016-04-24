def convert(filename, offset):
	with open(filename.split('.')[0] + '.s3', 'r') as file:
		lines = file.read().split('\n')
		file.close()

	asscode = []

	for line in lines:
		if '#' in line:
			add = int(line.split('#')[1])
			add = str(add + offset)
			line = line.replace('#' + line.split('#')[1], add)
			asscode.append(line)
		else:
			asscode.append(line)

	asscode.append('HLT')

	with open(filename.split('.')[0] + '.final', 'w') as file:
		file.write('\n'.join(asscode))
		file.close()
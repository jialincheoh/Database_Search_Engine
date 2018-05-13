
def get_atoms(filename):
	input_atoms = {}
	with open(filename) as input_file:
		input_data = input_file.readlines()
		for line in input_data:
			line_data = line.split()
			atom = line_data[0]
			if atom not in input_atoms:
				input_atoms[atom] = 0
			input_atoms[atom] += 1
	return input_atoms


input_data1 = get_atoms('isomer1')

input_data2 = get_atoms('isomer2')

if input_data1 == input_data2:
	print('is a structural isomer')
else:
	print('NOT an isomer')

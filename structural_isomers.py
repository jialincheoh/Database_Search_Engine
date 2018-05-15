
def get_atoms(filename):
	input_atoms = {}
	with open(filename) as input_file:
		input_data = input_file.readlines()
		for line in input_data:
			line = line.strip()
			if not line:
				continue
			line_data = line.split()
			atom = line_data[0]
			if atom not in input_atoms:
				input_atoms[atom] = 0
			input_atoms[atom] += 1
	return input_atoms


def is_isomer(filename1, filename2):
	input_data1 = get_atoms(filename1)
	input_data2 = get_atoms(filename2)
	print(input_data1)
	print(input_data2)

	return input_data1 == input_data2


if __name__ == "__main__":

	is_iso = is_isomer('data/water.zmat', 'data/water_frag6.zmat')

	if is_iso:
		print('is a structural isomer')
	else:
		print('NOT an isomer')

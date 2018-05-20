# isomers

### Setup

Install open babel:

	brew install open-babel

Create a python3 virtualenv, e.g.:

	conda create -n isomers scipy

Activate virtualenv:

	conda activate isomers

Install requirements:

	pip install -r requirements.txt


### Usage

1. Find a .pdb file you want to test.
2. Put it in the ~/Documents/isomers/data/ directory.
3. Run the script:
	
	conda activate isomers
	python execute_all_scripts.py data/<filename>

where filename is the name of the pdb file you want to test
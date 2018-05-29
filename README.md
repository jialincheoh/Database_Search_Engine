# isomers

Contributors

Yen Bui </br> 
Jia Lin

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

1. Find a .xyz file you want to test.
2. Put it in the iSpiEFP_Database_Search_Engine/data/ directory.
3. Ensure you are in the correct directory with the virtualenv active:

	cd /path/to/iSpiEFP_Database_Search_Engine  # Wherever you cloned the search engine
	conda activate isomers  # Whatever you called your virtualenv during setup

3. Run the script:
	
	python execute_all_scripts.py data/filename

where filename is the name of the xyz file you want to test

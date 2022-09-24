## File Descriptions

- `ns.py-main` contains the ns.py package for simulation.
- `Octopus-Micro` contains the codes of OctopusSketch and MicroSketch.
- `workplace` contains the main program and parameter settings for simulation.

## Usage
### Basic Setups
##### ns.py Setups
- Go to `./ns.py-main`
- Type `python setup.py install` to build ns.py environment


##### pybind Setups
- Go to `./` folder.
- Type `pip install pybind11-2.10.0-py3-none-any.whl` to install pybind

### More functions and tools

- Generate errors using `./workplace/utils/create_error.py`.

- Generate DCTCP distribution using `./workplace/utils/TCP_distribution.py`. 
	

### Running Simulations
- Go to `./workplace/simu` folder.
- Type `bash c.sh` to bind the OctopusMon implemented in C++ to the simulation implemented in Python
- Type `bash simu.sh` to run the simulation

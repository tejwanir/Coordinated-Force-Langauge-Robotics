# Coordinated-Force-Langauge-Robotics

TODO: project description

# Environment Setup

## MacOS

### Virtual environment setup using `pyenv` and `pyenv-virtualenv`
It's recommended to have on your system [`pyenv`](https://github.com/pyenv/pyenv) to manage multiple Python versions and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv) to manage multiple virtual environments alongside `pyenv`.
1. Install Python 3.8

    ```
    pyenv install 3.8.[some patch version]
    ```
2. Create the virtual environment

    ```
    pyenv virtualenv 3.8.[some patch version] [the virtual environment name]
    ```
3. Activate the virtual environment

    ```
    pyenv activate [the virtual environment name]
    ```
    Can optionally set the virtual environment locally for the project by creating a `.python-version` at the root directory of the project
    ```
    pyenv local [the virtual environment name]
    ```
4. Verify the virtual environment is activated
    ```
    pyenv version
    ```
    The output should show
    ```
    [the virtual environment name] (set by [some path]/[the virtual environment name]/.python-version)
    ```
3. Verify the correct Python version is being used

    ```
    python --version
    ```
    The output should show
    ```
    Python 3.8.[some patch version]
    ```
6. Verify the correct pip is being used

    ```
    pip --version
    ```
    The output should show
    ```
    pip [some version] from [some path]/.pyenv/versions/[the virtual environment name]/lib/python3.8/site-packages/pip (python 3.8)
    ```
### Install project modules
Once a virtual environment that uses Python version `3.8` is activated, simply run:
```
pip install -r requirements.txt
```
### Configure UR Robot

TODO: describe network ip stuff, maybe mention robot specs like specific model etc

# Repository Structure
```
Coordinated-Force-Language-Robotics/
├── src/
│   ├── __init__.py
│   ├── services/
│   │   ├── some_service/
│   │   │   ├── __init__.py
│   │   │   ├── some_service_code.py
│   │   │   └── ...
│   │   └── ...
│   ├── common/
│   │   ├── __init__.py
│   │   ├── some_common_code.py
│   │   └── ...
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── some_script.py
│   │   └── ...
│   ├── main.py
│   └── ...
├── notebooks/
│   ├── preamble.py
│   ├── notebook.ipynb
│   ├── ...
│   └── significant_notebook.ipynb
├── .gitignore
├── requirements.txt
└── README.md
```

- `Coordinated-Force-Language-Robotics` - project root
- `src/` - project source code
- `src/__init__.py` - makes `src/` a package which allows project source code to be imported into other code outside of `src/` such as `notebooks/`
- `src/services/` - project source code is split into multiple services that are responsible for different features and logic; one example is the service that manages and controls the robot
- `src/services/some_service/` - holds all of the code for a particular service
- `src/common/` - holds common code used throughout project source code
- `src/scripts/` - helper scripts that are their own entry points
- `src/main.py` - entry point of the project source code
- `notebooks/` - while notebooks are git ignored no matter where they exist in the project directory structure, put any created notebooks into this appropiate folder; any files in this directory are gitignored by default as well
- `notebooks/preamble.py` - helper script that if imported into a notebook will allow further imports from `src/`; this file is not gitignored
- `notebooks/significant_notebook.ipynb` - any significant files in `notebooks/` that should be commmitted must inclulde the line in the `.gitignore` file:
    ```
    !notebooks/[name of significant notebook].ipynb
    ```
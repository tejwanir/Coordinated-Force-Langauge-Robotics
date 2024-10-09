# Coordinated-Force-Langauge-Robotics

TODO: project description

# Environment Setup

## MacOS

### Virtual environment setup using `pyenv` and `pyenv-virtualenv`
It's recommend having on your system [`pyenv`](https://github.com/pyenv/pyenv) to manage multiple Python versions and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv) to manage multiple virtual environments alongside `pyenv`.
1. Install Python 3.117

    ```
    pyenv install 3.11.7
    ```
2. Create the virtual environment

    ```
    pyenv virtualenv 3.11.7 Coordinated-Force-Language-Robotics
    ```
3. Verify the virtual environment is activated while in the project directory. There is already a `.python-version` file in the project root that will automatically let `pyenv` and `pyenv-virtualenv` know to use the virtual environment that was just created
    ```
    pyenv version
    ```
    The output should show
    ```
    Coordinate-Force-Language-Robotics (set by [some path]/Coordinate-Force-Language-Robotics/.python-version)
    ```
4. Verify the correct Python version is being used

    ```
    python --version
    ```
    The output should show
    ```
    Python 3.11.7
    ```
5. Verify the correct pip is being used

    ```
    !pip --version
    ```
    The output should show
    ```
    pip [some version] from [some path]/.pyenv/versions/Coordinate-Force-Language-Robotics/lib/python3.11/site-packages/pip (python 3.11)
    ```
### Install project modules
Once a virtual environment named `Coordinated-Force-Language-Robotics` that uses Python version `3.11.7` exists on the system, simply run:
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
│   └── ...
├── notebooks/
│   ├── notebook.ipynb
│   ├── ...
│   └── significant_notebook.ipynb
├── .gitignore
├── .python-version
├── requirements.txt
└── README.md
```

- `Coordinated-Force-Language-Robotics` - project root
- `src` - project code
- `__init__.py` - makes `src` a module which allows project code to be imported into interactive python notebooks
- `notebooks` - while notebooks are git ignored no matter where they exist in the directory structure, put any created notebooks into this appropiate folder
- `significant_notebook.ipynb` - any significant notebooks that should be commmitted must inclulde the line in the `.gitignore` file:
    ```
    !notebooks/[name of significant notebook].ipynb
    ```
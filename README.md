# Projman

This is a tool to help initializing and developing python projects, speeding up the
development process.

It exposes every internal as a library, allowing it to be extended/overridden with
custom functionalities and behaviour.



## Overview

Projman uses _.projman_ files to manage the project, which describes the
project general structure and allows custom extensions (its a sort _package.json_ rip off)

An example ._projman_ file has the following structure

```
version: 3.6            # python version

name: example           # project name

dependencies: [         # project dependencies
    dep1==1.0.0,
    dep2==1.0.1
]

main: example.py        # path to the entrypoint of the project 
                        # if any, this will be executed with the run command

test-dir: example/tests # path of the tests directory
                        # if any, this will be executed with the test command

venv: "~/example-venv"  # path to the project virtual environment

commands: {             # map of custom commands  
"mycommand": "..."
}

```


## Installation

## Usage

```
projman [COMMAND] [...ARGS]
```

#### Commands

- __init__ : initialize the project structure and creates the virtual environment with
the specified python version, installing every defined dependency

    - ___--no-venv___ skip virtualenv creation  
    - ___--skip-install___ skip dependencies installation
    
- __install__ : installs the project dependencies

- __setup__ : activates the project virtual environment
    
    - ___--install___ : install project dependencies

- __run__ : runs a command  
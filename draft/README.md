# draft

A template based command-line-utility to create exams or worksheets using 
LaTeX and LilyPond.

## Installation

Install this tool with:

```
pip install draft
```

## Develop

This package uses [Poetry](https://python-poetry.org/) as its build tool 
([Installation](https://python-poetry.org/docs/#installation)).
There is also good documentation available in the docs of [Typer](https://typer.tiangolo.com/): 
[Building a Package - Typer](https://typer.tiangolo.com/tutorial/package/) 
(albeit a bit outdated: Running the tool is different).

#### Install poetry and pipx

```
brew install pipx
pipx ensurepath

pipx install poetry
```

### Running the tool

The tool can be run in a local environment. 

> 🚨 Important: You must be in the directory `./draft/` starting at 
> the root of the repository.

```
poetry install
poetry shell
draft
```

The first line resolves all necessary dependencies. They are somewhat persisted
between instances of the local environment.

### Adding new dependencies

New dependecies are added with

```
poetry add "dependency_name"
```

([More information](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment))

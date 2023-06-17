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
(albeit a bit outdated).

### Running the tool

To locally execute `draft`, first run `poetry shell`. Draft is then available 
to be run in the local environment and any changes to its source are immediatly
applied. 

Exit the local environment with `exit` or `deactivate`.
(See the [documentation](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment)
of poetry for more information.)

### Adding new dependencies

New dependecies are added with

```
poetry add "dependency_name"
```

([More information](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment))

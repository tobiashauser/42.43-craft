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

The tool itself can be run in a local environment.

```
poetry install
poetry shell
draft
```

The first line resolves all necessary dependencies and installs the tool which
is then somewhat persisted between instances of the local environment.

### Adding new dependencies

New dependencies are added with

```
poetry add "dependency_name"
```

([More information](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment))


## Some Documentation

```tex
% A template can use placeholders that will be replaced during
% the compilation. Placeholders have the form: <<IDENTIFIER>>.
% They can be customized inside this file in a YAML-formatted preface.
% 🚨 It cannot contain any colons.
% PLACEHOLDERS ------------------------------------------------------------ %
\iffalse
prompts:
- semantic-name:
	type: input
	message: Please enter the a semantic name for this document.
- group:
	message: Which group is this document for?
\fi
% ------------------------------------------------------------------------- %
% Draft uses the python package PyInquirer to create the prompts.
% See their documentation for more information.
% The key `name` will be created by default from the key name. Make sure
% this name matches the one used in document. If no `message` is provided
% it will fall back to the name. The default type of the prompt is `input`.
% The keys `filter` and `validate` cannot be used.
```

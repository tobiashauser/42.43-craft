import oyaml as yaml
from pathlib import Path
import re
from rich import print
import typer
from typing import List, Dict, Set

from .helpers import fetch_github_directory


class Headers:
    """
    A class encapsulating the headers directory in the configuration.
    """

    def __init__(self, path: Path):
        self.path = path
        self.validate()

        headers: List[Header] = []
        for file in self.path.iterdir():
            if file.is_file() and file.suffix == '.tex':
                try:
                    headers.append(Header(file))
                except:
                    pass
        self.headers = headers

    def validate(self):
        # - directory exists
        if not self.path.is_dir():
            self.path.mkdir(parents=True, exist_ok=True)

        # directory is not empty
        if not any(self.path.iterdir()):
            typer.confirm(
                "Do you want to fetch the header templates from GitHub?",
                abort=True
            )
            documents = fetch_github_directory(
                'tobiashauser',
                '42.43-draft',
                'templates/headers'
            )
            for name, contents in documents.items():
                with (self.path / name).open('w') as file:
                    file.write(contents)


class Header:
    """
    A class representing one header file in the templates' directory.
    """

    def __init__(self, path: Path):
        self.path = path
        self.validate()

        self.load()

        self.prompts = Header.create_prompts(
            Header.extract_yaml(self.contents).get('prompts', []),
            Header.extract_placeholders(self.contents)
        )

    def validate(self):
        # - is file
        # - file is not empty
        if (not self.path.is_file()) \
                or self.path.stat().st_size == 0:
            print("[red]TODO: Faulty header template.[/red]")
            raise typer.Abort()

    def load(self):
        """
        Load the header from the disk.
        """

        with self.path.open('r') as file:
            self.contents = file.read()

    @staticmethod
    def extract_yaml(contents: str):
        """
        Parses any YAML-formatted block comments and
        returns one dictionary holding all values.
        """
        pattern = re.compile(r"(?s)\n\\iffalse\n(.*?)\\fi")
        matches = pattern.findall(contents)

        dict = {}
        for match in matches:
            try:
                for key, value in yaml.safe_load(match).items():
                    if key not in dict:
                        dict[key] = value
                    elif isinstance(dict[key], list):
                        if isinstance(value, list):
                            dict[key] = dict[key] + value
                        else:
                            dict[key] = dict[key] + [value]
            except:
                pass
        return dict

    @staticmethod
    def create_prompts(dict: list, placeholders: Set[str]):
        """
        Create well structured prompts from YAML-dictionary
        that inserts default values if necessary cleans up
        the data.
        """

        prompts = []
        for item in dict:
            for name, values in item.items():
                if name not in placeholders:
                    continue
                question = {}
                # order: type, name, message, ...
                if 'type' not in question:
                    question['type'] = 'input'
                question['name'] = name
                if 'message' not in question:
                    question['message'] = "Please provide the %s." % name
                for key, value in values.items():
                    question[key] = value

                prompts.append(question)
                placeholders.remove(name)

        # create default prompts for any undeclared placeholders
        for name in placeholders:
            question = {}
            question['type'] = 'input'
            question['name'] = name
            question['message'] = "Please provide the %s." % name
            prompts.append(question)

        return prompts

    @staticmethod
    def extract_placeholders(contents: str) -> Set[str]:
        """
         Extract any placeholders (<<IDENTIFIER>>) found in contents.
        """
        pattern = re.compile(r"<<([^\s.]+?)>>")
        matches = pattern.findall(contents)
        return set(matches)

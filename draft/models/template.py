from abc import ABC, abstractmethod
import oyaml as yaml
import re
from rich import print
from pathlib import Path
from typing import Set, Dict, Any, List


class Folder(ABC):
    """
    An abstraction over a directory on the disk.
    """

    @property
    @abstractmethod
    def path(self) -> Path:
        pass

    @abstractmethod
    def validate(self):
        pass


class Template(ABC):
    """
    An abstract base class representing a template file on the
    disk such as a Header, an Exercise or the Preamble.

    This class follows the pattern in that it defines an internal
    property with an underscore and then defines a `@property` (getter)
    that access the underlying storage and sets it if accessed for the
    first time.
    """
    @property
    @abstractmethod
    def path(self) -> Path:
        pass

    _yaml = None
    _placeholders = None
    _prompts = None
    _contents = None

    @property
    def yaml(self) -> Dict[str, Any]:
        if self._yaml is None:
            self.__extract_yaml__()
        return self._yaml

    @property
    def placeholders(self) -> Set[str]:
        if self._placeholders is None:
            self.__extract_placeholders__()
            return self._placeholders

    @property
    def prompts(self) -> Dict[str, Any]:
        if self._prompts is None:
            self.__create_prompts__()
        return self._prompts

    @property
    def contents(self) -> str:
        if self._contents is None:
            self.__load__()
        return self._contents

    @property
    def name(self) -> str:
        return self.path.stem

    def validate(self):
        # - is file
        # - file is not empty
        if (not self.path.is_file()) \
                or self.path.stat().st_size == 0:
            print("[red]TODO: Faulty template.[/red]")
            raise typer.Abort()

    def __load__(self):
        """
        Load the file contents from the disk.
        """
        with self.path.open('r') as file:
            self._contents = file.read()

    def __extract_yaml__(self):
        """
        Parses any YAML-formatted block comments and
        returns one dictionary holding all values.
        """
        if self.contents is None:
            self.load()

        pattern = re.compile(r"(?s)\n\\iffalse\n(.*?)\\fi")
        matches = pattern.findall(self.contents)

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
        self._yaml = dict

    def __extract_placeholders__(self):
        """
        Extract any placeholders (<<IDENTIFIER>>) found in contents.
        """
        pattern = re.compile(r"<<([^\s.]+?)>>")
        matches = pattern.findall(self.contents)
        self._placeholders = set(matches)

    def __create_prompts__(self):
        """
        Create well structured prompts from YAML-dictionary
        that inserts default values if necessary cleans up
        the data.
        """
        dict = self.yaml.get('prompts', [])
        placeholders = self.placeholders

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

        self._prompts = prompts

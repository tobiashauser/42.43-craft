import re
from abc import ABC
from pathlib import Path
from typing import Any, Dict, List, Set

import oyaml as yaml

from draft.common.File import File
from draft.common.helpers import combine_dictionaries


class Template(File, ABC):
    """
    A abstract class representing a template, that is, a file
    on the disk.

    Conforming types are:
    - TexTemplate (ABC)

    Subclasses should remember to call `super().__init__()`
    if they implement their own initializer.
    """

    @property
    def placeholder_prefix(self) -> str:
        return self._placeholder_prefix

    @property
    def placeholder_suffix(self) -> str:
        return self._placeholder_suffix

    @property
    def placeholders(self) -> Set[str]:
        return self._placeholders

    @property
    def prompts(self) -> List[Dict[str, Any]]:
        return self._prompts

    @property
    def yaml_prefix(self) -> str:
        return self._yaml_prefix

    @property
    def yaml_suffix(self) -> str:
        return self._yaml_suffix

    @property
    def yaml(self) -> Dict[str, Any]:
        return self._yaml

    def __init__(
        self,
        path: Path,
        placeholder_prefix: str,
        placeholder_suffix: str,
        yaml_prefix: str,
        yaml_suffix: str,
    ):
        """
        Take care to pass properly escaped string literals for
        `placeholder_prefix`, `placeholder_suffix`, `yaml_prefix`,
        `yaml_suffix` to the initialiser:

        ```
        yaml_prefix=r"\\iffalse",
        ```
        """
        super().__init__(path=path)

        # Placeholders
        self._placeholder_prefix: str = placeholder_prefix
        self._placeholder_suffix: str = placeholder_suffix
        self.__init_placeholders__()

        # YAML
        self._yaml_prefix = yaml_prefix
        self._yaml_suffix = yaml_suffix
        self.__init_yaml__()

        # Prompts
        self.__init_prompts__()

    def __init_placeholders__(self):
        """
        Extract handlebars like `<<semester>>` from the
        contents of the template.
        """
        pattern = re.compile(
            r"%s([^\s.]+?)%s" % (self.placeholder_prefix, self.placeholder_suffix)
        )
        matches = pattern.findall(self.contents)
        self._placeholders = set(matches)

    def __init_yaml__(self):
        """
        Parse and combine YAML-frontmatter from all the
        block comments in the contents.

        YAML-blocks closer to the top of the document take
        priority over those further down.
        List and dictionary values will be combined.
        """

        # Extract all the block comments
        pattern = re.compile("(?s)\n%s(.*?)%s" % (self.yaml_prefix, self.yaml_suffix))
        matches = pattern.findall(self.contents)

        dict: Dict[str, Any] = {}

        # Iterate over all the block comments
        for match in matches:
            try:
                dict = combine_dictionaries(dict, yaml.safe_load(match))
            except:
                pass
            """
            TODO: This setup silently fails any block comments that are not valid yaml.
            This is necessary to allow any kind of block comment in the templates.
            Maybe a warning should be printed?
            """

        self._yaml = dict

    def __init_prompts__(self):
        """
        Create prompts for PyInquirer from the placeholders
        in the file.

        They can be customized in any YAML-block.
        """

        prompts: List[Dict[str, Any]] = []

        for placeholder in self.placeholders:
            question: Dict[str, Any] = {}

            # set the minimum default values
            question["name"] = placeholder
            question["type"] = "input"
            question["message"] = "Please provide the '%s'." % placeholder

            # customize if this placeholder was customized
            if isinstance(self.yaml.get(placeholder, {}), dict):
                for key, value in self.yaml.get(placeholder, {}).items():
                    # the name cannot be customized
                    if key == "name":
                        continue
                    elif key == "validate":
                        # TODO: this is a security risk that should be controlled by a global setting
                        question[key] = eval(value)
                    else:
                        question[key] = value

            prompts.append(question)

        self._prompts = prompts

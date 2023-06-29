import re
from abc import ABC

from draft.common.DiskRepresentable import DiskRepresentable


class File(ABC, DiskRepresentable):
    """
    Abstract class representing a file on the disk.

    Subclasses:
    - Template (ABC)

    Subclasses should remember to call `super().__init__()`
    if they implement their own initializer.
    """

    _contents: str

    @property
    def contents(self) -> str:
        return self._contents

    def __init__(self, path):
        self._path = path
        self.load()

    def load(self):
        with self.path.open("r") as file:
            self._contents = file.read()

    def remove_lines(self, prefix: str):
        """
        Removes all lines starting with the given
        prefix from the contents of the file.

        General case:
        ```text
        Paragraph before... ──┐
                              |
        % This is a comment ──┤
                              │
                              │ this will be deleted
                              │
        Paragraph after...  ──┤
        ```

        Special case:
        ```text
        Paragraph one ...   ──┐
        % this is the end   ──┤
                              │ this will be deleted
                              │ and replaced with a
                              │ newline.
        Paragraph after...  ──┤
        ```
        """
        # Handle `test_single_line_and_contents_condensed_leading` and
        # `test_multiple_lines_and_contents_condensed_leading` first
        pattern = re.compile(
            "(?<=.\n)(?:^%s.*?\n?)+(?:^\n)+(?=.)" % prefix, re.MULTILINE
        )
        self._contents = re.sub(pattern, "\n", self.contents)

        # General cases
        pattern = re.compile("^%s.*\n*" % prefix, re.MULTILINE)
        self._contents = re.sub(pattern, "", self.contents)

    def remove_blocks(self, prefix: str, suffix: str):
        r"""
        Removes all blocks enclosed by the given
        prefix and suffix from the contents of the file.

        General case:
        ```text
        Paragraph before... ──┐
                              |
        \iffalse            ──┤
        This is a comment     │
        \fi                   │ this will be deleted
                              │
                              │
        Paragraph after...  ──┤
        ```

        Special case:
        ```text
        Paragraph one ...   ──┐
        \iffalse            ──┤
        This is a comment     │ this will be deleted
        \fi                   │ and replaced with a
                              │ newline.
        Paragraph after...  ──┤
        ```
        """
        # Special case
        pattern = re.compile(
            "(?s)(?<=\\w\n)(%s(?:.*?)%s\n)+^\n+?(?=\\w)" % (prefix, suffix),
            re.MULTILINE,
        )
        self._contents = re.sub(pattern, "\n", self.contents)

        # General case
        pattern = re.compile("(?s)^%s(.*?)%s\n*" % (prefix, suffix), re.MULTILINE)
        self._contents = re.sub(pattern, "", self.contents)

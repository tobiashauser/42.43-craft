# bug fix
import collections.abc

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import prompt
from rich import print

from draft.common.Configuration import Configuration
from draft.common.Header import Header
from draft.common.Preamble import Preamble
from draft.new.DocumentNameValidator import DocumentNameValidator


class Compiler:
    """
    Class that handles compiling a document.
    """

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    @property
    def preamble(self) -> Preamble:
        return self._preamble

    @property
    def header(self) -> Header:
        return self._header

    @property
    def document(self) -> str:
        return self._document

    @document.setter
    def document(self, newValue: str):
        self._document = newValue

    def __init__(self, configuration: Configuration, header: Header):
        self._configuration = configuration
        self._preamble = Preamble(self.configuration.preamble, self.configuration)
        self._header = header
        self._document = ""

    def compile(self):
        """
        Compile the document. This involves the following steps:

        1. What should the compiled document be called?
        2. Resolve any prompts in the preamble. Then add its contents to
           `self.document`.
        """
        # Ask for the name of the compiled document.
        question = [
            {
                "type": "input",
                "name": "document-name",
                "message": "What should the compiled document be called?",
                "default": self.header.name,
                "when": lambda a: "document-name" not in self.configuration,
                "validate": DocumentNameValidator,
            }
        ]
        document_name = prompt(question)
        print(document_name)
        print(self.configuration)

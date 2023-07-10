# bug fix
import collections.abc

from draft.common.Prompt import Input
from draft.common.Prompter import Prompter

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

    @property
    def prompter(self) -> Prompter:
        return self._prompter

    def __init__(self, configuration: Configuration, header: Header):
        self._configuration = configuration
        self._preamble = Preamble(self.configuration.preamble, self.configuration)
        self._header = header
        self._document = ""
        self._prompter = Prompter(configuration)

    def compile(self):
        """
        Compile the document. This involves the following steps:

        1. What should the compiled document be called?
        2. Resolve any prompts in the preamble. Then add its contents to
           `self.document`.
        """
        # Ask for the name of the compiled document.
        question = Input(
            name="document-name",
            message="What should the compiled document be called?",
            when=lambda a: "document-name" not in self.configuration,
            default=self.header.name,
            validate=DocumentNameValidator,
        )
        self.prompter.ask(question)

        # Process the preamble
        print(self.preamble.prompts)
        prompt(self.preamble.prompts)
        # self.prompter.ask(self.preamble.prompts)
        # print(self.configuration)

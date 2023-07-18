from typing import Callable

import typer
from rich import print
from rich.panel import Panel
from typing_extensions import Annotated

from draft.common.Header import Header
from draft.common.TemplateManager import TemplateManager
from draft.configuration.Configuration import Configuration
from draft.configuration.VerboseValidator import VerboseValidator
from draft.debug.Debugger import Debugger
from tests.new.test_Compiler import Compiler


class Subcommands:
    """
    Initialize the subcommands; one for each header declared in the
    templates:
    - draft new exam
    - draft new worksheet

    Hand off the neccessary files to the compiler.
    """

    @property
    def template_manager(self) -> TemplateManager:
        return self._template_manager

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    def __init__(
        self,
        configuration: Configuration,
        template_manager: TemplateManager,
    ):
        self._template_manager = template_manager
        self._configuration = configuration

    def add_subcommands(self, app: typer.Typer):
        for header in self.template_manager.headers:
            app.command(name=header.name, help="Create a new %s." % header.name)(
                self.create_subcommand_for(header)
            )

    def create_subcommand_for(self, header: Header) -> Callable[..., None]:
        def subcommand(
            verbose: Annotated[
                bool, typer.Option(help="Output additional information.")
            ] = False,
        ):
            self.configuration[VerboseValidator().key] = verbose
            self.configuration.header = header.name
            compiler = Compiler(self.configuration)  # type: ignore

            if self.configuration.verbose:
                Debugger(self.configuration).run()

            compiler.compile()

        return subcommand

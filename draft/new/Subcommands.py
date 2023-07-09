from typing import Callable

import typer
from rich import print

from draft.common.Configuration import Configuration
from draft.common.Header import Header
from draft.common.TemplateManager import TemplateManager
from draft.new.Compiler import Compiler


class Subcommands:
    """
    Initialize the subcommands; one for each header declared in the
    templates:
    - draft new exam
    - draft new worksheet

    Hand off the neccessary files to the compiler.
    """

    @property
    def app(self) -> typer.Typer:
        return self._app

    @property
    def template_manager(self) -> TemplateManager:
        return self._template_manager

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    def __init__(
        self,
        app: typer.Typer,
        configuration: Configuration,
        template_manager: TemplateManager,
    ):
        self._app = app
        self._template_manager = template_manager
        self._configuration = configuration

        # Initialize the subcommands
        self.__init_subcommands__()

    def __init_subcommands__(self):
        for header in self.template_manager.headers:
            self.app.command(name=header.name, help="Create a new %s." % header.name)(
                self.create_subcommand_for(header)
            )

    def create_subcommand_for(self, header: Header) -> Callable[..., None]:
        def subcommand():
            compiler = Compiler(self.configuration, header)
            compiler.compile()

        return subcommand

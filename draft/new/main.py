from rich import print
import typer
from typing import Callable

from ..models.configuration import Configuration
from ..models.headers import Header

from .document import Document

app = typer.Typer(no_args_is_help=True)


# Dynamically create a subcommand for each header in 'templates/header/' #
# ---------------------------------------------------------------------- #
def subcommand(header: Header) -> Callable[None, None]:
    def logic():
        document = Document(header)

    return logic


for header in Configuration().headers:
    app.command(
        name=header.name,
        help="Create a new %s." % header.name
    )(subcommand(header))


# draft new template #
# ------------------ #

@app.command("template", help="Create a new template.")
def template():
    print("[violet]TODO: Implement [bold white]draft new "
          "template[/bold white][/violet].")

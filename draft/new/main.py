from rich import print
import typer
from typing import Callable

from ..models.configuration import Configuration
from ..models.headers import Header

from .document import Document


app = typer.Typer(no_args_is_help=True)
configuration = Configuration()


# Dynamically create a subcommand for each header in 'templates/header/' #
# ---------------------------------------------------------------------- #
def subcommand(
    header: Header,
    configuration: Configuration
) -> Callable[None, None]:
    def logic():
        document = Document(header, configuration)
        document.user_values
        print(document.exercises)

    return logic


for header in configuration.headers:
    app.command(
        name=header.name,
        help="Create a new %s." % header.name
    )(subcommand(header, configuration))


# draft new template #
# ------------------ #

@app.command("template", help="Create a new template.")
def template():
    print("[violet]TODO: Implement [bold white]draft new "
          "template[/bold white][/violet].")

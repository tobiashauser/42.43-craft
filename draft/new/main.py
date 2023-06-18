import typer
from typing import Callable

app = typer.Typer(no_args_is_help=True)


def command(name: str) -> Callable[None, None]:
    def subcommand():
        print(name)

    return subcommand


commands = ["exam", "worksheet"]

for c in commands:
    app.command(name=c)(command(c))

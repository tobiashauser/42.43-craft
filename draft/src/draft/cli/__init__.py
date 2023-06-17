# Declarations of the command line interface
import typer
from rich import print

draft = typer.Typer()

@draft.command()
def hi():
    print("[red bold]Hello, world![/red bold]")
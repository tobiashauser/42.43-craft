# Declarations of the command line interface
import typer
from rich import print

# import the different subcommands

app = typer.Typer()


@app.command()
def hi():
    print("Hello, world!")


@app.command()
def bye():
    print("Good Bye")

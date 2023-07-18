import typer

from draft.debug.main import app as debug
from draft.new.main import app as new

app = typer.Typer(no_args_is_help=True)


@app.command("test")
def test():
    print("Hello, world!")
    print("Hello, Pluto!")


app.add_typer(new, name="new", help="Create a new document.")
app.add_typer(
    debug,
    name="debug",
    help="Output the configuration in with which the tool would run.",
)

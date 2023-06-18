import typer
from pathlib import Path

from .models.configuration import Configuration
from .models.headers import Header
from .models.exercises import Exercise
from .models.helpers import fetch_github_directory
from .new.main import app as new
from .templates.main import app as templates

app = typer.Typer(no_args_is_help=True)
app.add_typer(new, name="new")
app.add_typer(templates, name="templates")


@app.command("test")
def always():
    c = Configuration()
    print(c.preamble.yaml)

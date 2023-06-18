import typer

from .models.configuration import Configuration
from .models.helpers import fetch_github_directory
from .new.main import app as new
from .templates.main import app as templates

app = typer.Typer(no_args_is_help=True)
app.add_typer(new, name="new")
app.add_typer(templates, name="templates")


@app.command("test")
def always():
    Configuration()

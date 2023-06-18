import typer

from .models.Configuration import Configuration
from .new.main import app as new
from .templates.main import app as templates

app = typer.Typer(no_args_is_help=True)
app.add_typer(new, name="new")
app.add_typer(templates, name="templates")


@app.command("test")
def always():
    Configuration()

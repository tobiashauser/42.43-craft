import typer

from .new.main import app as new
from .template.main import app as template

app = typer.Typer(no_args_is_help=True)
app.add_typer(new, name="new")
app.add_typer(template, name="template")

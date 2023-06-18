import typer
from .models.Configuration import Configuration

app = typer.Typer()


@app.command("new")
def new():
    Configuration()

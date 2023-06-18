import typer
from .models.Configuration import Configuration

app = typer.Typer()


@app.command("new")
def new():
    config = Configuration()
    print(config.headers.headers)

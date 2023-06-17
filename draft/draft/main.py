import typer 

app = typer.Typer()

@app.command("new")
def new():
    typer.echo("Hello, world!")

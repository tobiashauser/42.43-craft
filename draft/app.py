import typer

app = typer.Typer(no_args_is_help=True)


@app.command("test")
def test():
    print("Hello, world!")

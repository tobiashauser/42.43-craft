import typer

app = typer.Typer(no_args_is_help=True)


@app.command("exam")
def exam():
    print("exam")


@app.command("worksheet")
def worksheet():
    print("worksheet")

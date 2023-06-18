from rich import print
import typer

app = typer.Typer(no_args_is_help=True)


# remove when adding the proper subcommands
@app.callback("template")
def template():
    print("[violet]TODO: Implement [bold white]draft "
      "templates[/bold white][/violet].")

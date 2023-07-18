import typer
from rich import print

from draft.debug.Debugger import Debugger
from tests.common.test_common_Configuration import Configuration

app = typer.Typer()


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    Debugger(Configuration()).run()

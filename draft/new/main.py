from pathlib import Path

import typer
from rich import print

from draft.common.TemplateManager import TemplateManager
from draft.new.Subcommands import Subcommands
from tests.common.test_common_Configuration import Configuration

app = typer.Typer()

configuration = Configuration(
    main=Path("~/.config/draft/"),
    root=Path.home(),
    cwd=Path.cwd(),
    # header="exam.tex",
)

subcommands = Subcommands(
    configuration,
    TemplateManager(configuration),
)

subcommands.add_subcommands(app)


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        if configuration.header is not None:
            print("#TODO: Compiling document for `%s`." % configuration.header.name)
        else:
            ctx.get_help()

from pathlib import Path

import typer

from draft.common.Configuration import Configuration
from draft.common.TemplateManager import TemplateManager
from draft.new.Subcommands import Subcommands

app = typer.Typer(no_args_is_help=True)

configuration = Configuration(
    main=Path("config.draft/draftrc"),  # main=Path("~/.config/draft/"),
    root=Path.cwd(),  # Path.home(),
    cwd=Path.cwd(),
)

Subcommands(
    app,
    configuration,
    TemplateManager(configuration),
)

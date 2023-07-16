from pathlib import Path

import typer

from draft.common.Prompt import Checkbox, List
from draft.common.Prompter import Prompter
from draft.common.TemplateManager import TemplateManager
from draft.configuration.Configuration import Configuration
from draft.new.Compiler import Compiler
from draft.new.Subcommands import Subcommands

app = typer.Typer()

configuration = Configuration(
    main=Path("config.draft/draftrc"),  # main=Path("~/.config/draft/"),
    root=Path.cwd(),  # Path.home(),
    cwd=Path.cwd(),
    # test
    header="exam",
)

subcommands = Subcommands(
    configuration,
    TemplateManager(configuration),
)

subcommands.add_subcommands(app)


@app.callback(invoke_without_command=True)
def main():
    if "header" in configuration:
        # add ending .tex
        if not configuration["header"].endswith(".tex"):
            configuration["header"] = configuration["header"] + ".tex"

        # check that its a valid path else remove it
        if not (Path(configuration.headers) / configuration["header"]).is_file():
            configuration.pop("header", None)
    else:
        p = Prompter(configuration)
        p.ask(
            List(
                "header",
                choices=[file.name for file in configuration.headers.iterdir()],
                message="Which header should be used?",
            )
        )

    c = Compiler(configuration)
    c.compile()

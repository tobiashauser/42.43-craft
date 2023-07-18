import collections.abc

import typer

collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import prompt
from rich import print as rprint
from typing_extensions import Annotated

from draft.common.helpers import fetch_github_directory
from draft.common.Prompt import Confirm
from draft.templates.TemplateManager import TemplateManager
from tests.common.test_common_Configuration import Configuration

app = typer.Typer(no_args_is_help=True)

configuration = Configuration()
templates_manager = TemplateManager(configuration)


@app.command(name="path", help="Reveal the location of the templates folder.")
def path():
    print(templates_manager.folder.path)


@app.command(name="open", help="Open the directory of the templates.")
def open():
    templates_manager.folder.open()


@app.command(name="list", help="List the available templates.")
def list_function():
    rprint("[blue]==>[/blue] [bold white]Preambles")
    print("\n".join([p.name for p in templates_manager.preambles]))

    print("")
    rprint("[blue]==>[/blue] [bold white]Headers")
    print("\n".join([h.name for h in templates_manager.headers]))

    print("")
    rprint("[blue]==>[/blue] [bold white]Exercises")
    print("\n".join([e.name for e in templates_manager.exercises]))


@app.command(name="fetch", help="Fetch templates from GitHub")
def fetch(
    verbose: Annotated[
        bool, typer.Option(help="Don't overwrite any local templates.")
    ] = True
):
    print("Fetching templates from GitHub...")

    owner = "tobiashauser"
    repo = "42.43-draft"
    path = "config.draft/"

    preambles = fetch_github_directory(owner, repo, path + "preambles/")
    headers = fetch_github_directory(owner, repo, path + "headers/")
    exercises = fetch_github_directory(owner, repo, path + "exercises")

    def resolve_templates(dict, type, creator, path):
        for name, contents in dict.items():
            match = False
            for file in path.iterdir():
                if file.name == name:
                    match = True

            if not match:
                creator(name, contents)
                rprint("[blue]==>[/blue] [bold white]Created '%s' :sparkles:" % name)
            else:
                if verbose:
                    question = Confirm(
                        "confirmation",
                        message="A %s called '%s' already exists in your templates. Do you want to overwrite it with the version from GitHub?"
                        % (type, name),
                        default=False,
                    )
                    answer = prompt(question).get("confirmation", False)
                    if answer:
                        creator(name, contents)
                        rprint(
                            "[blue]==>[/blue] [bold white]Overwritten '%s' :sparkles:"
                            % name
                        )

    # Preambles
    if preambles is not None:
        print("")
        resolve_templates(
            preambles,
            "preamble",
            templates_manager.new_preamble,
            templates_manager.preambles_path,
        )

    # Headers
    if headers is not None:
        print("")
        resolve_templates(
            headers,
            "header",
            templates_manager.new_header,
            templates_manager.headers_path,
        )

    # Exercises
    if exercises is not None:
        print("")
        resolve_templates(
            exercises,
            "exercise",
            templates_manager.new_exercise,
            templates_manager.exercises_path,
        )

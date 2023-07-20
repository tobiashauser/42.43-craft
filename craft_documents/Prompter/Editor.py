import collections.abc
from typing import Callable

from craft_documents.Prompter.Prompt import Answers, Prompt

# Patch bug, caused by change in the collections package since python 3.10 (?)
collections.Mapping = collections.abc.Mapping  # type: ignore
from PyInquirer import Validator


class Editor(Prompt):
    """
    An editor prompt:
    https://github.com/CITGuru/PyInquirer/blob/master/examples/editor.py

    Take `type`, `name`, `message`[, `default`, `filter`, `validate`, `eargs`]
    properties.

    ### Editor Arguments - `eargs`
    Opens an empty or edits the default text in the defined editor.
    If an editor is given (should be the full path to the executable
    but the regular operating system search path is used for finding
    the executable) it overrides the detected editor.
    Optionally, some environment variables can be used. If the editor
    is closed without changes, None is returned. In case a file is
    edited directly the return value is always None and `save` and `ext`
    are ignored.

    Takes:

    - `editor`: accepts default to get the default platform editor.
        But you can also provide the path to an editor e.g vi.
    - `ext`: the extension to tell the editor about. This defaults
        to .txt but changing this might change syntax highlighting e.g ".py"
    - `save`: accepts True or False to determine to save a file.
    - `filename`: accepts the path of a file you'd like to edit.
    - `env`: accepts any given environment variables to pass to the editor

    Launches an instance of the users preferred editor on a temporary file.
    Once the user exits their editor, the contents of the temporary file
    are read in as the result. The editor to use is determined by reading
    the `VISUAL` or `EDITOR` environment variables. If neither of
    those are present, `notepad` (on Windows) or `vim` (Linux or Mac) is used.
    """

    class Eargs(dict):
        def __init__(
            self,
            editor: str | None = None,
            ext: str | None = None,
            save: bool | None = None,
            filename: str | None = None,
            env: list[str] | None = None,
        ):
            if editor is not None:
                self["editor"] = editor
            if ext is not None:
                self["ext"] = ext
            if save is not None:
                self["save"] = save
            if filename is not None:
                self["filename"] = filename
            if env is not None:
                self["env"] = env

    def __init__(
        self,
        name: str,
        message: str | None = None,
        default: str | Callable[[Answers], str] | None = None,
        filter: Callable[[str], str] | None = None,
        when: Callable[[Answers], bool] | bool = True,
        validate: Callable[[str], bool | str] | Validator | None = None,
        eargs: Eargs | None = None,
    ):
        super().__init__(Prompt.Type.editor, name, message, when)

        if default is not None:
            self["default"] = default
        if filter is not None:
            self["filter"] = filter
        if validate is not None:
            self["validate"] = validate
        if eargs is not None:
            self["eargs"] = eargs

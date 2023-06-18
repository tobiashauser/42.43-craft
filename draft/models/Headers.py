from pathlib import Path
from rich import print
from typer import Abort
from typing import List, Dict


class Headers:
    """
    A class encapsulating the headers directory in the configuration.
    """

    def __init__(self, path: Path):
        self.path = path
        self.validate()

        headers: List[Header] = []
        for file in self.path.iterdir():
            if file.is_file() and file.suffix == '.tex':
                try:
                    headers.append(Header(file))
                except:
                    pass
        self.headers = headers

    def validate(self):
        # - directory exists
        if not self.path.is_dir():
            self.path.mkdir(parents=True, exist_ok=True)

        # directory is not empty
        if not any(self.path.iterdir()):
            print("Creating default headers...")
            for name, contents in self.defaults.items():
                with (self.path / (name + '.tex')).open('w') as file:
                    file.write(contents)

    defaults: Dict[str, str] = {
        'exam': r"""
\usepackage{scrlayer-scrpage}

% EXAM
% |-------------------------------------------------------------------------|
% | **Klausur**               Name: _____                    Hörerziehung-2 |
% | (Gruppe 1)                                        Stuttgart • SoSe 2023 |
% |-------------------------------------------------------------------------|

\ihead*{\textbf{<<semantic_name>>}\\(<<group>>)}
\chead*{Name:_\rule{0.4\linewidth}{0.4pt}}
\ohead*{\textbf{<<course>>}\\<<place>> • <<semester>>}
""",
        'worksheet': r"""
\usepackage{scrlayer-scrpage}

% WORKSHEET
% |-------------------------------------------------------------------------|
% | HE 2 • SoSe 2023           Beethoven: Ariet...           TH • Stuttgart |
% |-------------------------------------------------------------------------|

\ihead*{<<course>> • <<semester>>}
\chead*{<<topic>>}
\ohead*{<<author>> • <<place>>}
""",
    }


class Header:
    """
    A class representing one header file in the templates' directory.
    """

    def __init__(self, path: Path):
        self.path = path
        self.validate()

    def validate(self):
        # - is file
        # - file is not empty
        if (not self.path.is_file()) \
                or self.path.stat().st_size == 0:
            print("[red]TODO: Faulty header template.[/red]")
            raise Abort()

    def load(self):
        """
        Load the header from the disk.
        """

        with self.path.open('r') as file:
            self.contents = file.read()

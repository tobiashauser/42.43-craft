from Exercises import Exercises
from Headers import Headers
from pathlib import Path
from Preamble import Preamble


class Configuration:
    """
    A class representing draft's configuration on the system.

    This class provides access to the templates and validates the
    configuration upon initialization.
    """

    # The base directory of the configuration
    basedir: Path = Path("config/draft/")  # Path.home() / ".config/draft/"

    # The templates' directory
    templates: Path = basedir / "templates/"

    # The preamble
    preamble: Preamble = Preamble(templates / "preamble.tex")

    # The headers
    headers: Headers = Headers(templates / "headers/")

    # The exercises
    exercises: Exercises = Exercises(templates / "exercises/")

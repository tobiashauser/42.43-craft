from draft.common.Header import Header
from draft.common.Preamble import Preamble
from draft.configuration.Configuration import Configuration


class Compiler:
    """
    Class that handles compiling a document.
    """

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    @property
    def preamble(self) -> Preamble:
        return self._preamble

    @property
    def header(self) -> Header:
        return self._header

    def __init__(self, configuration: Configuration):
        """
        You should guarantee values for `preamble` and `header` in the
        configuration when creating an instance of a Compiler.
        """

        self._configuration = configuration
        self._preamble = Preamble(configuration.preamble, configuration)

        if configuration.header is not None:
            self._header = Header(configuration.header, configuration)
        else:
            raise Exception("Unexpectedly found `None` at `configuration.header`.")
            # TODO: Handle Exception

from ..models.headers import Header


class Document:
    """
    A class representing the document created by draft.
    """

    def __init__(self, header: Header):
        self.header = header

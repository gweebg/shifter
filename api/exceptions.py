class InvalidParameter(TypeError):
    """
    Custom exception for invalid parameters.
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ParsingError(Exception):
    """
    Custom exception for parsing errors.
    """
    pass

class RecipeParseError(Exception):
    def __init__( self, line = None, line_nr = None):
        super().__init__()
        self.line = line
        self.line_nr = line_nr

    def __str__(self):
        if self.__cause__ is None:
            return 'Error: on line #{} ({!r}): invalid'.format(
                self.line_nr,
                self.line,
                )
        else:
            return 'Error: on line #{} ({!r}):\n{!s}'.format(
                self.line_nr,
                self.line,
                self.__cause__,
                )

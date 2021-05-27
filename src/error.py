class PCLError(Exception):
    pass


class PCLWarning(Warning):
    pass


class PCLCError(PCLError):
    pass


class PCLLexerError(PCLError):
    pass


class PCLParserError(PCLError):
    pass


class PCLSymbolTableError(PCLError):
    pass


class PCL2IRError(PCLError):
    pass

class LLMGenerationError(Exception):
    pass


class DatabaseError(Exception):
    pass


class PostgreSQLDatabaseError(DatabaseError):
    pass


class FileExportError(Exception):
    pass


class PromptSQLError(Exception):
    pass

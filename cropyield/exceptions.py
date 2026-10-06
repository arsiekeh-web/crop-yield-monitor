# cropyield/exceptions.py
"""Custom errors, so the app can explain problems in plain language."""


class CropYieldError(Exception):
    """Base error for this app."""


class StorageError(CropYieldError):
    """Raised when records can't be saved or loaded."""


class DuplicateRecordError(CropYieldError):
    """Raised when a record ID already exists."""


class RecordNotFoundError(CropYieldError):
    """Raised when a record ID does not exist."""

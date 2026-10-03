# cropyield/exceptions.py
class CropYieldError(Exception):
    """Base error for this app."""

class DuplicateRecordError(CropYieldError):
    pass

class RecordNotFoundError(CropYieldError):
    pass
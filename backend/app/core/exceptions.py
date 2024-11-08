from fastapi import HTTPException, status

class DocumentNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

class InvalidFileTypeError(HTTPException):
    def __init__(self, allowed_types: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )

class FileSizeTooLargeError(HTTPException):
    def __init__(self, max_size: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of {max_size/1024/1024}MB"
        )

class ModelNotFoundError(HTTPException):
    def __init__(self, model_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {model_name} not found"
        )

class UnauthorizedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

class ModelGenerationError(Exception):
    """Exception raised when there's an error generating a model response."""
    pass

class ServiceUnavailableError(Exception):
    """Exception raised when a service is temporarily unavailable."""
    pass 
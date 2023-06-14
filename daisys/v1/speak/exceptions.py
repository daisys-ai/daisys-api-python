from typing import Union
from .models import TakeResponse

class DaisysError(RuntimeError):
    pass

class DaisysGenerateError(DaisysError):
    def __init__(self, message: str, response: Union[TakeResponse, list[TakeResponse]]):
        super().__init__(message)
        self.response = response

class DaisysTakeGenerateError(DaisysGenerateError):
    pass

class DaisysVoiceGenerateError(DaisysGenerateError):
    pass

class DaisysDeletionError(DaisysError):
    pass

class DaisysUpdateError(DaisysError):
    pass

class DaisysTakeDeletionError(DaisysDeletionError):
    pass

class DaisysVoiceDeletionError(DaisysDeletionError):
    pass

class DaisysVoiceUpdateError(DaisysUpdateError):
    pass

class DaisysCredentialsError(DaisysError):
    def __init__(self, message: str='Insufficient credentials provided.'):
        super().__init__(message)

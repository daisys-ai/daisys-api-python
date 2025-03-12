__all__ = [ 'DaisysError', 'DaisysGenerateError', 'DaisysTakeGenerateError',
            'DaisysVoiceGenerateError', 'DaisysDeletionError', 'DaisysUpdateError',
            'DaisysTakeDeletionError', 'DaisysVoiceDeletionError', 'DaisysVoiceUpdateError',
            'DaisysCredentialsError', 'DaisysWebsocketError', 'DaisysWebsocketConnectError',
            'DaisysWebsocketStreamError', 'DaisysWebsocketGenerateError']

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

class DaisysWebsocketError(DaisysError):
    pass

class DaisysWebsocketConnectError(DaisysWebsocketError):
    pass

class DaisysWebsocketStreamError(DaisysWebsocketError):
    def __init__(self, message: str, request_id: Union[int,str,None]=None):
        super().__init__(message + ((f' for {request_id=}') if request_id is not None else ''))
        self.request_id = request_id

class DaisysWebsocketGenerateError(DaisysWebsocketError):
    def __init__(self, message: str, request_id: Union[int,str]):
        super().__init__(message + f', {request_id=}')
        self.request_id = request_id

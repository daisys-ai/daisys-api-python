__all__ = ['DaisysSyncSpeakWebsocketV1']

from typing import Union, Callable, Awaitable, Optional
import time
import json
import queue
import contextlib

import httpx
try:
    import httpx_ws
    import wsproto
except:
    # If websockets are not supported, classes in this module will not be used.
    pass

from .models import *
from .exceptions import (DaisysWebsocketError, DaisysWebsocketConnectError,
                         DaisysWebsocketStreamError, DaisysWebsocketGenerateError)


class DaisysSyncAudioStream:
    def __init__(self, request_id: int, take_id: str,
                 status_callback: Callable[[int, TakeResponse], None],
                 audio_callback: Callable[[int, str, int, Optional[int], Optional[bytes]], None]):
        self.request_id = request_id
        self.take_id = take_id
        self.status_callback = status_callback
        self.audio_callback = audio_callback
        self.parts = {}
        self.current_part = 0
        self.current_chunk = 0
        self.done = False

    def receive_status(self, take: Optional[TakeResponse]=None, voice: Optional[VoiceInfo]=None):
        if self.status_callback is None:
            return
        if take:
            self.status_callback(self.request_id, take)
        elif voice:
            self.status_callback(self.request_id, voice)
        else:
            self.status_callback(self.request_id)

    def receive_chunk(self, part_id: int, chunk_id: Optional[int], audio: bytes):
        # Store the audio using a tuple (part_id, chunk_id) as the key
        self.parts[(part_id, chunk_id)] = audio

        # Detect non-chunking mode
        if chunk_id is None:
            self.current_chunk = None

        # Process and send chunks in order
        while (self.current_part, self.current_chunk) in self.parts:
            audio_chunk = self.parts[(self.current_part, self.current_chunk)]

            if self.audio_callback:
                self.audio_callback(
                    request_id=self.request_id,
                    take_id=self.take_id,
                    part_id=self.current_part,
                    chunk_id=self.current_chunk,
                    audio=audio_chunk,
                )

            # Clear the buffer up to the current position
            del self.parts[(self.current_part, self.current_chunk)]

            # If audio_chunk is None, the part is fully processed
            if audio_chunk is None:
                if self.current_chunk in [0, None]:
                    self.done = True
                else:
                    self.current_chunk = 0
                    self.current_part += 1
            elif self.current_chunk is not None:
                self.current_chunk += 1
            else:
                self.current_part += 1

class DaisysSyncSpeakWebsocketV1:
    """Wrapper for Daisys v1 API websocket connection, synchronous version.

    This class is intended to be used in a ``with`` clause.
    """

    def __init__(self, client: 'DaisysSyncSpeakClientV1', model: str):
        self.client = client
        self.model = model
        self.ws = None
        self.connection = None
        self.current_request_id = None
        self.request_streams = None

    def __enter__(self):
        self.reconnect()
        return self

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def disconnect(self):
        """Disconnect this websocket."""
        if self.connection:
            try:
                next(self.connection)
            except StopIteration:
                pass
            self.connection = None
            self.ws = None

    def reconnect(self):
        """Reconnect this websocket, by first fetching the URL and then opening the conneciton to it."""
        self.disconnect()
        result = self.client._http('websocket/' + self.model)
        if not result:
            raise DaisysWebsocketConnectError()
        def make_connection():
            with httpx_ws.connect_ws(result['worker_websocket_url'], self.client.httpx_client) as ws:
                yield ws
        self.connection = make_connection()
        self.ws = next(self.connection)
        self.current_request_id = 0
        self.request_streams = {}
        self.take_parts = {}

    def generate_take(self,
                      voice_id: str,
                      text: str,
                      override_language: Optional[str]=None,
                      style: Optional[list[str]]=None,
                      prosody: Optional[ProsodyFeaturesUnion]=None,
                      stream_options: Optional[StreamOptions]=None,
                      status_webhook: Optional[str]=None,
                      done_webhook: Optional[str]=None,
                      status_callback: Optional[Callable[[int, TakeResponse], None]]=None,
                      audio_callback: Optional[Callable[[int, str, int, Optional[int], Optional[bytes]], None]]=None,
                      timeout: Optional[float]=None) -> int:
        """Generate a "take", an audio file containing an utterance of the given text by
        the given voice.

        Args:
            voice_id: The id of the voice to be used for generating audio.  The voice is
                      attached to a specific model.

            text: The text that the voice should say.

            override_language: Normally a language classifier is used to detect the language
                               of the speech; this allows for multilingual sentences.
                               However, if the language should be enforced, it should be
                               provided here.  Currently accepted values are "nl-NL" and
                               "en-GB".

            style: A list of styles to enable when speaking.  Note that most styles are
                   mutually exclusive, so a list of 1 value should be provided.  Accepted
                   styles can be retrieved from the associated voice's VoiceInfo.styles
                   or the model's TTSModel.styles field.  Note that not all models
                   support styles, thus this can be left empty if specific styles are not
                   desired.

            prosody: The characteristics of the desired speech not determined by the voice or
                     style.  Here you can provide a SimpleProsody or most models also accept
                     the more detailed AffectProsody.

            stream_options: Configuration for streaming.

            status_webhook: An optional URL to be called using ``POST`` whenever the take's
                            status changes, with :class:`TakeResponse` in the body content.

            done_webhook: An optional URL to be called exactly once using ``POST`` when the
                          take is ``READY``, ``ERROR``, or ``TIMEOUT``, with
                          :class:`TakeResponse` in the body content.

            status_callback: An optional function to call for status updates regarding this take.

            audio_callback: An optional function to call to provide the audio parts of the take.

        Returns:
            TakeResponse: Information about the take being generated, including status.

        """
        params = TakeGenerate(voice_id=voice_id, text=text,
                              override_language=override_language,
                              style=style, prosody=prosody,
                              status_webhook=Webhook(post_url=status_webhook) if status_webhook else None,
                              done_webhook=Webhook(post_url=done_webhook) if done_webhook else None)
        stream = f'"stream":{stream_options.model_dump_json()},' if stream_options else ''
        self.ws.send_text('{"command":"/takes/generate",'
                          f'"request_id":{self.current_request_id},'
                          f'{stream}'
                          f'"data":{params.model_dump_json(exclude_defaults=True)}}}')
        self.request_streams[self.current_request_id] = DaisysSyncAudioStream(
            request_id=self.current_request_id,
            take_id=None,
            status_callback=status_callback,
            audio_callback=audio_callback
        )
        self.current_request_id += 1
        return self.current_request_id - 1

    def generate_voice(self,
                       name: str,
                       model: str,
                       gender: VoiceGender,
                       description: Optional[str]=None,
                       default_style: Optional[list[str]]=None,
                       default_prosody: Optional[ProsodyFeaturesUnion]=None,
                       stream_options: Optional[StreamOptions]=None,
                       done_webhook: Optional[str]=None,
                       status_callback: Optional[Callable[[int, TakeResponse], None]]=None,
                       audio_callback: Optional[Callable[[int, str, int, Optional[int], Optional[bytes]], None]]=None,
                       ) -> int:
        """Generate a random, novel voice for a given model with desired properties.

        Args:
            name: A name to give the voice, may be any string, and does not need to be unique.
            model: The name of the model for this voice.
            gender: The gender of this voice.
            description: The description of this voice.
            default_style: An optional list of styles to associate with this voice by
                           default.  It can be overriden by a take that uses this voice.
                           Note that most styles are mutually exclusive, and not all
                           models support styles.
            default_prosody: An optional default prosody to associate with this voice.  It
                             can be overridden by a take that uses this voice.
            stream_options: Configuration for streaming.
            done_webhook: An optional URL to call exactly once using POST when the voice
                          is available, with VoiceInfo in the body content.

            status_callback: An optional function to call for status updates regarding this take.

            audio_callback: An optional function to call to provide the audio parts of the take.

        Returns:
            VoiceInfo: Information about the generated voice.

        """
        params = VoiceGenerate(name=name, model=model, gender=gender,
                               description=description,
                               default_style=default_style,
                               default_prosody=default_prosody, done_webhook=Webhook(post_url=done_webhook) if done_webhook else None)
        if stream_options is None:
            stream_options = StreamOptions(mode=StreamMode.CHUNKS)
        self.ws.send_text('{"command":"/voices/generate",'
                          f'"request_id":{self.current_request_id},'
                          f'"stream":{stream_options.model_dump_json()},'
                          f'"data":{params.model_dump_json(exclude_defaults=True)}}}')
        self.request_streams[self.current_request_id] = DaisysSyncAudioStream(
            request_id=self.current_request_id,
            take_id=None,
            status_callback=status_callback,
            audio_callback=audio_callback,
        )
        self.current_request_id += 1
        return self.current_request_id - 1

    def update(self, timeout: Optional[int]=1):
        """Retrieve a waiting message on the open websocket connection.

        Args:
            timeout: Number of seconds to wait. Can be 0 if non-blocking usage is desired.
                     If None, wait forever.
        """
        try:
            msg = self.ws.receive(timeout=timeout)
        except queue.Empty:
            return
        except httpx_ws.WebSocketDisconnect:
            self.reconnect()
            return
        if isinstance(msg, wsproto.events.TextMessage):
            try:
                data = json.loads(msg.data)
            except json.decoder.JSONDecodeError:
                raise DaisysWebsocketStreamError("Bad status message, JSONDecodeError")
            if data.get('status') == 'error':
                if 'request_id' in data:
                    raise DaisysWebsocketGenerateError(data["message"], request_id=data["request_id"])
                else:
                    raise DaisysWebsocketStreamError(data['message'])
            elif 'status' in data:
                return # TODO

            stream = self.request_streams.get(data['request_id'])
            if stream is None:
                raise DaisysWebsocketStreamError("Received response for unknown request_id",
                                                 request_id=data.get("request_id"))
            if 'example_take_id' in data['data']:
                if stream.take_id is None:
                    stream.take_id = data['data']['example_take_id']
                stream.receive_status(voice=VoiceInfo(**data['data']))
            else:
                if stream.take_id is None:
                    stream.take_id = data['data']['take_id']
                stream.receive_status(take=TakeResponse(**data['data']))
        elif isinstance(msg, wsproto.events.BytesMessage):
            if msg.data[:4] == b'JSON':
                json_length = int.from_bytes(msg.data[4:8], 'little')
                try:
                    data = json.loads(msg.data[8:8+json_length].decode('utf8'))
                except json.decoder.JSONDecodeError:
                    raise DaisysWebsocketStreamError("Bad bytes stream metadata, JSONDecodeError")
                audio = msg.data[8+json_length:]
                cid = data.get('chunk_id')
                if (len(audio) == 0
                    or cid in [0, None] and audio[:4] == b'RIFF' and audio[8:12] == b'WAVE'
                    or cid > 0):
                    if len(audio) == 0:
                        audio = None
                    stream = self.request_streams.get(data['request_id'])
                    if stream is None:
                        # TODO: keep these for some limited time in case of the
                        # unlikely event that the audio arrives before first status
                        raise DaisysWebsocketStreamError(message="Unknown request",
                                                         request_id=data["request_id"])
                    stream.receive_chunk(data['part_id'], data.get('chunk_id'), audio)
                else:
                    raise DaisysWebsocketStreamError(message="Bad bytes stream audio format",
                                                     request_id=data["request_id"])
            else:
                raise DaisysWebsocketStreamError(message="Bad bytes stream metadata",
                                                 request_id=data["request_id"])

    def iter_request(self, request_id):
        """Iterate over incoming text and audio messages for a given request_id.

        Args:
            request_id: The id value associated with the request to be iterated over.
                        Returned by :meth:`.take_generate` and :meth:`.voice_generate`.

        Returns:
            An Iterator yielding tuples (``take_id``, ``take``, ``header``,
            ``audio``), where:

            * ``take_id``: the take_id associated with this request
            * ``take``: the TakeResponse information if a text message, otherwise None
            * ``header``: the wav header if any, otherwise None
            * ``audio``: the audio bytes, if a binary message, otherwise None

        """
        stream = self.request_streams.get(request_id)
        if stream is None:
            raise DaisysWebsocketStreamError(request_id=f'{request_id=} (unknown)')
        q = queue.Queue()
        s = stream.status_callback
        a = stream.audio_callback
        def status_cb(request_id: int, take: TakeResponse):
            q.put(((take.take_id, take, None, None), False, False))
            if take.status.done():
                q.put((None, True, False))
            if s is not None:
                s(request_id, take)
        def audio_cb(request_id: int, take_id: str, part_id: int, chunk_id: Optional[int],
                     audio: Optional[bytes]):
            header = None
            if chunk_id in [0, None]:
                if audio is None:
                    q.put((None, False, True))
                else:
                    pos = 12
                    section = audio[pos:pos+4]
                    while section != b'data':
                        length = int.from_bytes(audio[pos+4:pos+8], 'little')
                        pos += length + 8
                        section = audio[pos:pos+4]
                    header = audio[:pos+8]
                    audio = audio[pos+8:]
            q.put(((take_id, None, header, audio), False, False))
            if a is not None:
                a(request_id, take_id, part_id, chunk_id, audio)
        stream.status_callback = status_cb
        stream.audio_callback = audio_cb
        done1, done2 = False, False
        while (done1, done2) != (True, True):
            self.update(timeout=1)
            try:
                item, d1, d2 = q.get(block=False)
            except queue.Empty:
                continue
            if item:
                yield item
            done1, done2 = done1 or d1, done2 or d2

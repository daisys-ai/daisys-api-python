"""Pydantic classes representing the JSON interface for the Daisys API."""

__all__ = ['Status', 'VoiceGender', 'Version', 'ProsodyFeatures', 'SimpleProsody',
           'AffectProsody', 'SignalProsody', 'ProsodyFeaturesUnion', 'ProsodyType',
           'TakeGenerate', 'TakeGenerateWithoutVoice', 'TakeInfo', 'TakeResponse',
           'VoiceGenerate', 'VoiceInfo', 'VoiceUpdate', 'TTSModel', 'Webhook',
           'StreamOptions', 'StreamMode']

import enum
import json
import warnings
from typing import Optional, Union
from pydantic import BaseModel

class Status(str, enum.Enum):
    """Represents the status of a take or voice generation process.

    Attributes:
        WAITING: Item is waiting to be processed.
        STARTED: Processing has started for this item.
        PROGRESS_25: Item has been 25% processed.
        PROGRESS_50: Item has been 50% procesesd.
        PROGRESS_75: Item has been 75% procesesd.
        READY: Item is ready to be used; for takes, audio is available.
        ERROR: An error occurred during processing of this item.
        TIMEOUT: Processing did not finish for this item.

    Note that ``TIMEOUT`` is used for very long intervals; it does not indicate a few
    seconds or minutes, but rather that an item has been in the queue for more than a day
    and has therefore been removed.  It should only be considered to represent
    circumstances where processing errors were not detected by normal means.

    """
    WAITING = 'waiting'
    STARTED = 'started'
    PROGRESS_25 = 'progress_25'
    PROGRESS_50 = 'progress_50'
    PROGRESS_75 = 'progress_75'
    READY = 'ready'
    ERROR = 'error'
    TIMEOUT = 'timeout'

    def done(self) -> bool:
        return self in [Status.READY, Status.ERROR, Status.TIMEOUT]

    def ready(self) -> bool:
        return self == Status.READY

    def error(self) -> bool:
        return self in [Status.ERROR, Status.TIMEOUT]

    def started(self) -> bool:
        return self != Status.WAITING

    def waiting_or_in_progress(self) -> bool:
        return self in [Status.WAITING, Status.STARTED, Status.PROGRESS_25,
                        Status.PROGRESS_50, Status.PROGRESS_75]

    def in_progress(self) -> bool:
        return self in [Status.STARTED, Status.PROGRESS_25,
                        Status.PROGRESS_50, Status.PROGRESS_75]

class VoiceGender(str, enum.Enum):
    """Represents the gender of a voice.

    Note: upper case in Python, lower case in JSON.

    Values:
      MALE, FEMALE, NONBINARY
    """
    MALE = 'male'
    FEMALE = 'female'
    NONBINARY = 'nonbinary'

class VoiceInputType(str, enum.Enum):
    """Represents the input that a model understands for voice generation.

    Note: upper case in Python, lower case in JSON.

    Values:
      GENDER, DESCRIPTION
    """
    GENDER = 'gender'
    DESCRIPTION = 'description'

class Version(BaseModel):
    """Represents the version of the API.

    Attributes:
        version: The major version number of the API.
        minor: The minor version number of the API.
    """
    version: int
    minor: int

class ProsodyFeatures(BaseModel):
    """Base prosody features supported by all models.

    Attributes:
        pitch: The normalized pitch; -10 to 10, where 0 is a neutral pitch.
        pace: The normalized pace; -10 to 10, where 0 is a neutral pace.
    """
    pitch: int
    pace: int

class SimpleProsody(ProsodyFeatures):
    """Simplified prosody features, supported by all models.  See also parent class
    :class:`ProsodyFeatures` for other fields.

    Attributes:
        expression: The normalized "expression"; -10 to 10, where 0 is neutral.

    """
    expression: int

class AffectProsody(ProsodyFeatures):
    """Prosody features based on analysis of affect.  See also parent class
    :class:`ProsodyFeatures` for other fields.

    Attributes:
        valence: The valence; -10 for negativity, 10 for positivity, 0 for neutral.
        arousal: The arousal; -10 for unexcited, 10 for very excited, 0 for neutral.
        dominance: The dominance; -10 for docile, 10 for commanding, 0 for neutral.

    """
    valence: int
    dominance: int
    arousal: int

class SignalProsody(ProsodyFeatures):
    """Prosody features based on signal analysis.
    See also parent class ProsodyFeatures for other fields.

    Attributes:
        tilt: The normalized spectral tilt; -10 for flat, 10 for bright, 0 for neutral.
        pitch_range: The normalized pitch range; -10 for flat, 10 for highly varied pitch, 0 for neutral.
    """
    tilt: int
    pitch_range: int

ProsodyFeaturesUnion = Union[SimpleProsody, AffectProsody, SignalProsody]
"""A union type representing different prosody feature variations."""

class ProsodyType(str, enum.Enum):
    """An enum representing different prosody feature types.

    Not all models accept all prosody types.  See the prosody_types field of :class:`TTSModel`.

    Attributes:
        SIMPLE: corresponds with SimpleProsody
        AFFECT: corresponds with AffectProsody
        SIGNAL: corresponds with SignalProsody

    """
    SIMPLE = 'simple'
    AFFECT = 'affect'
    SIGNAL = 'signal'

    def prosody(self, **kwargs):
        """Return a prosody object corresponding to this value, initialized with the given
        arguments."""
        return {
            ProsodyType.SIMPLE: SimpleProsody,
            ProsodyType.AFFECT: AffectProsody,
            ProsodyType.SIGNAL: SignalProsody,
        }[self](**kwargs)

    @staticmethod
    def from_class(prosody: ProsodyFeaturesUnion):
        """Return an enum value based on the prosody class provided.

        Args:
            prosody: The prosody object from which to derive the enum value.
        """
        if isinstance(prosody, SimpleProsody):
            return ProsodyType.SIMPLE
        if isinstance(prosody, AffectProsody):
            return ProsodyType.AFFECT
        if isinstance(prosody, SignalProsody):
            return ProsodyType.SIGNAL

class Webhook(BaseModel):
    """Store information about a registered webhook and its status.

    When specifying a webhook, only ``url`` needs to be provided.

    Attributes:
        post_url: The URL to be called with POST.
        timestamp_ms: The time it was last called at, milliseconds since epoch.
        status_code: The HTTP status code of the last response from the webhook.
    """
    post_url: str
    timestamp_ms: Optional[int] = None
    status_code: Optional[int] = None

class TakeGenerateWithoutVoice(BaseModel):
    """Parameters necessary to generate a "take", an audio file containing an utterance of
    the given text.  No voice is provided here, for the purpose of embedding in
    :class:`VoiceGenerate` for the voice example.

    Attributes:
        text: The text that the voice should say.
        override_language: Normally a language classifier is used to detect the language
                           of the speech; this allows for multilingual sentences.
                           However, if the language should be enforced, it should be
                           provided here.  Currently accepted values are "nl-NL" and
                           "en-GB".
        style: A list of styles to enable when speaking.  Note that most styles are
               mutually exclusive, so a list of 1 value should be provided.  Accepted
               styles can be retrieved from the associated voice's
               :class:`VoiceInfo.styles` or the model's :class:`TTSModel.styles` field.
               Note that not all models support styles, thus this can be left empty if
               specific styles are not desired.
        prosody: The characteristics of the desired speech not determined by the voice or
                 style.  Here you can provide a :class:`SimpleProsody` or most models also
                 accept the more detailed :class:`AffectProsody`.
        status_webhook: An optional URL to be called using ``POST`` whenever the take's
                        status changes, with :class:`TakeResponse` in the body content.
        done_webhook: An optional URL to be called exactly once using ``POST`` when the
                      take is ``READY``, ``ERROR``, or ``TIMEOUT``, with
                      :class:`TakeResponse` in the body content.

    """
    text: str
    override_language: Optional[str] = None
    style: Optional[list[str]] = None
    prosody: Optional[ProsodyFeaturesUnion] = None
    status_webhook: Optional[Webhook] = None
    done_webhook: Optional[Webhook] = None

class TakeGenerate(TakeGenerateWithoutVoice):
    """Parameters necessary to generate a "take", an audio file containing an utterance of
    the given text by the given voice.  See :class:`TakeGenerateWithoutVoice` for
    documentation on the remaining fields.

    Attributes:
        voice_id: The id of the voice to be used for generating audio.  The voice is
                  attached to a specific model.

    """
    voice_id: str

class TakeInfo(BaseModel):
    """Some information available when a take is ``READY``, attached to the
    :class:`TakeResponse`.

    Attributes:

        duration: The length of the audio in samples.  To get the length in seconds,
                  divide by audio_rate.
        audio_rate: The number of samples per second in the audio.
        normalized_text: The text used for text-to-speech after normalization,
                         ie. translated from "as written" to "as spoken".  Provided as a
                         list of sentences.

    """
    duration: int
    audio_rate: int
    normalized_text: list[str]

class TakeResponse(TakeGenerate):
    """Information about a take, returned during and after take generation.  Also includes
    fields from :class:`TakeGenerate`.

    Attributes:
        take_id: The unique identifier of this take.
        status: The status of this take, whether it is ready, in error, or in progress.
        timestamp_ms: The timestamp that this take generation was requested, in
                      milliseconds since epoch.
        info: Information available when the take is ``READY``, see :class:`TakeInfo`.

    """
    take_id: str
    status: Status
    timestamp_ms: int
    info: Optional[TakeInfo] = None

class VoiceGenerate(BaseModel):
    """Parameters necessary to generate a voice.

    Attributes:
        name: A name to give the voice, may be any string, and does not need to be unique.
        model: The name of the model for this voice.  Refers to the ``name`` entry in :class:`TTSModel`.
        gender: The gender of this voice.
        description: A description of this voice.
        default_style: An optional list of styles to associate with this voice by default.
                       It can be overriden by a take that uses this voice.  Note that
                       most styles are mutually exclusive, and not all models support
                       styles.
        default_prosody: An optional default prosody to associate with this voice.  It can
                         be overridden by a take that uses this voice.
        example_take: Parameters for an example take to generate for this voice.  If not
                      provided, a default example text will be used, depending on the
                      language of the model.
        done_webhook: An optional URL to call using ``POST`` when the voice is available,
                      with the response of VoiceInfo in the body content.  This shall be
                      called once, after the voice and example take have been generated.

    """
    name: str
    model: str
    gender: VoiceGender
    description: Optional[str]=None
    default_style: Optional[list[str]] = None
    default_prosody: Optional[ProsodyFeaturesUnion] = None
    example_take: Optional[TakeGenerateWithoutVoice] = None
    done_webhook: Optional[Webhook] = None

class VoiceInfo(VoiceGenerate):
    """Information about a voice.

    Attributes:
        voice_id: The unique identifier of this voice.
        status: The status of this voice, whether it is ready, in error, or in progress.
        timestamp_ms: The timestamp that this voice generation was requested, in
                      milliseconds since epoch.
        example_take_id: An optional identifier for a take that represents an example of
                         this voice.

    """
    voice_id: str
    status: Status
    timestamp_ms: int
    example_take_id: Optional[str] = None

class VoiceUpdate(BaseModel):
    """Update parameters of a voice.

    Attributes:
        name: A name to give the voice, may be any string, and does not need to be unique.
        gender: The gender of this voice.
        default_style: An optional list of styles to associate with this voice by default.
                       It can be overriden by a take that uses this voice.  Note that
                       most styles are mutually exclusive, and not all models support
                       styles.
        default_prosody: An optional default prosody to associate with this voice.  It can
                         be overridden by a take that uses this voice.
    """
    name: Optional[str] = None
    gender: Optional[VoiceGender] = None
    default_style: Optional[list[str]] = None
    default_prosody: Optional[ProsodyFeaturesUnion] = None

class TTSModel(BaseModel):
    """Information about a speech model.

    Attributes:
        name: The unique identifier of this model.
        displayname: A friendlier name that might contain spaces.
        flags: A list of flags that indicate some features of this model.
        languages: A list of languages supported by this model.
        genders: A list of genders supported by this model.
        styles: A list of style sets; each sublist is a list of mutually exlusive style tags.
        prosody_types: A list of which prosody types are supported by this model.
        voice_inputs: A list of which voice input types are supported by this model.
    """
    name: str
    displayname: str
    flags: list[str]=[]
    languages: list[str]
    genders: list[VoiceGender]
    styles: list[list[str]]=[]
    prosody_types: list[ProsodyType]
    voice_inputs: Optional[list[VoiceInputType]]

class StreamMode(str, enum.Enum):
    """Whether a websocket messages should contain a whole part or chunks of parts.

    Note: upper case in Python, lower case in JSON.

    Values:
      PARTS, CHUNKS
    """
    PARTS = 'parts'
    CHUNKS = 'chunks'

class StreamOptions(BaseModel):
    """Options for streaming.

    Attributes:
        mode: The streaming mode to use.
    """
    mode: StreamMode = StreamMode.PARTS

class WebsocketStatus(BaseModel):
    """Status messages on websocket connection.

    Attributes:
        status: 'ready' or 'error'
        message: a message to give details on the status
        request_id: present if the status update is assocated with a particular request
        model: present if the status update is associated with a particular model
    """
    status: Status
    message: str
    request_id: Optional[Union[int,str]] = None
    model: Optional[str] = None

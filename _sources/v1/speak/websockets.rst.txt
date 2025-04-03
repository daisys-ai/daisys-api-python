.. _v1_speak_websockets:

Daisys API websockets
=====================

The Daisys API provides a websocket interface to enable direct communication
with a single inference worker node, for applications that require lower
latency.

Latency vs. throughput
......................

While the websocket connection provides some convenience for certain
applications, it should not be used for tasks where a batch approach is more
appropriate, since generation requests through the REST API get distributed over
multiple workers and will overall finish faster. However, applications that
require real-time or near real-time interaction may benefit from keeping a
connection open and receiving the response immediately without making an extra
HTTP GET request.

Please do keep in mind that an effect of dedicating a connection is that
requests over this connection are effectively serialized, so the decision of
using websocket vs. the REST API is a typical latency vs. throughput tradeoff to
make.  For this reason, to help guarantee latency, the websocket system reserves
the right to occasionally drop the connection, forcing the client to request a
new URL, which has the effect of rebalancing the distribution of connections to
workers, helping to ensure lower latency overall.

In this document we describe:

- :ref:`connecting`: How to get a websocket URL and make and maintain a connection.
- :ref:`message_format`: The message format used to send commands and receive responses.
- :ref:`ws_python_interface`: How to use this Python library to communicate over the websocket.

Examples of using the websocket connection from the Python API as well as
communicating with the websocket from JavaScript in a browser application are
given in :ref:`websocket_examples`.


.. _connecting:

Connecting
..........

In order to connect to a Daisys worker node, you must first be assigned a node
through the API.  In Python, this is taken care of for you, see
:ref:`ws_python_interface` below.  However, when using another language or
``curl``, you can get a URL via the :ref:`websocket_endpoint` using a GET
request.

As mentioned there, the websocket may disconnect between requests for
rebalancing worker load, although this should not happen frequently.
Additionally it is assumed that a websocket connection is for interaction with a
specific model, which must be included in the URL.  In fact any model can be
used on a websocket connection but only the specified model shall be kept from
being unloaded, therefore if latency is at issue, it is recommended to open a
websocket connection per model.  A reconnection scheme can be used to
immediately request a new worker URL and reconnect if the connection is
dropped. The Daisys API shall make every effort to ensure that all current
requests are handled and results delivered before dropping any connections.

.. _message_format:

Message format
..............

In cases where you are not using Python and wish to develop your own client for
the websocket, the format is kept rather simple and should be quite approachable
for any language for which a websocket library is available.

Websocket supports text and bytes (binary) messages.  Commands are sent using
text messages, and status messages (text) and audio messages (bytes) are
received.  Both outgoing and incoming text messages are in JSON format.

Outgoing messages have the following format:

::

  {"command": "<command>", "data": {<data>}, "request_id": <request_id>}

where ``command`` may be one of ``/takes/generate`` or ``/voices/generate``.

The ``data`` field corresponds to the same POST body given to the corresponding
commands, i.e. the :class:`TakeGenerate <daisys.v1.speak.models.TakeGenerate>`
and :class:`VoiceGenerate <daisys.v1.speak.models.VoiceGenerate>` structures,
respectively.

Likewise, the status messages received for each correspond to the responses to
those same commands, these being :class:`TakeGenerate
<daisys.v1.speak.models.TakeResponse>` and :class:`TakeGenerate
<daisys.v1.speak.models.VoiceInfo>`, respectively.  They are similarly bundled
into a response structure,

::

  {"data": {<data>}, "request_id": <request_id>}

Special to the websocket connection is ``request_id``, which is needed to track
which incoming responses go with which outgoing requests.  Because websockets do
not guarantee message order (shorter messages may arrive before longer
messages), and because a ``take_id`` is not known until the first status message
is received, there is no way to know which audio goes with which
request. Therefore the ``request_id`` is a user-provided identifier, a string or
an integer, which is included with the responses to that command.  A simple
incrementing integer per connection is recommended, and is what the Python
interface implements.

Audio response messages are also simple, however since it is necessary to carry
some metadata, they contain two sections, delimited by a length prefix.  Audio
messages (bytes) are formatted thus:

::

  JSON<length 4 bytes><json metadata>RIFF..

That is, they start with the literal string ``JSON`` followed by a 32-bit little
endian integer indicating how long the metadata section is.  The metadata
section can be converted to a string and parsed as JSON.  This is immediately
followed by a ``.wav`` file header, which always starts with the literal string
``RIFF``.  Therefore, starting at ``R``, the rest of the bytes can be passed to
an audio player or a wav file parsing routine if chunking is not used.

The metadata section consists of the following fields,

::

  {"take_id": "<take_id>", "part_id": int, "chunk_id": int, "request_id": <request_id>}

where ``part_id`` and ``chunk_id`` are incrementing integers as specified in the
next section, and ``request_id`` reflects whatever was provided when the
associated command was issued.


Parts and chunks
................

If multiple sentences have been provided, then they are returned with separate
``part_id`` values, which are an incrementing integer, where each part consists
of a complete wav file.  The end of the stream for a take is indicated by a new
``part_id`` that has 0 bytes of audio.

If chunking is enabled, the bytes must be concatenated to an existing part
stream, either in real time or before writing the part to a file.  Chunks are
different from parts in that they are not prepended with a wav header, but are
merely the individual pieces of a part that is not yet fully received.  Similar
to parts, chunks are identified with an incrementing integer ``chunk_id`` which
must be used to put them in order before playback. Also similar, the end of the
chunk stream for a part is indicated by a new ``chunk_id`` being accompanied
with 0 bytes of audio.

Finally then, a stream of parts without chunking appears like so:

::

  [part_id=0, audio len=12340]
  [part_id=1, audio len=23450]
  [part_id=2, audio len=0]

and with chunking,

::

  [part_id=0, chunk_id=0, audio len=4140]
  [part_id=0, chunk_id=1, audio len=4140]
  [part_id=0, chunk_id=2, audio len=0]
  [part_id=1, chunk_id=0, audio len=4140]
  [part_id=1, chunk_id=1, audio len=4140]
  [part_id=1, chunk_id=2, audio len=0]
  [part_id=2, chunk_id=0, audio len=0]

The above is for visual explanation only, in reality the ``take_id`` and
``request_id`` are also included in the metadata header in order to know which
audio is for which stream.

I a ``/voices/generate`` message was requested, audio of the associated example
take will be sent.  However the status message will be a :class:`TakeGenerate
<daisys.v1.speak.models.VoiceInfo>` object, and the ``take_id`` included in the
audio messages will correspond with its ``example_take_id`` field.


.. _ws_python_interface:

Python interface
................

The Python interface consists of calling, :func:`websocket()` of the client
object (see :doc:`clients`), in a ``with`` context manager, which returns
respectively one of the following objects.  For example,

.. code-block:: python
   :caption: Streaming audio, websocket method
   :linenos:

   from daisys import DaisysAPI
   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       with speak.websocket(model='theatrical-v2') as ws:
           ....
           request_id = ws.generate_take(...

In each case, you can then issue a command to generate a take or a voice using
the returned context object, as demonstrated above.  Subsequently the callbacks
you provide get called whenever messages are received on the websocket
containing either status information or audio data.

.. automodule:: daisys.v1.speak.sync_websocket
   :members:

.. automodule:: daisys.v1.speak.async_websocket
   :members:

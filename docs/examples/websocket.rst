.. _websocket_examples:

Daisys API websocket examples
=============================

In addition to retrieving audio by means of the REST API (see
:ref:`v1_speak_endpoints_retrieving_audio`), takes can also be requested and
audio can be streamed using a websocket connection.  Do note that if the
``/wav`` endpoint is accessed before a take is "ready", the `.wav` file will be
streamed while it is generated, so the complexities of the websocket connection
may not be necessary, depending on your application.  However, the websocket
connection does provide the lowest latency since the connection is directly made
to a worker node.

On the other hand since a single shared connection is used, requests over
websocket are essentially serialized.  For batch-style jobs where throughput
rather than latency is a concern, the REST API is encouraged, since it
distributes the jobs over multiple workers.

The websocket streaming is also higher complexity than using the REST API.  A
detailed definition of the websocket streaming protocol can be found at
:ref:`v1_speak_websockets`.

Parts vs chunks
...............

There are two streaming modes: "parts" and "chunks", each example by default
shows "parts" mode but can be put in "chunks" mode by executing with an argument
``--chunks``.

The difference is:

* For audio generation, an input paragraph or document is broken up into
  multiple parts that end in silence, usually corresponding with a sentence.
* In "parts" streaming mode, the default, each part is sent in a separate
  message.  Each part contains a ``wav`` header. The intention is that this can
  be parsed and played directly by an audio player, and each part can be
  sequenced one after the other.
* In "chunks" streaming mode, the parts similarly are each composed of a ``wav``
  file with a header, however the file is sent in small chunks as it is
  generated.  This results in reduced latency, at the expense that the chunks
  must be combined on reception, either by feeding them into an audio stream or
  concatenating them into a final ``wav`` file.  Only the first chunk contains
  the ``wav`` header, and the length it indicates corresponds to the full part.

Furthermore each request results in a stream of both text and binary messages.
The former contain the entire contents of the take's
:class:`~daisys.v1.speak.models.TakeResponse` structure, and is transmitted
whenever the ``status`` field changes.  The latter contains the audio parts or
chunks.

Callbacks vs iterator
.....................

for both the "parts" and "chunks" mode, the Python API provides either a
callback-based mechanism for receiving status and audio messages, as well as a
wrapper that provides an iterator-style interface called
:meth:`~daisys.v1.speak.async_websocket.DaisysAsyncSpeakWebsocketV1.iter_request`
to the same information which tends to simplify client code, see the
corresponding examples for synchronous and async clients.

When callbacks or iterators are executed, order has already been reconstructed,
so parts and chunks are delivered to the user code in the correct order.

  Due to the nature of websocket connections, the order of incoming messages is
  not guaranteed.  This is why the ``part_id`` and ``chunk_id`` values are
  included in all messages (``chunk_id`` only if "chunks" streaming option is
  specified), so that the correct order can be reconstructed in the receiving
  client.  This is also taken care of by the Python library, and is demonstrated
  for JavaScript in the ``websocket_client`` web app example.

Fetching the websocket URL directly
...................................

As mentioned, the last example ``websocket_client`` shows how to integrate
websockets into a web app, and therefore in this case the stream ingestion is
performed by JavaScript.  Therefore the Python library is only used to retrieve
the websocket URL using
:meth:`~daisys.v1.speak.async_client.DaisysAsyncSpeakClientV1.websocket_url`
(which includes a lifetime-limited secret that is distinct from your access
token for security) and the same work described above of connecting to the
websocket, sending requests, and iterating over the ordered incoming status and
audio messages is performed by the included JavaScript code.

.. toctree::
   :maxdepth: 1
   :caption: Contents

   websocket_example.rst
   websocket_example_iter.rst
   websocket_example_async.rst
   websocket_example_async_iter.rst
   websocket_client.rst

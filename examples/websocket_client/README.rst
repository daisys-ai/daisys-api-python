Web client example
==================

This application demonstrates how to set up a simple FastAPI-based backend to
perform login to the Daisys API and return a websocket URL to the client-side
browser application, which then uses it to make take requests and stream the
resulting audio directly to the browser for playback.

In ``websocket_connector.js`` , the URL is retrieved and the websocket
connection is made and automatically reconnected if the connection is dropped.

The incoming messages come in two streams: status updates and audio chunks,
which are serialized per request in ``websocket_stream.js`` using an async
generator, making it easy to simply read the messages in the reconstructed order
and pass the audio chunks directly to an audio context for playback.

A simpler method where whole sentences (parts) are passed to the audio context
as "sources" is given, as well as slightly more complex buffer management for
chunk-based streams.

See ``websocket_client.js`` for the main application-specific entry points
demonstrating these concepts.

The application can be executed with::

  uvicorn examples.websocket_client:app --port 8001

or equivalently::

  python3 -m examples.websocket_client

.. _websocket_client:

Example: Websocket example, web client
======================================

This example shows how to use the Python client library to create a
`FastAPI`_-based web server that performs login to the Daisys API (so that
credentials are kept secure) and interacts with the REST API to retrieve a
websocket URL.  This URL is passed to the front-end JavaScript application that
makes the websocket connection and makes take requests, playing back the audio
in a streaming fashion using the `Web Audio API`_.

.. _FastAPI: https://fastapi.tiangolo.com/
.. _Web Audio API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API

The included JavaScript shows how to:

1. Retrieve the URL using
   :meth:`~daisys.v1.speak.async_client.DaisysAsyncSpeakClientV1.websocket_url`
   and open the websocket connection, automatically doing so again when
   disconnected, see `websocket_connector.js`_.

2. Define an async iterator that simplifies handling of streams for different
   requests by transforming the callback structure into a simple for loop, see
   `websocket_stream.js`_ and usage in `websocket_client.js`_.

3. Send a request for generating a take, see `websocket_client.js`_.

4. Use a single handler to handle incoming status messages and audio messages in
   both "parts" and "chunks" mode, see `websocket_stream.js`_.

5. Respectively play the audio in a simple (parts, using audio sources) and more
   complex (chunks, using dynamic audio buffers) way using the Web Audio API,
   see `part_audio_player.js`_ and `chunk_audio_player.js`_.

.. _websocket_connector.js: https://github.com/daisys-ai/daisys-api-python/tree/main/examples/websocket_client/websocket_connector.js
.. _websocket_stream.js: https://github.com/daisys-ai/daisys-api-python/tree/main/examples/websocket_client/websocket_stream.js
.. _websocket_client.js: https://github.com/daisys-ai/daisys-api-python/tree/main/examples/websocket_client/websocket_client.js
.. _part_audio_player.js: https://github.com/daisys-ai/daisys-api-python/tree/main/examples/websocket_client/part_audio_player.js
.. _chunk_audio_player.js: https://github.com/daisys-ai/daisys-api-python/tree/main/examples/websocket_client/chunk_audio_player.js

The above consists of several files, as opposed to other examples, so instead of
repeating the example in the documentation, the reader is invited to follow `the
code in the git repository`_.

.. _the code in the git repository: https://github.com/daisys-ai/daisys-api-python/tree/main/examples/websocket_client

The application can be launched using::

  python3 -m examples.websocket_client

or equivalently::

  uvicorn examples.websocket_client:app


.. _v1_speak_curl_example:

Example: ``curl`` example
=========================

This example shows:

1. How to use ``curl`` and ``jq`` in a shell script to access the Daisys API.

2. How to create the synchronous client using a context manager.

3. Get a list of voices and select the last one.

4. Reference the voice to generate audio (a "take") for some text.

5. Download the resulting audio.

6. Play the audio using ``aplay`` (Linux).

To run it, you must supply your email and password in the respecting environment
variables, as shown below.

Requires: `curl <https://curl.se/>`_, `jq <https://jqlang.github.io/jq/>`_.

.. code-block:: shell
   :caption: Example output

   $ curl -O https://raw.githubusercontent.com/daisys-ai/daisys-api-python/main/examples/curl_example.sh
   $ jq --version  # "jq" is needed for the example program to parse API responses
   $ export DAISYS_EMAIL=user@example.com
   $ export DAISYS_PASSWORD=example_password123
   $ bash examples/curl_example.sh 
   Found Daisys Speak API  {"version":1,"minor":0}
   GET https://api.daisys.ai/v1/speak/voices
   "Deirdre" is speaking!
   POST https://api.daisys.ai/v1/speak/takes/generate: {"voice_id": "v01hasgezqjcsnc91zdfzpx0apj",
   "text": "Hello there, I am Daisys!", "prosody": {"pace": -8, "pitch": 2, "expression": 8}}
   Take is "waiting".
   GET https://api.daisys.ai/v1/speak/takes/t01hawm80qzj60bf2w9z0np7wej
   Take is "started".
   GET https://api.daisys.ai/v1/speak/takes/t01hawm80qzj60bf2w9z0np7wej
   Take is "ready".
   Getting audio!
   GET https://api.daisys.ai/v1/speak/takes/t01hawm80qzj60bf2w9z0np7wej/wav
   Wrote 'hello_daisys.wav'.
   Playing WAVE 'hello_daisys.wav' : Signed 16 bit Little Endian, Rate 44100 Hz, Mono

The "Playing" message will only appear if you have the ``aplay`` command installed,
otherwise you may play the resulting ``hello_daisys.wav`` file in any audio player.

.. literalinclude:: ../../examples/curl_example.sh
   :language: shell
   :caption: examples/curl_example.sh
   :linenos:

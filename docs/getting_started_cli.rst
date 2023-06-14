
Getting started with the command line
=====================================

The Daisys API can be used from the command line using ``curl`` and ``jq``.  Most
application writers will want to use this guide to see how to make HTTP calls to the API
for developing their own client libraries in their favorite language.

Running the ``curl`` example
............................

The Python client library source code bundles an :ref:`example <v1_speak_curl_example>` of
how to use the API this way.  Instructions to run that example are provided on the linked
page.

The rest of this document shall describe how to use the API one step at a time in a shell,
rather than in a shell script.  In the examples, the result of ``curl`` is piped to ``jq .``
for formatting purposes.

Authenticating
..............

To access the Daisys Speak API, you must attach an access token to any HTTP calls, with
the exception of the ``/version`` endpoint.

To get such an access key, it can be requested by providing an email and password as
follows:

.. code-block:: shell
   :caption: Authenticating: Getting an access token
   :linenos:

   TOKENS=$(curl -s -X POST -H 'content-type: application/json' \
            -d '{"email": "user@example.com", "password": "my_password123"}' \
            https://api.daisys.ai/auth/login)
   export ACCESS_TOKEN=$(echo $TOKENS | jq -r .access_token)
   export REFRESH_TOKEN=$(echo $TOKENS | jq -r .refresh_token)

You can keep using this access token for a limited time.  It can be used by adding it into
the string ``Bearer $ACCESS_TOKEN`` for the value of the ``Authorization`` header.

If you receive a 401 response from any API request, the access token needs to be refreshed
by issuing:

.. code-block:: shell
   :caption: Authenticating: Refreshing the access token
   :linenos:

   $ TOKENS=$(curl -s -X POST -H 'content-type: application/json' \
              -H "Authorization: Bearer $ACCESS_TOKEN" \
              -d '{"refresh_token": "'$REFRESH_TOKEN'"}' \
              https://api.daisys.ai/auth/refresh)
   $ export ACCESS_TOKEN=$(echo $TOKENS | jq -r .access_token)
   $ export REFRESH_TOKEN=$(echo $TOKENS | jq -r .refresh_token)

Listing the models
..................

Models can be listed by accessing the ``/models`` endpoint.  More information on the
options are found in :ref:`v1_speak_model_endpoints`.

.. code-block:: shell
   :caption: Listing the models
   :linenos:

   $ curl -s -X GET -H "Authorization: Bearer $ACCESS_TOKEN" https://api.daisys.ai/v1/speak/models | jq .
   [
     {
       "name": "shakespeare",
       "displayname": "Shakespeare",
       "flags": [],
       "languages": [
         "en-GB"
       ],
       "genders": [
         "female",
         "male"
       ],
       "styles": [
         [
           "base",
           "character",
           "narrator"
         ]
       ],
       "prosody_types": [
         "simple",
         "affect"
       ]
     }
   ]

Listing the voices
..................

Voices can be listed by accessing the ``/voices`` endpoint.  More information on the
options are found in :ref:`v1_speak_voice_endpoints`.

.. code-block:: shell
   :caption: Listing the voices
   :linenos:

   $ curl -s -X GET -H "Authorization: Bearer $ACCESS_TOKEN" https://api.daisys.ai/v1/speak/voices | jq .
   [
     {
       "name": "Deirdre",
       "model": "shakespeare",
       "gender": "female",
       "default_style": [],
       "default_prosody": null,
       "example_take": null,
       "status_webhook": null,
       "done_webhook": null,
       "voice_id": "v01hasgezqjcsnc91zdfzpx0apj",
       "status": "ready",
       "timestamp_ms": 1695220727538,
       "example_take_id": "t01hasgezqkx4vth62xckymk3x3"
     }
   ]

Generating a voice
..................

If you do not yet have any voices, you should generate one using the ``/voices/generate``
endpoint.  Voices can be requested for a given gender and with default prosody
information.  Voices must be given names.  More information on the options are found in
:ref:`v1_speak_voice_endpoints`.

For instance, the following command creates an expressive female voice for the
``shakespeare`` model:

.. code-block:: shell
   :caption: Generating a voice
   :linenos:

   $ curl -s -X POST -H 'content-type: application/json' \
   -H "Authorization: Bearer $ACCESS_TOKEN" \
   -d '{"name": "Ignacio", "gender": "male", "model": "shakespeare"}' \
   https://api.daisys.ai/v1/speak/voices/generate | jq .
   {
     "name": "Ignacio",
     "model": "shakespeare-pause_symbol-18-4-23",
     "gender": "male",
     "default_style": null,
     "default_prosody": null,
     "example_take": null,
     "done_webhook": null,
     "voice_id": "v01haxx5cggwz215gzv0hjbra9m",
     "status": "waiting",
     "timestamp_ms": 1695368262160,
     "example_take_id": "t01haxx5cgg3n8f2qzc8zkbn97y"
   }

Note that voice generation can take a few seconds! In this example, the "status" is
"waiting" and not yet "ready", therefore we should check in on it again after a second or
two.  For this, we need to use the ``voice_id`` provided in the response:

.. code-block:: shell
   :caption: Checking the voice status
   :linenos:

   $ curl -s -X GET -H 'content-type: application/json' \
   -H "Authorization: Bearer $ACCESS_TOKEN" \
   https://api.daisys.ai/dev/v1/speak/voices/v01haxx5cggwz215gzv0hjbra9m | jq .
   {
     "name": "Ignacio",
     "model": "shakespeare-pause_symbol-18-4-23",
     "gender": "male",
     "default_style": null,
     "default_prosody": null,
     "example_take": null,
     "done_webhook": null,
     "voice_id": "v01haxx5cggwz215gzv0hjbra9m",
     "status": "ready",
     "timestamp_ms": 1695368262160,
     "example_take_id": "t01haxx5cgg3n8f2qzc8zkbn97y"
   }

The voice is now "ready"!  We can now get its example audio using the ``example_take_id``
field, see :ref:`retrieving_take_audio` below.

Note: as seen in the response structure, a webhook can also be provided to get a
notification when the result is ready.  This webhook is called as a ``POST`` request with
the same response structure as seen here, provided in the request body.

Generating a take
.................

Now that you have a voice, text to speech can be requested by the ``/takes/generate``
endpoint.  Here we generate one with default prosody for the voice, which we also left as
default (neutral) when generating the voice above.  More information on the options are
found in :ref:`v1_speak_take_endpoints`.

.. code-block:: shell
   :caption: Generating a take
   :linenos:

   $ curl -s -X POST -H 'content-type: application/json' \
   -H "Authorization: Bearer $ACCESS_TOKEN" \
   -d '{"text": "Hello, Daisys! It'\''s a beautiful day.", "voice_id": "v01hasgezqjcsnc91zdfzpx0apj"}' \
   https://api.daisys.ai/dev/v1/speak/takes/generate
   {
     "text": "Hello, Daisys! It's a beautiful day.",
     "override_language": null,
     "style": null,
     "prosody": null,
     "status_webhook": null,
     "done_webhook": null,
     "voice_id": "v01hasgezqjcsnc91zdfzpx0apj",
     "take_id": "t01haybgb16dn9dk0p5je47qz74",
     "status": "waiting",
     "timestamp_ms": 1695383301158,
     "info": null
   }

Similar to with voice generation, take generation takes a couple of seconds, and the
status can be retrieved by using the ``take_id``:

.. code-block:: shell
   :caption: Generating a take: checking status
   :linenos:

   $ curl -s -X GET -H "Authorization: Bearer $ACCESS_TOKEN" \
   https://api.daisys.ai/dev/v1/speak/takes/t01haybgb16dn9dk0p5je47qz74 | jq .
   {
     "text": "Hello, Daisys! It's a beautiful day.",
     "override_language": null,
     "style": null,
     "prosody": null,
     "status_webhook": null,
     "done_webhook": null,
     "voice_id": "v01hasgezqjcsnc91zdfzpx0apj",
     "take_id": "t01haybgb16dn9dk0p5je47qz74",
     "status": "ready",
     "timestamp_ms": 1695383301158,
     "info": {
       "duration": 150528,
       "audio_rate": 44100,
       "normalized_text": [
         "Hello, Daisys!",
         "It's a beautiful day."
       ]
     }
   }

Similar to voice generation, it is possible to use a webhook for the "done" notification.
For longer texts, it is also possible to request a "status" webhook which may be called
several times whenever the progress for a take changes.

Here, we see the status is "ready", meaning that audio can now be retrieved.

.. _retrieving_take_audio:

Retrieving a take's audio
.........................

The take is ready, now we can hear the result!  Audio for a take can be retrieved as follows:

.. code-block:: shell
   :caption: Retrieving audio
   :linenos:

   $ curl -s -L -X GET -H "Authorization: Bearer $ACCESS_TOKEN" \
   -o beautiful_day.wav \
   https://api.daisys.ai/dev/v1/speak/takes/t01haybgb16dn9dk0p5je47qz74/wav

In the above, we retrieve a ``.wav`` file and write it to disk as ``beautiful_day.wav``.
Note that the ``-L`` flag must be provided since the file is returned through a 307
redirect.

The resulting file ``beautiful_day.wav`` can be played using command line programs like
``aplay`` on Linux, or any audio player such as the excellent `VLC`_.  You can integrate
the results into your creative projects!

It is also possible to retrieve the audio in other formats: ``mp3``, ``flac``, and
``m4a``, by retrieving at the corresponding URL,
``../speak/takes/t01haybgb16dn9dk0p5je47qz74/mp3``, etc.

.. _VLC: https://www.videolan.org/

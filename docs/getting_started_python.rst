Getting started with the Python client library
==============================================

For more on using the Python client library, see :doc:`examples`.

In the following, the default "synchronous" client will be demonstrated.  Some users will
prefer to use ``asyncio``, and in the following examples, ``with DaisysAPI()`` can be
replaced with ``async with DaisysAPI``, which returns an asynchronous client library that
can be used with the ``await`` keyword.

Installing the library
......................

The library is available on pypi.org and can be installed via ``pip``.  The Daisys API
requires Python version 3.10 or greater.  First create a Python ``venv``, activate it,
install the library, and then download and run the examples:

.. code-block:: shell
   :caption: Installing the library
   :linenos:

   $ mkdir daisys_project
   $ cd daisys_project
   $ python3 -m venv venv
   $ . venv/bin/activate
   $ python3 -m pip daisys

Running an example
..................

Within the Python virtual environment, the ``hello_daisys.py`` example can be run. The
examples are programmed to take your email and password in the environment variables as
shown:

.. code-block:: shell
   :caption: Running an example
   :linenos:

   $ curl -O https://raw.githubusercontent.com/daisys-ai/daisys-api-python/main/examples/hello_daisys.py
   $ export DAISYS_EMAIL=user@example.com
   $ export DAISYS_PASSWORD=example_password123
   $ python3 hello_daisys.py

Getting a client
................

.. code-block:: python
   :caption: Getting a client by context manager
   :linenos:

   from daisys import DaisysAPI
   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       ...

   # or for asyncio support:
   async with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       ...

As mentioned, an ``asyncio``-enabled client can be instantiated by using ``async with`` in
the line above.  Additionally, the context manager interface (``with``) is optional; it is
also possible to create a client by normal function call:

.. code-block:: python
   :caption: Getting a client by function
   :linenos:

   from daisys import DaisysAPI
   speak = DaisysAPI('speak', email=EMAIL, password=PASSWORD).get_client()
   # or..
   speak = DaisysAPI('speak', email=EMAIL, password=PASSWORD).get_async_client()

The main difference is that when an email and password are used, the context manager
approach will automatically log out when the program exits the context, whereas when the
client is retrieved by ``get_client`` or ``get_async_client``, then ``.logout()`` function
should be called.  Logging out invalidates the refresh token so that no further sessions
can be renewed without logging in again.  Auto-logout will not occur when an access token
is provided.

The rest of this documentation will assume the normal, synchronous client.  In all cases,
functions should be called with ``await`` when used with the ``asyncio`` client.

Listing the models
..................

Using the client library, it is easy to log into the API and start requesting text to
speech services.  The following Python code can be used to list the available models:

.. code-block:: python
   :caption: Listing the models
   :linenos:

   from daisys import DaisysAPI
   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       print('Found models:')
       for model in speak.get_models():
           print(model)

Listing the voices
..................

You can use a model by using a voice associated with that model.  Voices are identified by
a ``voice_id`` field.

.. code-block:: python
   :caption: Listing the voices
   :linenos:

   from daisys import DaisysAPI
   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       print('Found voices:')
       for voice in speak.get_voices():
           print(f'{voice.name}, a {voice.gender} voice of {voice.model} with id {voice.voice_id}.')

Generating a voice
..................

If you do not yet have any voices, you should generate one.  Voices can be requested for a
given gender and with default prosody information.  Voices must be given names.

For instance, the following block of code creates an expressive female voice for the
``shakespeare`` model:

.. code-block:: python
   :caption: Generating a voice
   :linenos:

   from daisys import DaisysAPI, VoiceGender
   from pprint import pprint
   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       print('Creating a voice:')
       voice = speak.generate_voice(name="Deirdre", gender=VoiceGender.FEMALE, model="shakespeare")
       pprint(voice.model_dump())

Note that voice generation can take a few seconds! In this example, the
``speak.generate_voice`` command `waits` for the operation to finish, and therefore we can
print the result immediately.

It is also possible to adopt a more asynchronous style by providing ``wait=False`` to
``speak.generate_voice()``.  Alternatively, as mentioned above you can use the ``asyncio``
client to allow the ``await speak.generate_voice()`` syntax.

The above code gives the following details:

.. code-block:: text
   :caption: Generating a voice: output
   :linenos:

   Creating a voice:
   {'default_style': [],
    'default_prosody': None,
    'done_webhook': None,
    'example_take': None,
    'example_take_id': 't01hasgezqkx4vth62xckymk3x3',
    'gender': <VoiceGender.FEMALE: 'female'>,
    'model': 'shakespeare',
    'name': 'Deirdre',
    'status': <Status.READY: 'ready'>,
    'timestamp_ms': 1695218371261,
    'voice_id': 'v01hasgezqjcsnc91zdfzpx0apj'}

We can see that the voice has a female gender, and has an example take associated with it.
This ``take_id`` can already be used to hear the voice.

Generating a take
.................

Now that you have a voice, text to speech can be requested by the
``speak.take_generate()`` command:

.. code-block:: python
   :caption: Generating a take
   :linenos:

   from daisys import DaisysAPI
   from pprint import pprint
   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       print('Creating a take:')
       take = speak.generate_take(voice_id='v01hasgezqjcsnc91zdfzpx0apj',
                                  text="Hello, Daisys! It's a beautiful day.")
       pprint(take.model_dump())

Giving,

.. code-block:: text
   :caption: Generating a take: output
   :linenos:

   Creating a take:
   {'done_webhook': None,
    'info': {'audio_rate': 44100,
             'duration': 152576,
             'normalized_text': ['Hello, Daisys!', "It's a beautiful day."]},
    'override_language': None,
    'prosody': None,
    'status': <Status.READY: 'ready'>,
    'status_webhook': None,
    'style': None,
    'take_id': 't01hasgn2dnyg6jqrcym9cgxv75',
    'text': "Hello, Daisys! It's a beautiful day.",
    'timestamp_ms': 1695220926901,
    'voice_id': 'v01hasgezqjcsnc91zdfzpx0apj'}

Note that the status is "ready", meaning that audio can now be retrieved.  As with voice
generation, an asynchronous approach is also available for ``generate_take``.

Retrieving a take's audio
.........................

The take is ready, now we can hear the result!  Audio for a take can be retrieved as follows:

.. code-block:: python
   :caption: Retrieving audio (1)
   :linenos:

   from daisys import DaisysAPI
   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       print("Getting a take's audio.")
       audio_wav = speak.get_take_audio(take_id='t01hasghx0zgdc29gpzexw5r8wc', file='beautiful_day.wav')
       print('Length in bytes:', len(audio_wav))

In the above code, we retrive a ``.wav`` file, which is (optiionally) written to a file in
addition to being returned.  This can be decoded for example using ``scipy``'s
``io.wavfile`` module:

.. code-block:: python
   :caption: Retrieving audio (2)
   :linenos:

       from scipy.io import wavfile
       from io import BytesIO
       print(wavfile.read(BytesIO(audio_wav)))

       # Note: Since decoding the audio is outside the scope of the client library,
       # `scipy` is not a dependency and will not be automatically installed by `pip`.

which, along with the previous code block, prints:

.. code-block:: text
   :caption: Retrieving audio: output
   :linenos:

   Getting a take's audio.
   Length in bytes: 292908
   (44100, array([-111,  -46, -104, ..., -128,  -95,   -9], dtype=int16))

The resulting file ``beautiful_day.wav`` can be played using command line programs like
``aplay`` on Linux, or any audio player such as the excellent `VLC`_.  You can integrate
the results into your creative projects!

It is also possible to retrieve the audio in other formats: ``mp3``, ``flac``, and ``m4a``
by providing the ``format`` parameter.

.. _VLC: https://www.videolan.org/

Authentication with access tokens
.................................

All the above examples authenticate with the API using email and password.  In some
scenarios users will prefer to authenticate using only the access token.  An access and
refresh token can be retrieved once and used until it is manually revoked.

By default, when the client library is used with email and password, the refresh token is
automatically revoked when the client context is exited.  When an access token is provided
to the client context, this automatic revocation is skipped, so that the token can be
refreshed on next usage.  This can be controlled by setting ``speak.auto_logout`` to
``True`` or ``False``.

To retrieve an access and refresh token for future use, the following program can thus be
used:

.. code-block:: python
   :caption: Retrieving an access and refresh token
   :linenos:

   from daisys import DaisysAPI
   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       speak.auto_logout = False
       speak.login()
       access_token, refresh_token = speak.access_token, speak.refresh_token

These tokens can now be stored, and provided to the client as follows:

.. code-block:: python
   :caption: Retrieving an access and refresh token
   :linenos:

   from daisys import DaisysAPI

   def store_tokens(speak, access_token: str, refresh_token: str):
       """Store the current Daisys access and refresh tokens."""
       with open('daisys_tokens.json','w') as token_file:
           json.dump([access_token, refresh_token], token_file)

   access_token, refresh_token = json.load(open('daisys_tokens.json'))
   with DaisysAPI('speak', access_token=access_token, refresh_token=refresh_token) as speak:
       speak.refresh_callback = store_tokens
       ...

The library does *not* implement a storage and retrieval mechanism for these tokens, as it
is presumed that users will have their own files or databases for this purpose.

Importantly, when an access token expires, a new one will be automatically retrieved by
the library.  Therefore, it is useful to store ``speak.access_token`` and
``speak.refresh_token`` whenever it changes.  The ``refresh_callback`` is provided for
this purpose.  It is optional, but recommended if not using a permatoken and one wishes to
avoid transmitting passwords.

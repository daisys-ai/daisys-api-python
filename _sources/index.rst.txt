Daisys API documentation
========================

This is the documentation for the public wrapper library for the Daisys API.  The main
product is "Speak", which provides text-to-speech (TTS) services.

Have your product talking in seconds!

.. code-block:: python
   :caption: Example
   :linenos:

   with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
       voice = await speak.get_voices()[-1]
       print(f"{voice.name} speaking!")
       take = speak.generate_take(voice_id=voice.voice_id, text="Hello there, I am Daisys!",
                                  prosody=SimpleProsody(pace=-3, pitch=2, expression=10))
       audio_wav = speak.get_take_audio(take.take_id, filename='hello_daisys.wav')

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started.rst
   examples.rst
   input.rst
   daisys.rst
   v1/speak/clients.rst
   v1/speak/models.rst
   v1/speak/endpoints.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

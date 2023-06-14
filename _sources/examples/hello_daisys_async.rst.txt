Example: Hello Daisys, asynchronous client
==========================================

This example shows:

1. How to create the asyncio client using a context manager.

2. Get a list of voices.

3. If there are none, how to generate a voice.

4. Reference the voice to generate audio (a "take") for some text.

5. Download the resulting audio.

6. Get the take information by identifier or as a filtered list.

To run it, you must replace the username and password with your credentials.

.. code-block:: shell
   :caption: Example output

   $ python3 -m examples.hello_daisys_async
   Found Daisys Speak API version=1 minor=0
   Found voices: []
   Not enough voices!
   Using model "shakespeare"
   Generating a voice.
   Sally speaking!
   Read 208940 bytes of wav data, wrote "hello_daisys.wav".
   Checking take: True
   Checking list of takes: True
   Deleting take t01hbbgyx2008ggp61pzh6jaemf: True
   Deleting voice v01hbbgyrpxxbcj6q37f1yd03gd: True

.. literalinclude:: ../../examples/hello_daisys_async.py
   :language: python
   :caption: examples/hello_daisys_async.py
   :linenos:

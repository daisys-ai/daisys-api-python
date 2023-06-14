Example: Hello Daisys, synchronous client
=========================================

This example shows:

1. How to create the synchronous client using a context manager.

2. Get a list of voices.

3. If there are none, how to generate a voice.

4. Reference the voice to generate audio (a "take") for some text.

5. Download the resulting audio.

.. code-block:: shell
   :caption: Example output

   $ python3 -m examples.hello_daisys
   Found Daisys Speak API version=1 minor=0
   Found voices: []
   Not enough voices!
   Using model "shakespeare"
   Generating a voice.
   Sally speaking!
   Read 198700 bytes of wav data, wrote "hello_daisys.wav".
   Checking take: True
   Checking list of takes: True
   Deleting take t01hbbgw0zz4e9y6pb9qdxnrmag: True
   Deleting voice v01hbbgtrvk50pxwyjvvsxygbza: True


.. literalinclude:: ../../examples/hello_daisys.py
   :language: python
   :caption: examples/hello_daisys.py
   :linenos:

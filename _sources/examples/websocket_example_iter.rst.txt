Example: Websocket example, synchronous client with iterator
============================================================

This example shows:

1. How to open a websocket connection using a context manager.

2. Generate a take.

3. How to iterate over the resulting status and audio messages using ``iter_request()``.

4. How to make a request with and without chunks enabled. (Add argument ``--chunks``.)

.. code-block:: shell
   :caption: Example output

   $ python3 -m examples.websocket_example_iter
   Found Daisys Speak API version=1 minor=0
   [0.002] Take status was changed to: WAITING.
   [0.022] Take status was changed to: STARTED.
   [0.748] New part being received.
   [0.748] Received audio chunk of size 233472.
   [1.204] Take status was changed to: PROGRESS_50.
   [1.208] New part being received.
   [1.208] Received audio chunk of size 116736.
   [2.597] Take status was changed to: READY.
   Deleting take t01jqrj9j7hyx49enqya9qeas3t: True

.. code-block:: shell
   :caption: Example output (chunks enabled)

   $ python3 -m examples.websocket_example_iter --chunks
   Found Daisys Speak API version=1 minor=0
   [0.002] Take status was changed to: WAITING.
   [0.026] Take status was changed to: STARTED.
   [0.314] New part being received.
   [0.314] Received audio chunk of size 4096.
   [0.328] Received audio chunk of size 4096.
   [0.341] Received audio chunk of size 4096.
   [0.351] Received audio chunk of size 4096.
   [0.361] Received audio chunk of size 4096.
   [0.371] Received audio chunk of size 4096.
   [0.381] Received audio chunk of size 4096.
   [0.391] Received audio chunk of size 4096.
   [0.401] Received audio chunk of size 4096.
   [0.411] Received audio chunk of size 4096.
   [0.421] Received audio chunk of size 4096.
   [0.431] Received audio chunk of size 4096.
   [0.442] Received audio chunk of size 4096.
   [0.452] Received audio chunk of size 4096.
   [0.462] Received audio chunk of size 4096.
   [0.472] Received audio chunk of size 4096.
   [0.482] Received audio chunk of size 4096.
   [0.492] Received audio chunk of size 4096.
   [0.502] Received audio chunk of size 4096.
   [0.512] Received audio chunk of size 4096.
   [0.521] Received audio chunk of size 4096.
   [0.532] Received audio chunk of size 4096.
   [0.542] Received audio chunk of size 4096.
   [0.551] Received audio chunk of size 4096.
   [0.561] Received audio chunk of size 4096.
   [0.572] Received audio chunk of size 4096.
   [0.582] Received audio chunk of size 4096.
   [0.592] Received audio chunk of size 4096.
   [0.603] Received audio chunk of size 4096.
   [0.613] Received audio chunk of size 1536.
   [0.963] Take status was changed to: PROGRESS_50.
   [0.966] New part being received.
   [0.966] Received audio chunk of size 4096.
   [0.976] Received audio chunk of size 4096.
   [0.985] Received audio chunk of size 4096.
   [0.994] Received audio chunk of size 4096.
   [1.004] Received audio chunk of size 4096.
   [1.014] Received audio chunk of size 4096.
   [1.024] Received audio chunk of size 4096.
   [1.034] Received audio chunk of size 4096.
   [1.044] Received audio chunk of size 4096.
   [1.055] Received audio chunk of size 4096.
   [1.065] Received audio chunk of size 4096.
   [1.075] Received audio chunk of size 4096.
   [1.085] Received audio chunk of size 4096.
   [1.095] Received audio chunk of size 3072.
   [2.600] Take status was changed to: READY.
   Deleting take t01jqrjxc257e1mr0r0z65ak4qb: True

.. literalinclude:: ../../examples/websocket_example_async_iter.py
   :language: python
   :caption: examples/websocket_example_async_iter.py
   :linenos:

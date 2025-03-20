Example: Websocket example, asynchronous client with iterator
=============================================================

This example shows:

1. How to open a websocket connection using an async context manager.

2. Generate a take.

3. How to iterate over the resulting status and audio messages using ``iter_request()``.

4. How to make a request with and without chunks enabled. (Add argument ``--chunks``.)

.. code-block:: shell
   :caption: Example output

   $ python3 -m examples.websocket_example_async_iter
   Found Daisys Speak API version=1 minor=0
   [0.002] Take status was changed to: WAITING.
   [0.024] Take status was changed to: STARTED.
   [0.761] New part being received.
   [0.761] Received audio chunk of size 245760.
   [1.197] Take status was changed to: PROGRESS_50.
   [1.200] New part being received.
   [1.200] Received audio chunk of size 108544.
   [2.595] Take status was changed to: READY.
   Deleting take t01jqrj756qrvrqaw59zgyxpcrw: True

.. code-block:: shell
   :caption: Example output (chunks enabled)

   $ python3 -m examples.websocket_example_async_iter --chunks
   Found Daisys Speak API version=1 minor=0
   [0.002] Take status was changed to: WAITING.
   [0.023] Take status was changed to: STARTED.
   [0.318] New part being received.
   [0.318] Received audio chunk of size 4096.
   [0.331] Received audio chunk of size 4096.
   [0.344] Received audio chunk of size 4096.
   [0.358] Received audio chunk of size 4096.
   [0.371] Received audio chunk of size 4096.
   [0.384] Received audio chunk of size 4096.
   [0.397] Received audio chunk of size 4096.
   [0.411] Received audio chunk of size 4096.
   [0.424] Received audio chunk of size 4096.
   [0.437] Received audio chunk of size 4096.
   [0.450] Received audio chunk of size 4096.
   [0.463] Received audio chunk of size 4096.
   [0.472] Received audio chunk of size 4096.
   [0.482] Received audio chunk of size 4096.
   [0.492] Received audio chunk of size 4096.
   [0.503] Received audio chunk of size 4096.
   [0.513] Received audio chunk of size 4096.
   [0.523] Received audio chunk of size 4096.
   [0.533] Received audio chunk of size 4096.
   [0.543] Received audio chunk of size 4096.
   [0.553] Received audio chunk of size 4096.
   [0.564] Received audio chunk of size 4096.
   [0.575] Received audio chunk of size 4096.
   [0.584] Received audio chunk of size 4096.
   [0.595] Received audio chunk of size 4096.
   [0.605] Received audio chunk of size 4096.
   [0.615] Received audio chunk of size 4096.
   [0.626] Received audio chunk of size 4096.
   [0.636] Received audio chunk of size 4096.
   [0.646] Received audio chunk of size 1024.
   [1.002] Take status was changed to: PROGRESS_50.
   [1.005] New part being received.
   [1.005] Received audio chunk of size 4096.
   [1.015] Received audio chunk of size 4096.
   [1.024] Received audio chunk of size 4096.
   [1.033] Received audio chunk of size 4096.
   [1.043] Received audio chunk of size 4096.
   [1.053] Received audio chunk of size 4096.
   [1.064] Received audio chunk of size 4096.
   [1.074] Received audio chunk of size 4096.
   [1.084] Received audio chunk of size 4096.
   [1.095] Received audio chunk of size 4096.
   [1.105] Received audio chunk of size 4096.
   [1.115] Received audio chunk of size 4096.
   [1.125] Received audio chunk of size 4096.
   [1.135] Received audio chunk of size 2048.
   [2.641] Take status was changed to: READY.
   Deleting take t01jqrk04k7fhrdgs764bv6h7p1: True


.. literalinclude:: ../../examples/websocket_example_async_iter.py
   :language: python
   :caption: examples/websocket_example_async_iter.py
   :linenos:

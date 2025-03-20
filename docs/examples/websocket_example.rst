Example: Websocket example, synchronous client
==============================================

This example shows:

1. How to open a websocket connection using a context manager.

2. Generate a take, specifying status and audio callbacks.

3. The signature of each of these callbacks and how to interpret their arguments.

4. How to make a request with and without chunks enabled. (Add argument ``--chunks``.)

.. code-block:: shell
   :caption: Example output

   $ python3 -m examples.websocket_example
   Found Daisys Speak API version=1 minor=0
   Status.WAITING
   Status.STARTED
   [0.739s] Received part_id=0 (chunk_id=None) for take_id='t01jqrjc9bfx8z0w6zarf8hcq8y' with audio length 235564
   Read 235564 bytes of wav data, wrote "websocket_part1.wav".
   Status.PROGRESS_50
   [1.166s] Received part_id=1 (chunk_id=None) for take_id='t01jqrjc9bfx8z0w6zarf8hcq8y' with audio length 106540
   Read 106540 bytes of wav data, wrote "websocket_part2.wav".
   [1.166s] Received part_id=2 (chunk_id=None) for take_id='t01jqrjc9bfx8z0w6zarf8hcq8y' with audio length (empty -- done receiving)
   Status.READY
   Deleting take t01jqrjc9bfx8z0w6zarf8hcq8y: True

.. code-block:: shell
   :caption: Example output (chunks enabled)

   $ python3 -m examples.websocket_example --chunks
   Found Daisys Speak API version=1 minor=0
   Status.WAITING
   Status.STARTED
   [0.311s] Received part_id=0 (chunk_id=0) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4140
   [0.323s] Received part_id=0 (chunk_id=1) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.335s] Received part_id=0 (chunk_id=2) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.347s] Received part_id=0 (chunk_id=3) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.359s] Received part_id=0 (chunk_id=4) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.372s] Received part_id=0 (chunk_id=5) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.385s] Received part_id=0 (chunk_id=6) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.396s] Received part_id=0 (chunk_id=7) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.409s] Received part_id=0 (chunk_id=8) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.421s] Received part_id=0 (chunk_id=9) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.433s] Received part_id=0 (chunk_id=10) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.445s] Received part_id=0 (chunk_id=11) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.457s] Received part_id=0 (chunk_id=12) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.469s] Received part_id=0 (chunk_id=13) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.479s] Received part_id=0 (chunk_id=14) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.489s] Received part_id=0 (chunk_id=15) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.500s] Received part_id=0 (chunk_id=16) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.510s] Received part_id=0 (chunk_id=17) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.520s] Received part_id=0 (chunk_id=18) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.530s] Received part_id=0 (chunk_id=19) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.540s] Received part_id=0 (chunk_id=20) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.550s] Received part_id=0 (chunk_id=21) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.560s] Received part_id=0 (chunk_id=22) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.570s] Received part_id=0 (chunk_id=23) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.580s] Received part_id=0 (chunk_id=24) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.590s] Received part_id=0 (chunk_id=25) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.600s] Received part_id=0 (chunk_id=26) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.610s] Received part_id=0 (chunk_id=27) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.621s] Received part_id=0 (chunk_id=28) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.631s] Received part_id=0 (chunk_id=29) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 2560
   [0.631s] Received part_id=0 (chunk_id=30) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length (empty -- done receiving)
   Read 121388 bytes of wav data, wrote "websocket_part1.wav".
   Status.PROGRESS_50
   [0.979s] Received part_id=1 (chunk_id=0) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4140
   [0.989s] Received part_id=1 (chunk_id=1) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [0.998s] Received part_id=1 (chunk_id=2) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.007s] Received part_id=1 (chunk_id=3) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.018s] Received part_id=1 (chunk_id=4) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.028s] Received part_id=1 (chunk_id=5) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.038s] Received part_id=1 (chunk_id=6) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.048s] Received part_id=1 (chunk_id=7) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.058s] Received part_id=1 (chunk_id=8) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.069s] Received part_id=1 (chunk_id=9) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.079s] Received part_id=1 (chunk_id=10) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.089s] Received part_id=1 (chunk_id=11) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.100s] Received part_id=1 (chunk_id=12) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 4096
   [1.109s] Received part_id=1 (chunk_id=13) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length 2048
   [1.110s] Received part_id=1 (chunk_id=14) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length (empty -- done receiving)
   Read 55340 bytes of wav data, wrote "websocket_part2.wav".
   [1.110s] Received part_id=2 (chunk_id=0) for take_id='t01jqrjq6xs1vbkdm1493e60gv2' with audio length (empty -- done receiving)
   Status.READY
   Deleting take t01jqrjq6xs1vbkdm1493e60gv2: True


.. literalinclude:: ../../examples/websocket_example.py
   :language: python
   :caption: examples/websocket_example.py
   :linenos:

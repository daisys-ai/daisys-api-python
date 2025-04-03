Example: Websocket example, asynchronous client
===============================================

This example shows:

1. How to open a websocket connection using an async context manager.

2. Generate a take, specifying status and audio callbacks.

3. The signature of each of these callbacks and how to interpret their arguments.

4. How to make a request with and without chunks enabled. (Add argument ``--chunks``.)

.. code-block:: shell
   :caption: Example output

   $ python3 -m examples.websocket_example_async
   Found Daisys Speak API version=1 minor=0
   Status.WAITING
   Status.STARTED
   [0.751s] Received part_id=0 (chunk_id=None) for take_id='t01jqrjedpjb11hpg40h9kkydpk' with audio length 245804
   appending audio 245804
   Read 245804 bytes of wav data, wrote "websocket_part1.wav".
   Status.PROGRESS_50
   [1.183s] Received part_id=1 (chunk_id=None) for take_id='t01jqrjedpjb11hpg40h9kkydpk' with audio length 112684
   appending audio 112684
   Read 112684 bytes of wav data, wrote "websocket_part2.wav".
   [1.184s] Received part_id=2 (chunk_id=None) for take_id='t01jqrjedpjb11hpg40h9kkydpk' with audio length (empty -- done receiving)
   stream done
   Status.READY
   Deleting take t01jqrjedpjb11hpg40h9kkydpk: True

.. code-block:: shell
   :caption: Example output (chunks enabled)

   $ python3 -m examples.websocket_example_async --chunks
   Found Daisys Speak API version=1 minor=0
   Status.WAITING
   Status.STARTED
   [0.311s] Received part_id=0 (chunk_id=0) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4140
   appending audio 4140
   [0.324s] Received part_id=0 (chunk_id=1) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 8236
   [0.338s] Received part_id=0 (chunk_id=2) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 12332
   [0.351s] Received part_id=0 (chunk_id=3) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 16428
   [0.365s] Received part_id=0 (chunk_id=4) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 20524
   [0.378s] Received part_id=0 (chunk_id=5) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 24620
   [0.389s] Received part_id=0 (chunk_id=6) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 28716
   [0.399s] Received part_id=0 (chunk_id=7) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 32812
   [0.409s] Received part_id=0 (chunk_id=8) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 36908
   [0.419s] Received part_id=0 (chunk_id=9) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 41004
   [0.429s] Received part_id=0 (chunk_id=10) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 45100
   [0.439s] Received part_id=0 (chunk_id=11) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 49196
   [0.449s] Received part_id=0 (chunk_id=12) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 53292
   [0.459s] Received part_id=0 (chunk_id=13) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 57388
   [0.469s] Received part_id=0 (chunk_id=14) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 61484
   [0.479s] Received part_id=0 (chunk_id=15) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 65580
   [0.489s] Received part_id=0 (chunk_id=16) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 69676
   [0.500s] Received part_id=0 (chunk_id=17) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 73772
   [0.510s] Received part_id=0 (chunk_id=18) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 77868
   [0.520s] Received part_id=0 (chunk_id=19) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 81964
   [0.530s] Received part_id=0 (chunk_id=20) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 86060
   [0.540s] Received part_id=0 (chunk_id=21) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 90156
   [0.550s] Received part_id=0 (chunk_id=22) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 94252
   [0.560s] Received part_id=0 (chunk_id=23) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 98348
   [0.570s] Received part_id=0 (chunk_id=24) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 102444
   [0.580s] Received part_id=0 (chunk_id=25) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 106540
   [0.590s] Received part_id=0 (chunk_id=26) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 110636
   [0.600s] Received part_id=0 (chunk_id=27) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 114732
   [0.610s] Received part_id=0 (chunk_id=28) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 118828
   [0.620s] Received part_id=0 (chunk_id=29) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 2048
   appending audio 120876
   [0.621s] Received part_id=0 (chunk_id=30) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length (empty -- done receiving)
   part done
   Read 120876 bytes of wav data, wrote "websocket_part1.wav".
   Status.PROGRESS_50
   [0.976s] Received part_id=1 (chunk_id=0) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4140
   appending audio 4140
   [0.985s] Received part_id=1 (chunk_id=1) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 8236
   [0.995s] Received part_id=1 (chunk_id=2) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 12332
   [1.004s] Received part_id=1 (chunk_id=3) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 16428
   [1.014s] Received part_id=1 (chunk_id=4) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 20524
   [1.024s] Received part_id=1 (chunk_id=5) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 24620
   [1.034s] Received part_id=1 (chunk_id=6) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 28716
   [1.044s] Received part_id=1 (chunk_id=7) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 32812
   [1.054s] Received part_id=1 (chunk_id=8) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 36908
   [1.064s] Received part_id=1 (chunk_id=9) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 41004
   [1.074s] Received part_id=1 (chunk_id=10) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 45100
   [1.084s] Received part_id=1 (chunk_id=11) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 49196
   [1.095s] Received part_id=1 (chunk_id=12) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 4096
   appending audio 53292
   [1.105s] Received part_id=1 (chunk_id=13) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length 1024
   appending audio 54316
   [1.105s] Received part_id=1 (chunk_id=14) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length (empty -- done receiving)
   part done
   Read 54316 bytes of wav data, wrote "websocket_part2.wav".
   [1.105s] Received part_id=2 (chunk_id=0) for take_id='t01jqrjh3yrbzpd79q1nprcrbjy' with audio length (empty -- done receiving)
   stream done
   Status.READY
   Deleting take t01jqrjh3yrbzpd79q1nprcrbjy: True


.. literalinclude:: ../../examples/websocket_example_async.py
   :language: python
   :caption: examples/websocket_example_async.py
   :linenos:

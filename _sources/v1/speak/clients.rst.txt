
Daisys API clients
==================

These objects should not be instantiated directly, but accessed through the DaisysAPI
top-level factory object.

The synchronous client makes requests using synchronous, blocking calls.  The asynchronous
client uses an asyncio event loop.  You should choose whichever implementation is most
convenient for your application.

.. automodule:: daisys.v1.speak.sync_client
   :members:
   :undoc-members:

.. automodule:: daisys.v1.speak.async_client
   :members:
   :undoc-members:

Daisys API examples
===================

The following examples can be used to see how the Daisys API client library for Python can
be used.

.. code-block:: shell
   :caption: Running examples
   :linenos:

   export DAISYS_EMAIL=user@example.com DAISYS_PASSWORD='<my password>'
   python3 -m venv venv
   . venv/bin/activate
   python3 -m pip install daisys
   python3 -m daisys.examples.hello_daisys

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples/hello_daisys.rst
   examples/hello_daisys_async.rst
   examples/tokens_example.rst
   examples/curl_example.rst

Getting started
===============

Once you confirm your email address, you will be provided access to the Daisys API via the
email account you registered.  You have also already provided a password.

    If you have not already done so, the first step to enable your account is to set your
    password using the following ``curl`` command::

      curl -X POST https://api.daisys.ai/auth/set_password \
        -H "Content-Type: application/json" \
        -d '{"email": "<email>", "password": "<provided_password>", "new_password": "YOUR NEW PASSWORD"}'

    The temporary password for ``<provided_password>`` should have been received by email.
    If you did not receive it, please don't hesitate to get in touch at api@daisys.ai.

At this point the API can be used.  The steps are:

1. Authentication: provide your email and password to get an access token.
2. List the models that are available to you.
3. Create a voice for a model.
4. Create a "take" with that voice. (Request some speech.)
5. Download the audio for that take.

All these steps are taken care of by the Python client library.  Therefore, first we show
briefly how to use the library, and secondly we show how to accomplish the above steps
manually from the command line using ``curl``.  This can be useful if you want to build
your own client in your preferred language.

Depending on your needs, you may prefer not to provide the email and password every time
the API is used.  It is also possible refresh the access token using the provided refresh
token, thereby continuing a previous session without logging out.

For more on using the Python client library, see :doc:`examples`.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started_python.rst
   getting_started_cli.rst

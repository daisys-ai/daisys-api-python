"""High-level factory interface to instantiate a sync or async client object to interact with the Daisys API."""

import os

DAISYS_API_URL = os.environ.get('DAISYS_API_URL', 'https://api.daisys.ai')
DAISYS_AUTH_URL = os.environ.get('DAISYS_AUTH_URL', DAISYS_API_URL)

class DaisysAPI:
    """Factory class to get a Daisys API client.

    This class is intended (but not required) to be used in a ``with`` or ``async with`` clause.
    """
    def __init__(self, product='speak', version='v1',
                 email: str=None, password: str=None,
                 access_token: str=None, refresh_token: str=None,
                 daisys_url: str=DAISYS_API_URL, auth_url: str=DAISYS_AUTH_URL):
        """Initialize the factory object for a given product and version.

        This object is intended to be short lived, only used to provide a client object.

        Login or token details be be optionally provided.  If they are not provided here,
        they may be later provided to the client by calling client.login().

        Args:
            product: The product to retrieve a client for.
            version: The version of the product to retrieve a client for.
            email: Optionally, email to use for logging in.
            password: Optionally, password to use for logging in.
            access_token: Optionally, access token to use.  Specify if login was already performed.
            refresh_token: Optionally, refresh token to use.  Specify if login was already performed.
            daisys_url: For overriding default API URL, usually not needed.
            auth_url: For overriding default authentication URL, usually not needed.

        """
        self.daisys_url = daisys_url
        self.auth_url = auth_url
        self.version = version
        self.product = product
        self.email = email
        self.password = password
        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_client(self) -> 'DaisysSyncSpeakClientV1':
        """Retrieve a client for synchronous usage of the Daisys Speak API."""

        auth_url = self.auth_url + f'/auth'
        product_url = self.daisys_url + f'/{self.version}/{self.product}'
        if self.version == 'v1' and self.product == 'speak':
            product_url = self.daisys_url + f'/{self.version}/{self.product}'
            from .v1.speak import DaisysSyncSpeakClientV1
            return DaisysSyncSpeakClientV1(auth_url=auth_url,
                                           product_url=product_url,
                                           email=self.email,
                                           password=self.password,
                                           access_token=self.access_token,
                                           refresh_token=self.refresh_token)
        else:
            raise NotImplementedError(f'Product {self.product} version {self.version} unknown.')

    def get_async_client(self) -> 'DaisysAsyncSpeakClientV1':
        """Retrieve a client for asynchronous usage of the Daisys Speak API."""
        auth_url = self.auth_url + f'/auth'
        product_url = self.daisys_url + f'/{self.version}/{self.product}'
        if self.version == 'v1' and self.product == 'speak':
            product_url = self.daisys_url + f'/{self.version}/{self.product}'
            from .v1.speak import DaisysAsyncSpeakClientV1
            return DaisysAsyncSpeakClientV1(auth_url=auth_url,
                                            product_url=product_url,
                                            email=self.email,
                                            password=self.password,
                                            access_token=self.access_token,
                                            refresh_token=self.refresh_token)
        else:
            raise NotImplementedError(f'Product {self.product} version {self.version} unknown.')

    def __enter__(self) -> 'DaisysSyncSpeakClientV1':
        self.client = self.get_client()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    async def __aenter__(self) -> 'DaisysAsyncSpeakClientV1':
        self.client = self.get_async_client()
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()

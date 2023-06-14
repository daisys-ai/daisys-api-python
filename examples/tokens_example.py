import os, asyncio, json
from daisys import DaisysAPI
from daisys.v1.speak import VoiceGender, SimpleProsody, DaisysTakeGenerateError, HTTPStatusError

# This example shows how to use access and refresh tokens instead of a username and email
# address for authenticating with the Daisys API.

# Override DAISYS_EMAIL and DAISYS_PASSWORD with your details!
EMAIL = os.environ.get('DAISYS_EMAIL', 'user@example.com')
PASSWORD = os.environ.get('DAISYS_PASSWORD', 'pw')

def load_tokens():
    """A function to access and refresh tokens from a local file.  In practice you might
    store this somewhere more global like in a database, to re-use between sessions."""
    try:
        with open('daisys_tokens.json') as tokens_file:
            tokens = json.load(tokens_file)
            print('Loaded tokens from "daisys_tokens.json".')
            return tokens['access_token'], tokens['refresh_token']
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

ACCESS_TOKEN, REFRESH_TOKEN = load_tokens()

def store_tokens(access_token: str, refresh_token: str):
    """A function to store the access and refresh tokens to a local file.  In practice you
    might store this somewhere like in a database or larger configuration.

    """
    with open('daisys_tokens.json', 'w') as tokens_file:
        json.dump({'access_token': access_token,
                   'refresh_token': refresh_token},
                  tokens_file)
        print('Stored new tokens in "daisys_tokens.json".')

def initial_login():
    """Initially retrieve access and refresh tokens through a normal login."""
    # Initial login is only required if we don't have an access token yet.
    print(f'Initial login, attempting to log in with {EMAIL} to retrieve an access token.')
    with DaisysAPI('speak', email=EMAIL, password=PASSWORD) as speak:
        # Say what should happen when tokens are retrieved or changed.
        speak.token_callback = store_tokens

        # Explicit login is only necessary if no other operations occur here, otherwise
        # login is automatic.
        speak.login()

        # Login enables auto-logout.  Disable it so that the token will not be invalidated.
        speak.auto_logout = False

        print('Run again to use stored access token!')

def subsequent_login():
    """In subsequent uses, the previously stored access token can be used directly."""
    print('Using previously stored access token.')
    with DaisysAPI('speak', access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN) as speak:
        speak.token_callback = store_tokens

        # Here we are just showing how to authenticate with the Daisys API using an access
        # token instead of the password, so we just list some voices.  See hello_daisys.py
        # for an example of how to generate audio!

        # Get a list of all voices
        voices = speak.get_voices()
        print('Found voices:', [voice.name for voice in voices])

def main():
    if ACCESS_TOKEN:
        subsequent_login()
    else:
        initial_login()

if __name__=='__main__':
    try:
        main()
    except HTTPStatusError as e:
        try:
            print(f'HTTP error status {e.response.status_code}: {e.response.json()["detail"]}, {e.request.url}')
        except:
            print(f'HTTP error status {e.response.status_code}: {e.response.text}, {e.request.url}')

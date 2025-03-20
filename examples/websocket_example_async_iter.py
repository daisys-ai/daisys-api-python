import sys, os, asyncio, time
from typing import Optional
from daisys import DaisysAPI
from daisys.v1.speak import (DaisysWebsocketGenerateError, HTTPStatusError, Status, TakeResponse,
                             StreamOptions, StreamMode)

# Override DAISYS_EMAIL and DAISYS_PASSWORD with your details!
EMAIL = os.environ.get('DAISYS_EMAIL', 'user@example.com')
PASSWORD = os.environ.get('DAISYS_PASSWORD', 'pw')

# Please see tokens_example.py for how to use an access token instead of a password.

async def main(chunks):
    async with DaisysAPI('speak', email=EMAIL, password=PASSWORD) as speak:
        print('Found Daisys Speak API', await speak.version())

        # A buffer to receive parts; we initialize with a single empty bytes()
        # because we will use it to accumulate chunks of the current wav file
        # there.  In total we will end with a list of wav files, one for each
        # part.  Parts are bits of speech, usually full sentences, that end with
        # silence.
        audio_wavs = [bytes()]

        # Assume at least one voice is available
        voice = (await speak.get_voices())[0]

        async with speak.websocket(voice_id=voice.voice_id) as ws:
            # Time the latency from when we submit the request until each part
            # is received.
            t0 = time.time()

            # Submit a request to generate a take over the websocket connection.
            generate_request_id = await ws.generate_take(
                voice_id=voice.voice_id,
                text='Hello from Daisys websockets! How may I help you?',

                # Optional
                stream_options=StreamOptions(mode=StreamMode.CHUNKS) if chunks else None,
            )

            # The use of an interator simplifies streaming, here we show how to
            # get both status and audio chunks from the same iterator.
            async for take_id, take, header, audio in ws.iter_request(generate_request_id):
                now = time.time() - t0
                if take is not None:
                    print(f'[{now:.03f}] Take status was changed to: {take.status.name}.')
                if header is not None:
                    print(f'[{now:.03f}] New part being received.')
                if audio is not None:
                    print(f'[{now:.03f}] Received audio chunk of size {len(audio)}.')

        # Delete the take
        if take_id:
            print(f'Deleting take {take_id}:', await speak.delete_take(take_id))

if __name__=='__main__':
    try:
        asyncio.run(main('--chunks' in sys.argv[1:]))
    except HTTPStatusError as e:
        try:
            print(f'HTTP error status {e.response.status_code}: {e.response.json()["detail"]}, {e.request.url}')
        except:
            print(f'HTTP error status {e.response.status_code}: {e.response.text}, {e.request.url}')

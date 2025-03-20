import os, asyncio
from daisys import DaisysAPI
from daisys.v1.speak import VoiceGender, SimpleProsody, DaisysTakeGenerateError, HTTPStatusError

# Override DAISYS_EMAIL and DAISYS_PASSWORD with your details!
EMAIL = os.environ.get('DAISYS_EMAIL', 'user@example.com')
PASSWORD = os.environ.get('DAISYS_PASSWORD', 'pw')

# Please see tokens_example.py for how to use an access token instead of a password.

def main():
    with DaisysAPI('speak', email=EMAIL, password=PASSWORD) as speak:
        print('Found Daisys Speak API', speak.version())

        # The following is an example of how to use the Daisys API for generating a voice
        # and then using it in a speech generation task.  The API generates "takes"
        # representing one or more sentences from a speaker.  The same example is possible
        # with the synchronous client, where the 'await' keywords should be removed.

        # Get a list of all voices
        voices = speak.get_voices()
        print('Found voices:', [voice.name for voice in voices])

        # Choose one
        if len(voices) > 0:
            voice = voices[-1]
            delete_voice = False
        else:
            print('Not enough voices!')

            # Okay, let's generate a voice.

            # First we need to know the model.
            models = speak.get_models()
            if len(models) > 0:
                model = models[0]
                print(f'Using model "{model.displayname}"')
            else:
                print('No models found!')
                return

            print('Generating a voice.')
            voice = speak.generate_voice(name='Lucy', gender=VoiceGender.FEMALE, model=model.name)
            delete_voice = True

            # Try to modify the voice's name
            voice.name = 'Sally'
            speak.update_voice(**dict(voice))
            voice = speak.get_voice(voice.voice_id)

        # Now we have a voice.
        print(voice.name, 'speaking!')

        try:
            # Synthesize some audio from text
            take = speak.generate_take(voice_id=voice.voice_id, text="Hello there, I am Daisys!",
                                       prosody=SimpleProsody(pace=-3, pitch=2, expression=10))
        except DaisysTakeGenerateError as e:
            print('Error generating take:', str(e))
            return

        # The take is now READY.  We get its associated audio file.  We provide a filename
        # so that it gets written to disk, but it is also returned.
        audio_wav = speak.get_take_audio(take.take_id, file='hello_daisys.mp3', format='mp3')

        print(f'Read {len(audio_wav)} bytes of wav data, wrote "hello_daisys.wav".')

        # Let's check if we can get info on it again.
        check_take = speak.get_take(take.take_id)
        print('Checking take:', check_take == take)

        # Let's check if we can find it in the most recent 5 takes.
        last_5_takes = speak.get_takes(length=5)
        print('Checking list of takes:', take.take_id in [t.take_id for t in last_5_takes])

        # Delete the take
        print(f'Deleting take {take.take_id}:', speak.delete_take(take.take_id))

        # Delete the voice
        if delete_voice:
            print(f'Deleting voice {voice.voice_id}:', speak.delete_voice(voice.voice_id))

if __name__=='__main__':
    try:
        main()
    except HTTPStatusError as e:
        try:
            print(f'HTTP error status {e.response.status_code}: {e.response.json()["detail"]}, {e.request.url}')
        except:
            print(f'HTTP error status {e.response.status_code}: {e.response.text}, {e.request.url}')

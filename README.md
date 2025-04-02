# Daisys API

This library wraps the Daisys API for text-to-speech and voice generation services.

Have your product talking in seconds!


```python
    from daisys import DaisysAPI
    from daisys.v1.speak import SimpleProsody

    with DaisysAPI('speak', email='user@example.com', password='pw') as speak:
        voice = speak.get_voices()[-1]
        print(f"{voice.name} speaking!")
        take = speak.generate_take(voice_id=voice.voice_id, text="Hello there, I am Daisys!",
                                   prosody=SimpleProsody(pace=-3, pitch=2, expression=10))
        audio_wav = speak.get_take_audio(take.take_id, filename='hello_daisys.wav')
```

This library uses `pydantic` and `httpx` as the main dependencies.  It can be
used with or without ``asyncio``.

Please visit the [online documentation](https://daisys-ai.github.io/daisys-api-python/)
for information on how to use the Daisys API from Python, or from any language using the
documented REST endpoints.

A product of [Daisys AI](https://daisys.ai).

The software is licensed with the MIT license, as detailed in LICENSE.

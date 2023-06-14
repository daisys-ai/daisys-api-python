#!/bin/bash

# The following is an example of how to use the Daisys API for generating a voice and then
# using it in a speech generation task using the "curl" program.  The API generates
# "takes" representing one or more sentences from a speaker.

# This program downloads the resulting .wav file and tries to play it using "aplay" if
# that program is available.

set -e  # Stop if we hit any problems along the way.

EMAIL="${DAISYS_EMAIL:=user@example.com}"
PASSWORD="${DAISYS_PASSWORD:=example_password}"

DAISYS_AUTH="${DAISYS_AUTH_URL:=https://api.daisys.ai}"
DAISYS="${DAISYS_API_URL:=https://api.daisys.ai}"
API="$DAISYS/v1"
SPEAK="$API/speak"

TOKEN=$(curl -s -X POST -H 'Content-Type: application/json' -d '{"email": "'$EMAIL'", "password": "'$PASSWORD'"}' $DAISYS_AUTH/auth/login | jq -r ".access_token")

AUTH="Authorization: Bearer $TOKEN"

# Some functions for authenticated GET and POST methods using curl.
speak_get() {
    echo "GET $SPEAK/$1" >/dev/stderr
    curl -s -L -H "$AUTH" "$SPEAK/$1"
}
speak_post() {
    echo "POST $SPEAK/$1: $2" >/dev/stderr
    curl -s -H "Content-Type: application/json" -H "$AUTH" -d "$2" "$SPEAK/$1"
}

VERSION=$(curl -s $API/speak/version)
echo 'Found Daisys Speak API ' $VERSION

# Get a list of all voices, select the last one.
VOICE=$(speak_get voices | jq '.[-1]')
if [ "$VOICE" = null ]; then
    echo No voices found.
    MODEL=$(speak_get models | jq '.[-1]')
    if [ "$MODEL" = null ]; then
        echo No models found.
        exit 1
    fi
    echo Using model $(echo $MODEL | jq .displayname)
    echo Generating a voice.
    VOICE=$(speak_post voices/generate '{"name": "Tina", "gender": "female", "model": '$(echo $MODEL | jq .name)'}')
fi
echo "$(echo $VOICE | jq .name) is speaking!"
VOICE_ID="$(echo $VOICE | jq .voice_id)"

TAKE=$(speak_post takes/generate '{"voice_id": '$VOICE_ID', "text": "Hello there, I am Daisys!", "prosody": {"pace": -8, "pitch": 2, "expression": 8}}')
TAKE_ID="$(echo $TAKE | jq -r .take_id)"
echo "Take is $(echo $TAKE | jq .status)."
while [ $(echo $TAKE | jq -r .status) != 'ready' ] && [ $(echo $TAKE | jq -r .status) != 'error' ]; do
    sleep 0.5
    TAKE=$(speak_get takes/$TAKE_ID)
    echo "Take is $(echo $TAKE | jq .status)."
done

echo "Getting audio!"
speak_get takes/$TAKE_ID/wav > hello_daisys.wav
echo "Wrote 'hello_daisys.wav'."

# Play the audio if we have aplay (Linux), otherwise just print a nice message.
if which aplay >/dev/null; then
    aplay hello_daisys.wav
else
    echo "aplay not found, but audio was written to 'hello_daisys.wav'."
fi

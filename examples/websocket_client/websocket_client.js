import { PartAudioPlayer } from './part_audio_player.js';
import { ChunkAudioPlayer } from './chunk_audio_player.js';
import { WebsocketStream } from './websocket_stream.js';

// Spinner interaction when buttons are clicked
const buttonSpinnerPairs = [
  { buttonId: 'connectButtonPartStream', spinnerId: 'spinnerPartStream' },
  { buttonId: 'connectButtonChunkStream', spinnerId: 'spinnerChunkStream' }
];

function setupSpinners() {
  buttonSpinnerPairs.forEach(({ buttonId, spinnerId }) => {
    const button = document.getElementById(buttonId);
    const spinner = document.getElementById(spinnerId);
    button.addEventListener('click', () => {
      spinner.classList.remove('visually-hidden');
      button.classList.add('active');
    });
  });
}

function removeSpinners() {
  buttonSpinnerPairs.forEach(({ buttonId, spinnerId }) => {
    const button = document.getElementById(buttonId);
    const spinner = document.getElementById(spinnerId);
    spinner.classList.add('visually-hidden');
    button.classList.remove('active');
  });
}

setupSpinners();

// The backend determines which voice we use
let voice_id = await (await fetch('/voice_id')).text();

// Functions for interacting with the HTML display
function updateWebsocketStatus(message) {
  let s = document.getElementById("ws_status");
  let b = document.getElementById("reconnect");
  let msg = message.toLowerCase();
  window.m = msg;
  if (msg.includes('error') || msg.includes('disconnect')
      || msg.includes('reconnect') || msg.includes('fail')) {
    s.classList.remove('text-success');
    s.classList.add('text-danger');
    if (msg.includes('reconnect'))
      b.classList.add('visually-hidden');
    else
      b.classList.remove('visually-hidden');
  } else {
    s.classList.remove('text-danger');
    s.classList.add('text-success');
    b.classList.add('visually-hidden');
  }
  s.textContent = message;
}
function updateTakeStatus(message, take_id) {
  document.getElementById("take_status").textContent = message;
}
function updateTiming(time) {
  if (time) {
    removeSpinners();
    document.getElementById("timing").textContent = time.toFixed(3) + ' seconds.';
  } else
    document.getElementById("timing").textContent = '';
}
function clearEvents() {
  document.getElementById("event").innerHTML = '';
}
function updateEvent(...args) {
  console.log(...args);
  window.a = args;
  let msg = args.map(item => (item?.byteLength ? item?.byteLength
                             : typeof item === 'string' ? item : JSON.stringify(item))).join(' ');
  let event_log = document.getElementById("event");
  event_log.innerHTML += '<br/>' + msg;
  event_log.scrollTop = event_log.scrollHeight;
}
function parseTakeStatus(message) {
  let msg = JSON.parse(message);
  if ('data' in msg)
    updateTakeStatus(msg.data.status);
  else
    updateTakeStatus(`[${msg.status}] ${msg.message}`);
}

// Obtain the WebSocket connection.
let ws;
try {
  ws = new WebsocketStream("/ws_url", {
    onconnectionstatus: (status) => updateWebsocketStatus(status),
  });
  document.getElementById("reconnect").addEventListener("click", ws.connector.connect.bind(ws.connector));
} catch {
  updateWebsocketStatus('connection error');
}

// Generate unique request IDs.
let requestCounter = 1;

// Helper function to send a /take/generate command.
function takeGenerateCommand(text, voice_id, chunking, request_id) {
  const message = {
    command: "/take/generate",
    request_id: request_id,
    data: {
      text: text,
      voice_id: voice_id
    }
  };
  if (chunking) {
    message.stream = {mode: 'chunks'};
  }
  return message;
}



// EXAMPLE 1: Requesting and playing a stream of parts
document.getElementById("connectButtonPartStream").addEventListener("click", async () => {
  const reqId = requestCounter++;
  clearEvents();

  // Register a simple (non‑chunked) stream handler for this request.
  // We use two sentences to demonstrate how they are sequenced during playback.
  const message = takeGenerateCommand(
    "The quick brown fox jumps over the lazy dog. Then he trips and falls.",
    voice_id, false, reqId);

  // In this example we show how to play back each part one after the other as a
  // individual audio sources.
  const audioPlayer = new PartAudioPlayer();

  // Send a message and process all incoming status and audio messages in the same loop.
  let messageStream;
  try {
    messageStream = ws.messageStream(message);
  } catch {
    removeSpinners();
    return;
  }
  let take_id = null;
  let now = Date.now();
  let first = true;
  updateTiming();

  try {
    for await (const [info, prefix, audio] of messageStream) {
      // Handle take status messages (for take, or example take if handling a voice generate request)
      if (info) {
        updateEvent("Got status:", info);
        if (info.data) {
          take_id = info.data.example_take_id || info.data.take_id;
          updateTakeStatus(info.data.status, take_id);
        } else {
          updateTakeStatus(`[${info.status}] ${info.message}`);
        }
      }

      // Handle incoming parts or chunks
      else {
        if ([null, undefined].includes(prefix.chunk_id))
          updateEvent("Got part:", prefix, 'audio:', audio);
        else
          updateEvent("Got chunk:", prefix, 'audio:', audio);

        if (first) {
          // Record time to first chunk
          updateTiming((Date.now() - now)/1000);
          first = false;
        }
        audioPlayer.playAudio(prefix, audio);
      }
    }
    audioPlayer.endStream();
  } catch {
    setTimeout(removeSpinners, 500);
  }

  if (take_id)
    updateEvent('Done message stream for', take_id);
  else
    updateEvent('No status messages arrived.');
});



// EXAMPLE 2: Requesting and playing a stream of chunks
document.getElementById("connectButtonChunkStream").addEventListener("click", async () => {
  const reqId = requestCounter++;
  clearEvents();

  // Register a simple (non‑chunked) stream handler for this request.
  // We use two sentences to demonstrate how they are sequenced during playback.
  const message = takeGenerateCommand(
    "The quick brown fox jumps over the lazy dog. Then he trips and falls.",
    voice_id, true, reqId);

  // In this example we show how to play back each part one after the other as a
  // individual audio sources.
  const audioPlayer = new ChunkAudioPlayer();

  // Send a message and process all incoming status and audio messages in the same loop.
  let messageStream;
  messageStream = ws.messageStream(message);
  let take_id = null;
  let now = Date.now();
  let first = true;
  updateTiming();

  try {
    for await (const [info, prefix, audio] of messageStream) {
      // Handle take status messages (for take, or example take if handling a voice generate request)
      if (info) {
        updateEvent("Got status:", info);
        if (info.data) {
          take_id = info.data.example_take_id || info.data.take_id;
          updateTakeStatus(info.data.status, take_id);
        } else {
          updateTakeStatus(`[${info.status}] ${info.message}`);
        }
      }

      // Handle incoming parts or chunks
      else {
        if ([null, undefined].includes(prefix.chunk_id))
          updateEvent("Got part:", prefix, 'audio:', audio);
        else
          updateEvent("Got chunk:", prefix, 'audio:', audio);

        if (first) {
          // Record time to first chunk
          updateTiming((Date.now() - now)/1000);
          first = false;
        }
        audioPlayer.playAudio(prefix, audio);
      }
    }
    audioPlayer.endStream();
  }
  catch {
    setTimeout(removeSpinners, 500);
  }

  if (take_id)
    updateEvent('Done message stream for', take_id);
  else
    updateEvent('No status messages arrived.');
});

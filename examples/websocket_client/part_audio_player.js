import { parseWavHeader } from './audio_utils.js';

export class PartAudioPlayer {
  constructor () {
    this.audioContext = null;

    // A queue of audio sources to play. The first item will be the active
    // source, removed when it's done playing.
    this.sources = [];
  }

  playAudio(prefix, audio) {
    // This handler supports parts only, so we assume chunk_id is null and that a
    // header is included.  In that case we can just deliver it to the audio
    // context as-is, but first need to create the audio context with the correct
    // sample rate.
    let header = parseWavHeader(audio);
    if (!this.audioContext || this.audioContext.sampleRate != header.sampleRate) {
      this.audioContext = new AudioContext({sampleRate: header.sampleRate});
    }

    // For non-chunked streams, we expect the complete audio file in one chunk,
    // so just create a source directly and put it on the queue for playback.
    let sources = this.sources;
    this.audioContext.decodeAudioData(audio)
      .then(audioBuffer => {
        const first = (sources.length == 0);
        const source = this.audioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(this.audioContext.destination);
        source.onended = this.playNext.bind(this);
        sources.push(source);
        if (first)
          source.start();
      })
      .catch(err => {
        console.error("SimpleStreamHandler: Error decoding audio:", err);
      });
  }

  playNext() {
    this.sources.shift();
    if (this.sources.length > 0)
      this.sources[0].start();
  }

  endStream() {
  }
}

import {parseWavHeader, decodePCM} from './audio_utils.js';

export class ChunkAudioPlayer {
  constructor() {
    this.audioContext = null;
    this.buffer = [];            // Holds decoded PCM samples (floats).
    this.isStreaming = false;    // Indicates whether streaming has started.
    this.scriptNode = null;      // The ScriptProcessorNode for streaming.
    this.headerParsed = false;   // Whether we've parsed the WAV header.
    this.headerInfo = null;      // Parsed header info (sampleRate, channels, etc.)
  }

  /**
   * Called for each incoming chunk.
   * For the first chunk of each part, parse the WAV header.
   */
  playAudio(prefix, audio) {
    if ([0, null, undefined].includes(prefix.chunk_id)) {
      this.headerInfo = parseWavHeader(audio);
      this.headerParsed = true;
      if (!this.audioContext || this.audioContext.sampleRate != this.headerInfo.sampleRate) {
        this.audioContext = new AudioContext({sampleRate: this.headerInfo.sampleRate});
      }

      // Remove the header bytes.
      audio = audio.slice(this.headerInfo.headerSize);
    }
    const samples = decodePCM(audio, this.headerInfo.bitsPerSample);
    this.buffer.push(...samples);
    if (!this.isStreaming) {
      this.startStreaming();
    }
  }

  startStreaming() {
    this.isStreaming = true;
    // Create a ScriptProcessorNode (deprecated; consider AudioWorklet for production).
    this.scriptNode = this.audioContext.createScriptProcessor(4096, 1, 1);
    this.scriptNode.onaudioprocess = (event) => {
      const output = event.outputBuffer.getChannelData(0);
      for (let i = 0; i < output.length; i++) {
        output[i] = this.buffer.length > 0 ? this.buffer.shift() : 0;
      }
    };
    this.scriptNode.connect(this.audioContext.destination);
    console.log("ChunkStreamHandler: Streaming started.");
  }

  endStream() {
    // Allow a short delay for buffered audio to play before disconnecting.
    if (this.scriptNode) {
      if (this.buffer.length <  this.audioContext.sampleRate)
        setTimeout(() => {
          this.scriptNode.disconnect();
          console.log("ChunkStreamHandler: Streaming ended.");
        }, 1000);
      else
        setTimeout(this.endStream, 1000);
    }
  }
}

// audioUtils.js

export function parseWavHeader(arrayBuffer) {
  const dataView = new DataView(arrayBuffer);
  // For standard PCM WAV, "RIFF" at byte 0 and "WAVE" at byte 8.
  const numChannels = dataView.getUint16(22, true);
  const sampleRate = dataView.getUint32(24, true);
  const bitsPerSample = dataView.getUint16(34, true);
  // Assume a 44-byte header.
  const headerSize = 44;
  return { numChannels, sampleRate, bitsPerSample, headerSize };
}


/**
 * Decodes PCM data (assumes 16-bit PCM) to a Float32Array.
 */
export function decodePCM(arrayBuffer, bitsPerSample) {
  if (bitsPerSample === 16) {
    const dataView = new DataView(arrayBuffer);
    const numSamples = arrayBuffer.byteLength / 2;
    const samples = new Float32Array(numSamples);
    for (let i = 0; i < numSamples; i++) {
      let sample = dataView.getInt16(i * 2, true);
      samples[i] = sample / 32768;
    }
    return samples;
  }
  console.warn("Unsupported bitsPerSample:", bitsPerSample);
  return new Float32Array(0);
}

export function splitInfoPrefix(arrayBuffer) {
  const dataView = new DataView(arrayBuffer);

  function readChunkId(offset) {
    return String.fromCharCode(
      dataView.getUint8(offset),
      dataView.getUint8(offset + 1),
      dataView.getUint8(offset + 2),
      dataView.getUint8(offset + 3)
    );
  }

  function readChunkSize(offset) {
    return dataView.getUint32(offset, true);
  }

  const prefixName = readChunkId(0);
  if (prefixName !== 'JSON') return [null, null];

  const prefixSize = readChunkSize(4);
  const prefixChunk = arrayBuffer.slice(8, 8 + prefixSize);
  const prefixDecoded = new TextDecoder().decode(new Uint8Array(prefixChunk));
  try {
    const prefixJson = JSON.parse(prefixDecoded);
    // Expected properties: part_id, take_id, and possibly chunk_id
    return [prefixJson, arrayBuffer.slice(8 + prefixSize)];
  } catch (error) {
    console.log('Error decoding JSON in part prefix:', error);
    return [null, arrayBuffer.slice(8 + prefixSize)];
  }
}

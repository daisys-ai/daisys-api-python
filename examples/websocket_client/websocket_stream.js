import { WebsocketConnector } from './websocket_connector.js';
import { splitInfoPrefix } from './audio_utils.js';

export class WebsocketStream {
  constructor(ws_url, other_handlers) {
    this.handlers = new Map();
    this.connector = new WebsocketConnector(ws_url, {
      ontextmessage: this.routeTextMessage.bind(this),
      onbinarymessage: this.routeBinaryMessage.bind(this),
      ...other_handlers
    });
  }

  routeTextMessage(raw) {
    let msg;
    try {
      msg = JSON.parse(raw);
    } catch (e) {
      console.warn("Failed to parse message:", raw);
      return;
    }

    const requestId = msg.request_id;
    if (!requestId || !this.handlers.has(requestId)) return;

    const controller = this.handlers.get(requestId);
    controller.push([msg, null, null]);

    if (["ready", "error", "timeout"].includes(msg.data.status))
      controller.text_done();
  }

  routeBinaryMessage(raw) {
    let [prefix, audio] = splitInfoPrefix(raw);

    const requestId = prefix.request_id;
    if (!requestId || !this.handlers.has(requestId)) return;

    const controller = this.handlers.get(requestId);

    if ([0, null, undefined].includes(prefix.chunk_id) && audio.byteLength === 0) {
      controller.binary_done();
    } else {
      controller.push([null, prefix, audio]);
    }
  }

  async *messageStream(message) {
    if (this.handlers.has(message.request_id)) {
      throw new Error(`Already listening for request_id: ${message.request_id}`);
    }

    let buffer = new Map();
    let resolveNext;
    let text_done = false;
    let bin_done = false;
    let nextPart = 0;
    let nextChunk = 0;

    const key = (part, chunk) => `${part}:${chunk}`;

    const controller = {
      push: ([msg, prefix, audio]) => {
        if (msg) {
          buffer.set('__next__', [msg, null, null]);
        } else if (prefix && audio) {
          const part = prefix.part_id ?? 0;
          const chunk = prefix.chunk_id ?? 0;
          buffer.set(key(part, chunk), [null, prefix, audio]);
        }

        maybeResolve();
      },
      text_done: () => {
        text_done = true;
        maybeResolve();
        if (text_done && bin_done) this.handlers.delete(message.request_id);
      },
      binary_done: () => {
        bin_done = true;
        maybeResolve();
        if (text_done && bin_done) this.handlers.delete(message.request_id);
      },
    };

    const maybeResolve = () => {
      const item = buffer.get(key(nextPart, nextChunk));
      if (item) {
        buffer.delete(key(nextPart, nextChunk));
        const [msg, prefix, audio] = item;
        nextChunk++;

        if (audio && (audio.byteLength === 0 || [null, undefined].includes(prefix.chunk_id))) {
          nextPart++;
          nextChunk = 0;
        }

        if (resolveNext) {
          const r = resolveNext;
          resolveNext = null;
          r(item);
        } else {
          buffer.set("__next__", item); // temp place until pulled by iterator
        }
      } else if (text_done && bin_done && resolveNext) {
        const r = resolveNext;
        resolveNext = null;
        r();
      }
    };

    this.handlers.set(message.request_id, controller);

    this.send(message);

    while (!text_done || !bin_done || buffer.size > 0) {
      if (buffer.has("__next__")) {
        const item = buffer.get("__next__");
        buffer.delete("__next__");
        yield item;
      } else {
        const value = await new Promise((resolve) => {
          resolveNext = resolve;
        });
        if (value) yield value;
      }
    }
  }

  send(data) {
    this.connector.send(JSON.stringify(data));
  }

  close() {
    this.connector.close();
  }
}

// A websocket class that handles fetching the URL to connect to, and
// automatically fetching it again and reconnecting if we get disconnected.

export class WebsocketConnector {
  constructor(ws_url, callbacks = {}) {
    if (!ws_url) throw new Error("Missing ws_url argument");
    this.ws_url = ws_url;
    this.websocket = null;
    this.callbacks = callbacks;
    this.shouldReconnect = true;
    this.reconnectDelay = 1000; // ms
    this.connect();
  }

  async fetchWebSocketUrl() {
    const response = await fetch(this.ws_url);
    if (!response.ok) {
      throw new Error(`Failed to fetch URL: ${response.status}`);
    }

    return await response.text();
  }

  async connect() {
    try {
      // Note that this URL must be fetched whenever we reconnect, after 1 hour
      // it expires and connections will not be accepted.
      const websocketUrl = await this.fetchWebSocketUrl();
      this.websocket = new WebSocket(websocketUrl);

      this.websocket.binaryType = "arraybuffer";

      this.websocket.onopen = () => {
        console.log("WebSocket connection established");
        this.callbacks.onconnectionstatus('connected');
      };

      this.websocket.onerror = (err) => {
        console.error("WebSocket encountered an error:", err);
        this.callbacks.onconnectionstatus('error');
        throw new Error("WebSocket error occurred");
      };

      this.websocket.onclose = () => {
        console.warn("WebSocket disconnected");
        this.callbacks.onconnectionstatus('reconnecting (wait)');
        if (this.shouldReconnect) {
          setTimeout(() => {
            this.callbacks.onconnectionstatus('reconnecting..');
            this.connect();
          }, this.reconnectDelay);
        }
      };

      this.websocket.onmessage = (event) => {
        if (typeof event.data === "string" && this.callbacks.ontextmessage) {
          this.callbacks.ontextmessage(event.data);
        } else if (event.data instanceof ArrayBuffer && this.callbacks.onbinarymessage) {
          this.callbacks.onbinarymessage(event.data);
        }
      };
    } catch (err) {
      console.error("Failed to connect WebSocket:", err);
      this.callbacks.onconnectionstatus(err.message);
      throw err;
    }
  }

  close() {
    this.shouldReconnect = false;
    if (this.websocket) {
      this.callbacks.onconnectionstatus('closing');
      this.websocket.close();
    }
  }

  send(data) {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      this.websocket.send(data);
    } else {
      throw new Error("WebSocket is not open.");
    }
  }
}

let socket = new WebSocket("ws://127.0.0.1:6677/");

socket.onopen = function(e) {
  console.log("[open] Connection established");
  console.log("[send] Sending to server");
  socket.send("Web connection established")
};

socket.onmessage = function(event) {
  console.log(`[message] Data received from server: ${event.data}`);
};

socket.onclose = function(event) {
  if (event.wasClean) {
    console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    console.log('[close] Connection died!')
  }
};

socket.onerror = function(error) {
  console.log(`[error] ${error.message}`);
};

function sendHello() {
  console.log("[send] Sending to server");
  socket.send("Hello!");
};
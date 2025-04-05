const { ipcRenderer } = require('electron');

// Function to send a message to the main process
function sendMessageToMainProcess(message) {
  ipcRenderer.send('message-from-renderer', message);
}

// Function to receive a message from the main process
ipcRenderer.on('message-from-main', (event, message) => {
  console.log('Message from main process:', message);
});

// Example usage: send a message to the main process when a button is clicked
document.getElementById('sendMessageButton').addEventListener('click', () => {
  sendMessageToMainProcess('Hello from renderer process!');
});

// Handle UI interactions for device and visualizer panels
document.getElementById('device-panel').addEventListener('input', (event) => {
  const control = event.target;
  if (control.tagName === 'INPUT' || control.tagName === 'BUTTON') {
    const action = {
      type: control.tagName,
      id: control.id,
      value: control.value
    };
    sendMessageToMainProcess(action);
  }
});

document.getElementById('visualizer-panel').addEventListener('input', (event) => {
  const control = event.target;
  if (control.tagName === 'INPUT' || control.tagName === 'BUTTON') {
    const action = {
      type: control.tagName,
      id: control.id,
      value: control.value
    };
    sendMessageToMainProcess(action);
  }
});

const {ipcRenderer} = require('electron');

ipcRenderer.on('image', (event, arg) => {
    document.getElementById('viewport').setAttribute('src', 'data:image/png;base64,' + arg);
});

ipcRenderer.on('viewport-state', (event, arg) => {
    document.getElementById('viewport').style.visibility = arg;
});

document.getElementById("button").onclick = () => {
    ipcRenderer.send('message', 'toggle-state');
};
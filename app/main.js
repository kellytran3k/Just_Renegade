const electron = require("electron");
const { app, BrowserWindow } = require("electron");

const { PythonShell } = require('python-shell');
const py_main = app.getAppPath() + "/app/py/main.py"

function createWindow() {
  // Use python shell
  var pyshell = new PythonShell(py_main);

  pyshell.on('message', function (message) {
      // received a message sent from the Python script (a simple "print" statement)
      console.log("[py] " + message);
  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err) {
      if (err) {
          throw err;
      }

      console.log('main python script finished');
  });

  // Create the browser window.
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });

  // and load the index.html of the app.
  win.loadFile("app/index.html");

  //open dev tools
  win.webContents.openDevTools();

}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(createWindow);


// Quit when all windows are closed.
app.on("window-all-closed", () => {
  mainWindow = new BrowserWindow({ width: 800, height: 600 });
  mainWindow.WebContents.openDevTools();
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

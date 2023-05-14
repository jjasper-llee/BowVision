const webcam = document.getElementById("webcam");
const canvas = document.getElementById("canvas");
const startStopBtn = document.getElementById("startStopBtn");
const darkModeToggle = document.querySelector("#darkModeToggle");

const ctx = canvas.getContext("2d");
let webcamStream = null;
let isRunning = false;

startStopBtn.addEventListener("click", () => {
  if (isRunning) {
    stopWebcam();
  } else {
    startWebcam();
  }
});

if (darkModeToggle) {
  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
  });
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

async function startWebcam() {
  try {
    webcamStream = await navigator.mediaDevices.getUserMedia({ video: true });
    webcam.srcObject = webcamStream;
    isRunning = true;
    startStopBtn.textContent = "Stop Webcam";
    detectObjects();
  } catch (err) {
    console.error(err);
  }
}

function stopWebcam() {
  if (webcamStream) {
    webcamStream.getTracks().forEach((track) => track.stop());
    webcamStream = null;
  }
  isRunning = false;
  startStopBtn.textContent = "Start Webcam";
  clearCanvas()
}

function detectObjects() {
  if (!isRunning) return;

  ctx.drawImage(webcam, 0, 0, canvas.width, canvas.height);
  const frame = canvas.toDataURL("image/jpeg");

  $.post("/detect", { frame }, (data) => {
    const annotatedFrame = new Image();
    annotatedFrame.src = data.frame;
    annotatedFrame.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(annotatedFrame, 0, 0, canvas.width, canvas.height);
      setTimeout(detectObjects, 5); // Adjust the delay here
    };
  });
}
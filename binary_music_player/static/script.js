const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const audio = document.getElementById('audio');
const bitDisplay = document.getElementById('bit-display');

function updateBitsDisplay(bits) {
  bitDisplay.innerHTML = '';
  for (let i = 0; i < bits.length; i++) {
    const div = document.createElement('div');
    div.classList.add('bit');
    div.classList.add(bits[i] === '1' ? 'on' : 'off');
    bitDisplay.appendChild(div);
  }
}

function fetchAndPlayAudio() {
  fetch('/generate')
    .then(res => res.json())
    .then(data => {
      const url = `/audio?ts=${data.timestamp}`; // bust cache
      audio.src = url;
      audio.play();

      // Simulate bit updates every pattern
      let count = 0;
      const interval = setInterval(() => {
        if (audio.paused || audio.ended) {
          clearInterval(interval);
          return;
        }
        const bits = count.toString(2).padStart(10, '0');
        updateBitsDisplay(bits);
        count = (count + 1) % 1024;
      }, 375);
    });
}

startBtn.onclick = fetchAndPlayAudio;
stopBtn.onclick = () => audio.pause();

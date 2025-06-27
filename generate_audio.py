import numpy as np
import soundfile as sf
import random
import os

# === AUDIO CONFIG ===
SAMPLE_RATE = 44100
PATTERN_DURATION = 0.375  # seconds
note_frequencies = [
    261.63, 293.66, 329.63, 349.23, 392.00,
    440.00, 493.88, 523.25, 587.33, 659.25
]

# === PATTERNS ===
fixed_patterns = ['1010001001', '0101010101']
def gen_random(n=8, length=10, density=0.4):
    return [''.join('1' if random.random()<density else '0' for _ in range(length)) for _ in range(n)]
musical_patterns = fixed_patterns + gen_random()

# === PRECOMPUTE NOTES ===
def make_note(freq):
    t = np.linspace(0, PATTERN_DURATION, int(SAMPLE_RATE * PATTERN_DURATION), False)
    wave = np.sin(2 * np.pi * freq * t) * 0.5
    attack, decay = int(0.05 * SAMPLE_RATE), int(0.1 * SAMPLE_RATE)
    env = np.ones_like(wave)
    env[:attack], env[-decay:] = np.linspace(0, 1, attack), np.linspace(1, 0, decay)
    return wave * env

note_waves = [make_note(f) for f in note_frequencies]

# === BACKEND AUDIO GENERATOR ===
def generate_full_song(num_steps=1024):
    song = []
    patterns = []
    for i in range(num_steps):
        pattern = random.choice(musical_patterns)
        patterns.append(pattern)
        wave = np.zeros_like(note_waves[0])
        for idx, bit in enumerate(pattern):
            if bit == '1':
                wave += note_waves[idx]
        wave /= max(1, pattern.count('1'))
        song.append(wave)

    full_song = np.concatenate(song)
    os.makedirs("generated", exist_ok=True)
    path = "generated/audio.wav"
    sf.write(path, full_song, SAMPLE_RATE)
    return path, patterns

# Run this script directly to test
if __name__ == "__main__":
    path, patterns = generate_full_song()
    print("✅ Audio generated:", path)
    print("🎵 First few patterns:")
    for p in patterns[:5]:
        print(p)

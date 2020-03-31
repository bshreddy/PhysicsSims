import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import matplotlib.pyplot as plt

notes_frq = {"C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13, "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392, "G#": 415.3, "A": 440, "A#": 466.16, "B": 493.88, " ": 0}

notes = [
"G", "B", "B", "G", "G", "E",
"B", " ", "A", "B", "C", "B", "A",
"G", "B", "B", "G", "G", "E",
"B", " ", "A", "B", "C", "B", "A",
"G", "B", "B", "G", "G", "E",
"B", " ", "A", "B", "C", "B", "A", "G", "B", "G",
"B", " ", " ", "A", "A", "B", " ", "A", "G", " ", "B", "F#",
"G", "F#", "G", "F#", "G", "E",
" ", " ", " ", " ", " ",
"B", "E", "E", "E", "B", " ", "B", " ", "B", " ", "C", "B", "A", "B",
" ", "B", " ", "A", " ", "B", "A", "G", "E",
"B", " ", "E", " ", "E", "E",  "B", "B", "B", "C", " ", "B", "A", "B",
" ", "B",  "A", "B", " ", "A", "G", " ", "E",
"B", "E",  "E", "E", "E", "F#", "G", "F#", "E", "F#",
" ", "B", " ", "A", "B", " ", "A", "G", "E",
"B", "E", "E", "E", "B", "B", "C", "B", "A", "B",
" ", " ", " ", " ", " ",
"B", "A", "B", "E", "E", "E",
"D", "E", "D", "E", "B", "A", "G", "A", "F#",
"D", "D", "D", "D", "D", "E", "B",
"B", "A", " ", "B", " ", "A",  "G", "B", "F#",
" ", " ", " ", " ", " ",
"B", "A", "B", "E", "E", "E",
"D", "E", "D", "E", "B", "A", "G", "A", "F#",
"D", "D", "D", "D", "D", "E", "B",
"E", "B", "B", "G", "F#",
"E", "E", "E", "E", "E", "E",
" ", " ", " ", " ", " ",
"G", "B", "B", "G", "G", "E",
"B", " ", "A", "B", "C", "B", "A",
"G", "B", "B", "G", "G", "E",
"B", " ", "A", "B", "C", "B", "A",
"G", "B", "B", "G", "G", "E",
"B", " ", "A", "B", "C", "B", "A", "G", "B", "G",
"B", " ", " ", "A", "A", "B", " ", "A", "G", " ", "B", "F#",
"G", "F#", "G", "F#", "G", "E"
]
filename = "Havana.wav"

print(f"Synthesizing {filename}")
freqs = [notes_frq[note] for note in notes]
sps = 44100
total_duration = 80
duration = total_duration / len(freqs)

waveform = np.array([])

for i, freq in enumerate(freqs):
    cduration = (int(duration * freq) / freq) if freq != 0 else duration
    each_sample_no = np.arange(cduration * sps)
    waveform = np.append(waveform, np.sin(2 * np.pi * each_sample_no * freq / sps))
waveform = waveform * 0.4

write(filename, sps, np.int16(waveform * 32767))
print(f"Saved as {filename}")

print(f"Playing {filename}")
sd.play(waveform, sps, blocking=True)
sd.stop()

if input("Do you want to see Waveform Plot?\nYour Computer may freeze... (Y/n): ").lower() == 'y':
    plt.plot(waveform)
    plt.show()
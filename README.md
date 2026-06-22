# 🎵 HarmoniQ AI

HarmoniQ AI is an AI-powered music analysis and transcription system.

It takes an audio file and automatically extracts:

- 🎼 Key Signature
- 🥁 Tempo (BPM) & Beat Locations
- 🎸 Chord Progression
- 🎹 Musical Notes (MIDI Transcription)
- 🎹 Piano Roll Visualization
- 🎸 Guitar Tabs (Experimental)

---

## Demo Pipeline

```
Audio File
     |
     v
Demucs Source Separation
     |
     v
Instrument Stem (other.wav)
     |
     +---- Tempo Detection
     |
     +---- Key Detection
     |
     +---- BTC Chord Recognition
     |
     +---- Basic Pitch Transcription
                  |
                  v
            Note Cleaning
                  |
                  v
          Piano Roll Generation
                  |
                  v
        Guitar Tab Generation (WIP)
```

---

## Current Features

### 🎵 AI Source Separation
Uses Facebook Demucs to separate:

- Vocals
- Drums
- Bass
- Other Instruments

GPU acceleration supported through CUDA.

---

### 🥁 Tempo Detection

Extracts:
- BPM
- Precise tempo
- Beat timestamps

Example:

```
Tempo: 91 BPM
Beats: 274
```

---

### 🎼 Key Detection

Analyzes chromagram and compares all 24 major/minor keys.

Example:

```
Primary Key: D Major
Confidence: 1.0
```

---

### 🎸 Chord Detection

Uses BTC (Bi-directional Transformer for Chord Recognition).

Detects:
- Major / Minor
- 7th Chords
- Suspended Chords
- Extended Chords

Example:

```
D
G
A
Bm
Em7
A7
```

---

### 🎹 Note Transcription

Uses Spotify Basic Pitch for:

- MIDI note extraction
- Pitch detection
- Note timing

Outputs:

```
outputs/notes/other.json
```

---

### 🎹 Piano Roll

Generates high-quality piano roll images with:

- Note timing
- MIDI pitch
- Multiple pages for long songs

---

### 🎸 Guitar Tabs (Experimental)

Current capabilities:

- Guitar fret mapping
- Hand position optimization
- Phrase detection
- Hammer-ons
- Pull-offs
- Slides
- ASCII tab rendering

Future improvements:

- Better melody extraction
- Rhythm-aware tabs
- Standard notation export

---

# Project Structure

```
HarmoniQ AI/
│
├── src/
│   ├── analysis/
│   │   ├── tempo.py
│   │   ├── key.py
│   │   ├── chords.py
│   │   ├── transcription.py
│   │   └── note_cleaner.py
│   │
│   ├── audio/
│   │   └── separator.py
│   │
│   ├── guitar/
│   │   └── lead_guitar.py
│   │
│   └── visualization/
│       ├── piano_roll.py
│       └── lead_tab_renderer.py
│
├── externals/
│   └── BTC/
│
├── sample audio/
│
├── outputs/
│
├── main.py
│
└── requirements.txt
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/pushp-365/audio_to-_pianoRoll

```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / MacOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Download BTC Model Weights

Place the BTC model files inside:

```
externals/BTC/weights/
```

Required:

```
btc_model.pt
btc_model_large_voca.pt
```

---

# Usage

Put your audio file inside:

```
sample audio/
```

Edit:

```python
INPUT_AUDIO = "sample audio/song.mp3"
```

Run:

```bash
python main.py
```

---

# Output

```
outputs/
│
├── separated/
│
├── analysis/
│   ├── tempo.json
│   ├── key.json
│   └── chords.json
│
├── notes/
│   ├── other.json
│   └── clean_notes.json
│
├── piano/
│
└── tabs/
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Source Separation | Demucs |
| Chord Detection | BTC Transformer |
| Note Transcription | Spotify Basic Pitch |
| Tempo Analysis | Librosa |
| Key Detection | Chroma Analysis |
| MIDI Processing | Pretty MIDI |
| Visualization | Matplotlib |
| ML Framework | PyTorch |

---

# Roadmap

- [x] Source Separation
- [x] Tempo Detection
- [x] Key Detection
- [x] Chord Detection
- [x] Piano Roll
- [x] Basic Guitar Tab Engine
- [ ] Better Lead Extraction
- [ ] Rhythm-Aware Guitar Tabs
- [ ] Web GUI
- [ ] Real-Time Analysis

---

## Author

## Author

HarmoniQ  AI was created and developed by **Pushp Sharma**.

If you use this project in your research, academic work, or another project,
please consider giving proper credit by mentioning the original repository.

GitHub: https://github.com/pushp-365
---

⭐ If you like this project, consider giving it a star.
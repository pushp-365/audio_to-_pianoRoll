import os

# ===============================
# IMPORT MODULES
# ===============================

from src.audio.separator import separate_audio

from src.analysis.tempo import analyze_tempo

from src.analysis.key import analyze_key

from src.analysis.chords import analyze_chords

# CHANGE THIS IMPORT TO YOUR ACTUAL FILE
# Example:
# from src.analysis.note_extractor import extract_notes
# from src.analysis.basic_pitch import extract_notes
from src.analysis.transcription import transcribe_notes

from src.analysis.note_cleaner import clean_notes

from src.visualization.piano_roll import create_piano_roll


# ===============================
# CONFIG
# ===============================

INPUT_AUDIO = "sample audio/sample1.mp3"

OUTPUT_AUDIO = "outputs/input.wav"

RAW_NOTES = "outputs/notes/raw_notes.json"

CLEAN_NOTES = "outputs/notes/clean_notes.json"


# ===============================
# MAIN PIPELINE
# ===============================

def main():

    print("\n" + "=" * 60)
    print("🎵 MUSICMIND AI")
    print("=" * 60)


    # ===============================
    # 1. Separation
    # ===============================

    print("\n[1/7] Separating audio...")

    separate_audio(INPUT_AUDIO)

    print("✓ Separation complete")


    # ===============================
    # 2. Tempo
    # ===============================

    print("\n[2/7] Detecting tempo...")

    tempo_data = analyze_tempo(OUTPUT_AUDIO)

    print(
        f"✓ Tempo: {tempo_data['tempo_bpm']} BPM"
    )


    # ===============================
    # 3. Key
    # ===============================

    print("\n[3/7] Detecting key...")

    key_data = analyze_key(OUTPUT_AUDIO)

    print(
        f"✓ Key: {key_data['primary_key']['key']}"
    )


    # ===============================
    # 4. Chords
    # ===============================

    print("\n[4/7] Detecting chords...")

    analyze_chords(OUTPUT_AUDIO)

    print(
        "✓ Chords analyzed"
    )


    # ===============================
    # 5. Basic Pitch Note Extraction
    # ===============================

    print("\n[5/7] Extracting notes...")

    transcribe_notes(
        OUTPUT_AUDIO
    )

    print(
        "✓ Raw notes extracted"
    )


    # ===============================
    # 6. Note Cleaning
    # ===============================

    print("\n[6/7] Cleaning notes...")

    clean_notes(
        "outputs/notes/other.json"

    )

    print(
        "✓ Notes cleaned"
    )


    # ===============================
    # 7. Piano Roll
    # ===============================

    print("\n[7/7] Generating piano roll...")

    create_piano_roll(
        notes_file=CLEAN_NOTES,
        tempo=tempo_data["tempo_bpm"]
    )

    print(
        "✓ Piano roll generated"
    )


    # ===============================
    # FINISH
    # ===============================

    print("\n" + "=" * 60)
    print("🎉 MUSICMIND ANALYSIS COMPLETE")
    print("=" * 60)

    print("""
Generated files:

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
│   ├── raw_notes.json
│   └── clean_notes.json
│
└── piano/
    ├── page_1.png
    ├── page_2.png
    └── ...
""")


# ===============================
# START
# ===============================

if __name__ == "__main__":
    main()
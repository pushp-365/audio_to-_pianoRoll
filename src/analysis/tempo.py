import os
import json
import librosa
import numpy as np


def analyze_tempo(audio_path, output_file="outputs/analysis/tempo.json"):
    """
    Detect tempo (BPM) and beat timestamps.
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        dict: Tempo analysis results
    """

    print("\n" + "=" * 50)
    print("🎵 TEMPO ANALYSIS ENGINE")
    print("=" * 50)
    print(f"Loading: {audio_path}")

    # Load audio
    y, sr = librosa.load(
        audio_path,
        sr=None,
        mono=True
    )

    print("Detecting tempo and beats...")

    # Beat tracking
    tempo, beat_frames = librosa.beat.beat_track(
        y=y,
        sr=sr
    )
    if hasattr(tempo, "__len__"):
        tempo = float(tempo[0])
    else:
        tempo = float(tempo)

    # Convert frames to seconds
    beat_times = librosa.frames_to_time(
        beat_frames,
        sr=sr
    )

    result = {
        "file": os.path.basename(audio_path),
        "tempo_bpm": int(round(tempo)),
        "tempo_precise": round(tempo, 3),
        "total_beats": int(len(beat_times)),
        "beat_times": [
            round(float(time), 3)
            for time in beat_times
        ]
    }

    # Create output folder
    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    # Save JSON
    with open(
        output_file,
        "w"
    ) as f:
        json.dump(
            result,
            f,
            indent=4
        )

    print("Analysis complete!")
    print(f"BPM: {result['tempo_bpm']}")
    print(f"Beats found: {result['total_beats']}")
    print(f"Saved: {output_file}")

    return result
import os
import json
import numpy as np
import librosa


# Krumhansl-Schmuckler key profiles
MAJOR_PROFILE = np.array([
    6.35, 2.23, 3.48, 2.33,
    4.38, 4.09, 2.52, 5.19,
    2.39, 3.66, 2.29, 2.88
])

MINOR_PROFILE = np.array([
    6.33, 2.68, 3.52, 5.38,
    2.60, 3.53, 2.54, 4.75,
    3.98, 2.69, 3.34, 3.17
])


NOTES = [
    "C", "C#", "D", "D#",
    "E", "F", "F#", "G",
    "G#", "A", "A#", "B"
]


def analyze_key(
        audio_path,
        output_file="outputs/analysis/key.json"
):
    """
    Detect the musical key of an audio file.
    """

    print("\n" + "=" * 60)
    print("🎼 KEY DETECTION ENGINE")
    print("=" * 60)
    print(f"Loading: {audio_path}")


    # Load audio
    try:
        y, sr = librosa.load(
            audio_path,
            sr=None,
            mono=True
        )

    except Exception as error:
        print("❌ Failed to load audio")
        print(error)
        return None


    print("Generating chromagram...")

    # Compute chromagram
    chroma = librosa.feature.chroma_cqt(
        y=y,
        sr=sr
    )

    # Average energy of each note
    chroma_vector = np.mean(
        chroma,
        axis=1
    )

    # Normalize
    chroma_vector = (
        chroma_vector /
        np.sum(chroma_vector)
    )


    print("Comparing 24 possible keys...")

    scores = []


    # Check major keys
    for i in range(12):

        profile = np.roll(
            MAJOR_PROFILE,
            i
        )

        score = np.corrcoef(
            chroma_vector,
            profile
        )[0, 1]


        scores.append({
            "key": f"{NOTES[i]} Major",
            "score": float(score)
        })


    # Check minor keys
    for i in range(12):

        profile = np.roll(
            MINOR_PROFILE,
            i
        )

        score = np.corrcoef(
            chroma_vector,
            profile
        )[0, 1]


        scores.append({
            "key": f"{NOTES[i]} Minor",
            "score": float(score)
        })


    # Sort by score
    scores.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # Convert scores into confidence values
    best_score = scores[0]["score"]

    results = []

    for item in scores[:3]:

        confidence = (
            item["score"] / best_score
        )

        results.append({
            "key": item["key"],
            "confidence": round(
                float(confidence),
                3
            )
        })


    output = {
        "file": os.path.basename(audio_path),

        "primary_key": results[0],

        "alternatives": results[1:]
    }


    # Create folder
    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )


    # Save JSON
    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            indent=4
        )


    print("\n" + "=" * 60)
    print("✅ Key analysis complete")
    print("=" * 60)

    print(
        f"Primary key: "
        f"{results[0]['key']}"
    )

    print(
        f"Confidence: "
        f"{results[0]['confidence']}"
    )

    print(
        f"Saved: {output_file}"
    )


    return output
import os
import json
import shutil
import subprocess
import sys


# ===============================
# BTC Configuration
# ===============================

BTC_DIR = "externals/btc"

BTC_INPUT = os.path.join(
    BTC_DIR,
    "musicmind_input"
)

BTC_OUTPUT = os.path.join(
    BTC_DIR,
    "musicmind_output"
)


# ===============================
# Main Function
# ===============================

def analyze_chords(
    audio_path,
    output_file="outputs/analysis/chords.json",
    large_vocabulary=True
):

    print("\n" + "=" * 50)
    print("🎸 BTC CHORD DETECTION ENGINE")
    print("=" * 50)

    # Create folders
    os.makedirs(BTC_INPUT, exist_ok=True)
    os.makedirs(BTC_OUTPUT, exist_ok=True)


    # Clean old files
    for folder in [BTC_INPUT, BTC_OUTPUT]:
        for file in os.listdir(folder):
            os.remove(
                os.path.join(folder, file)
            )


    # -----------------------------
    # Copy audio to BTC
    # -----------------------------

    filename = os.path.basename(audio_path)

    btc_audio = os.path.join(
        BTC_INPUT,
        filename
    )

    shutil.copy(
        audio_path,
        btc_audio
    )

    print(f"Input audio: {filename}")


    # -----------------------------
    # Run BTC
    # -----------------------------

    command = [
        sys.executable,
        "test.py",
        "--audio_dir",
        "musicmind_input",
        "--save_dir",
        "musicmind_output",
        "--voca",
        str(large_vocabulary)
    ]

    print("Running BTC model...")


    subprocess.run(
        command,
        cwd=BTC_DIR,
        check=True
    )


    print("BTC finished")


    # -----------------------------
    # Find LAB file
    # -----------------------------

    name = os.path.splitext(
        filename
    )[0]


    lab_path = os.path.join(
        BTC_OUTPUT,
        name + ".lab"
    )


    if not os.path.exists(lab_path):
        raise FileNotFoundError(
            f"BTC output not found: {lab_path}"
        )


    print(f"LAB file found: {lab_path}")


    # -----------------------------
    # Parse LAB
    # -----------------------------

    chords = []


    with open(
        lab_path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()


            if not line:
                continue


            parts = line.split()


            if len(parts) != 3:
                continue


            start, end, chord = parts


            chords.append(
                {
                    "start": round(
                        float(start),
                        3
                    ),

                    "end": round(
                        float(end),
                        3
                    ),

                    "chord": chord
                }
            )


    result = {
        "file": filename,
        "total_chords": len(chords),
        "chords": chords
    }


    # -----------------------------
    # Save JSON
    # -----------------------------

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )


    print("\n" + "=" * 50)
    print("✅ Chord analysis complete")
    print("=" * 50)

    print(
        f"Total chords: {len(chords)}"
    )

    print(
        f"Saved: {output_file}"
    )


    return result
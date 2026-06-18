import json
import os


# ==============================
# Guitar chord dictionary
# Standard tuning E A D G B E
# ==============================

CHORD_SHAPES = {

    # Major
    "C":  ["x", 3, 2, 0, 1, 0],
    "D":  ["x", "x", 0, 2, 3, 2],
    "E":  [0, 2, 2, 1, 0, 0],
    "F":  [1, 3, 3, 2, 1, 1],
    "G":  [3, 2, 0, 0, 0, 3],
    "A":  ["x", 0, 2, 2, 2, 0],
    "B":  ["x", 2, 4, 4, 4, 2],

    # Minor
    "C:min": ["x", 3, 5, 5, 4, 3],
    "D:min": ["x", "x", 0, 2, 3, 1],
    "E:min": [0, 2, 2, 0, 0, 0],
    "F:min": [1, 3, 3, 1, 1, 1],
    "G:min": [3, 5, 5, 3, 3, 3],
    "A:min": ["x", 0, 2, 2, 1, 0],
    "B:min": ["x", 2, 4, 4, 3, 2],

    # 7 chords
    "A:7": [0, 0, 2, 0, 2, 0],
    "D:7": ["x", "x", 0, 2, 1, 2],
    "E:7": [0, 2, 0, 1, 0, 0],

    # Sus chords
    "G:sus2": [3, 0, 0, 0, 3, 3],
    "D:sus4": ["x", "x", 0, 2, 3, 3],
    "A:sus4": ["x", 0, 2, 2, 3, 0],

    # Major 7
    "G:maj7": [3, 2, 0, 0, 0, 2],

    # Minor 7
    "E:min7": [0, 2, 2, 0, 3, 0],
    "B:min7": ["x", 2, 4, 2, 3, 2],

    # No chord
    "N": ["-", "-", "-", "-", "-", "-"]
}


# ==============================
# Generate text tab
# ==============================

def generate_rhythm_tabs(
        chord_file,
        output_file="outputs/tabs/rhythm_tabs.txt"
):

    print("\n" + "="*50)
    print("🎸 RHYTHM GUITAR GENERATOR")
    print("="*50)


    with open(chord_file, "r", encoding="utf-8") as f:
        data = json.load(f)


    chords = data["chords"]


    lines = {
        "e": "e|",
        "B": "B|",
        "G": "G|",
        "D": "D|",
        "A": "A|",
        "E": "E|"
    }


    string_names = ["E", "A", "D", "G", "B", "e"]


    for item in chords:

        chord = item["chord"]

        shape = CHORD_SHAPES.get(chord)


        if shape is None:
            print(f"Unknown chord skipped: {chord}")
            continue


        # Convert each fret to text
        for i, string in enumerate(string_names):

            fret = str(shape[i])

            lines[string] += fret + "---"


    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )


    with open(output_file, "w") as f:

        f.write(
            lines["e"] + "\n" +
            lines["B"] + "\n" +
            lines["G"] + "\n" +
            lines["D"] + "\n" +
            lines["A"] + "\n" +
            lines["E"]
        )


    print("✅ Tabs generated")
    print(f"Saved: {output_file}")


    return lines
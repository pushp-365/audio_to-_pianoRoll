import os
import json


MIN_NOTE_DURATION = 0.08      # seconds
PITCH_PADDING = 4             # notes above and below
OUTLIER_PERCENT = 0.02        # remove top/bottom 2%
MERGE_GAP = 0.05              # merge notes within 50ms


def merge_notes(notes):
    """
    Merge consecutive notes of same pitch.
    """

    if not notes:
        return []

    notes.sort(
        key=lambda x: (
            x["pitch"],
            x["start"]
        )
    )

    merged = [
        notes[0]
    ]


    for note in notes[1:]:

        previous = merged[-1]


        same_pitch = (
            note["pitch"] ==
            previous["pitch"]
        )


        small_gap = (
            note["start"] -
            previous["end"]
            <= MERGE_GAP
        )


        if same_pitch and small_gap:

            previous["end"] = max(
                previous["end"],
                note["end"]
            )

            previous["velocity"] = max(
                previous["velocity"],
                note["velocity"]
            )

        else:
            merged.append(note)


    return merged


def clean_notes(
    input_file,
    output_file="outputs/notes/clean_notes.json"
):

    print("\n" + "=" * 50)
    print("🎹 NOTE CLEANING ENGINE")
    print("=" * 50)


    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    notes = data["notes"]


    print(
        f"Original notes: {len(notes)}"
    )


    # --------------------------------
    # Remove tiny notes
    # --------------------------------

    notes = [
        n for n in notes
        if (
            n["end"] - n["start"]
        ) >= MIN_NOTE_DURATION
    ]


    print(
        f"After duration filter: {len(notes)}"
    )


    # --------------------------------
    # Remove pitch outliers
    # --------------------------------

    pitches = sorted(
        n["pitch"]
        for n in notes
    )


    low = pitches[
        int(
            len(pitches)
            * OUTLIER_PERCENT
        )
    ]


    high = pitches[
        int(
            len(pitches)
            * (1 - OUTLIER_PERCENT)
        )
    ]


    notes = [
        n for n in notes
        if low - PITCH_PADDING
        <= n["pitch"]
        <= high + PITCH_PADDING
    ]


    print(
        f"After pitch cleanup: {len(notes)}"
    )


    # --------------------------------
    # Merge broken notes
    # --------------------------------

    notes = merge_notes(notes)


    print(
        f"After merging: {len(notes)}"
    )


    # Sort by time again

    notes.sort(
        key=lambda x: x["start"]
    )


    result = {

        "total_notes": len(notes),

        "notes": notes
    }


    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4
        )


    print("\n✅ Cleaning complete")

    print(
        f"Saved: {output_file}"
    )


    return result
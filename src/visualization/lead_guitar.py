import os
import json


# ==================================
# Guitar configuration
# ==================================

STRINGS = {
    1: 64,  # High E
    2: 59,  # B
    3: 55,  # G
    4: 50,  # D
    5: 45,  # A
    6: 40   # Low E
}


MAX_FRET = 20

MIN_GUITAR_MIDI = 40
MAX_GUITAR_MIDI = 80

PHRASE_GAP = 0.2


# ==================================
# Fretboard mapping
# ==================================

def get_positions(midi_note):

    positions = []

    for string, open_note in STRINGS.items():

        fret = midi_note - open_note

        if 0 <= fret <= MAX_FRET:

            positions.append({
                "string": string,
                "fret": fret
            })

    return positions


# ==================================
# Phrase detection
# ==================================

def split_phrases(notes):

    if not notes:
        return []

    phrases = []
    current = [notes[0]]

    for note in notes[1:]:

        gap = (
            note["start"]
            -
            current[-1]["end"]
        )

        if gap > PHRASE_GAP:

            phrases.append(current)

            current = [note]

        else:

            current.append(note)

    phrases.append(current)

    return phrases


# ==================================
# Find phrase hand position
# ==================================

def get_phrase_position(phrase):

    frets = []

    for note in phrase:

        for pos in get_positions(
            note["pitch"]
        ):

            frets.append(
                pos["fret"]
            )

    if not frets:
        return 5

    frets.sort()

    return frets[len(frets)//2]


# ==================================
# Position cost
# ==================================

def position_cost(
    current,
    previous_position,
    previous_note,
    current_note,
    time_gap,
    target_position
):

    # First note of phrase
    if previous_position is None:

        return abs(
            current["fret"]
            - target_position
        )


    fret_jump = abs(
        current["fret"]
        -
        previous_position["fret"]
    )


    string_jump = abs(
        current["string"]
        -
        previous_position["string"]
    )


    # Keep hand in the same area
    position_penalty = abs(
        current["fret"]
        -
        target_position
    )


    # Avoid very high frets
    high_fret_penalty = 0

    if current["fret"] > 12:

        high_fret_penalty = (
            current["fret"] - 12
        ) * 2


    # Time-aware movement
    speed_penalty = (
        fret_jump /
        max(time_gap, 0.05)
    )


    # Important:
    # Same note should stay on the same string
    same_note_bonus = 0


    if (
        previous_note is not None
        and previous_note["pitch"]
        == current_note["pitch"]
    ):

        if (
            current["string"]
            ==
            previous_position["string"]
        ):

            same_note_bonus = -30


    cost = (
        fret_jump * 3
        +
        string_jump * 5
        +
        position_penalty * 4
        +
        high_fret_penalty
        +
        speed_penalty
        +
        same_note_bonus
    )


    return cost


# ==================================
# Choose best fret position
# ==================================

def choose_position(
    positions,
    previous_position,
    previous_note,
    current_note,
    time_gap,
    target_position
):

    if not positions:
        return None


    return min(
        positions,
        key=lambda pos:
        position_cost(
            pos,
            previous_position,
            previous_note,
            current_note,
            time_gap,
            target_position
        )
    )

# ==================================
# Choose best fingering
# ==================================

def choose_position(
    positions,
    previous_position,
    previous_note,
    current_note,
    time_gap,
    target_position
):

    if not positions:
        return None


    return min(
        positions,
        key=lambda pos:
        position_cost(
            pos,
            previous_position,
            previous_note,
            current_note,
            time_gap,
            target_position
        )
    )

# ==================================
# Main Lead Guitar Generator
# ==================================

def generate_lead_tabs(
    notes_file,
    output_file="outputs/tabs/lead_tabs.json"
):

    print("\n" + "=" * 50)
    print("🎸 LEAD GUITAR V3.1 ENGINE")
    print("=" * 50)


    # ------------------------------
    # Load notes
    # ------------------------------

    with open(
        notes_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    notes = data["notes"]


    print(
        f"Original notes: {len(notes)}"
    )


    # ------------------------------
    # Guitar range filtering
    # ------------------------------

    notes = [
        n for n in notes
        if MIN_GUITAR_MIDI
        <= n["pitch"]
        <= MAX_GUITAR_MIDI
    ]


    print(
        f"After guitar range filter: {len(notes)}"
    )


    # ------------------------------
    # Sort by time
    # ------------------------------

    notes.sort(
        key=lambda x: x["start"]
    )


    # ------------------------------
    # Split phrases
    # ------------------------------

    phrases = split_phrases(
        notes
    )


    print(
        f"Phrases detected: {len(phrases)}"
    )


    tabs = []


    # ==============================
    # Process every phrase
    # ==============================

    for index, phrase in enumerate(
        phrases
    ):

        print(
            "\n--------------------------------"
        )

        print(
            f"Phrase {index + 1}"
        )

        print(
            f"Notes: {len(phrase)}"
        )


        # Find best fret region
        target_position = (
            get_phrase_position(
                phrase
            )
        )


        print(
            f"Hand position: {target_position}"
        )


        previous_position = None
        previous_note = None
        previous_time = None


        # ==========================
        # Process each note
        # ==========================

        for note in phrase:


            # Find all possible places
            positions = get_positions(
                note["pitch"]
            )


            if not positions:
                continue


            # Time available for movement
            if previous_time is None:

                time_gap = 1.0

            else:

                time_gap = (
                    note["start"]
                    -
                    previous_time
                )


            # Choose best fret
            position = choose_position(
                positions,
                previous_position,
                previous_note,
                note,
                time_gap,
                target_position
            )


            if position is None:
                continue


            # Save tab information
            tabs.append({

                "note":
                note["note"],

                "pitch":
                note["pitch"],

                "start":
                round(
                    note["start"],
                    3
                ),

                "end":
                round(
                    note["end"],
                    3
                ),

                "duration":
                round(
                    note["end"]
                    -
                    note["start"],
                    3
                ),

                "string":
                position["string"],

                "fret":
                position["fret"],

                "phrase":
                index + 1
            })


            # Update memory
            previous_position = position

            previous_note = note

            previous_time = (
                note["start"]
            )


    print("\n" + "=" * 50)
    print(
        f"Lead notes converted: {len(tabs)}"
    )


    # We will add techniques
    # and saving in Part 3


    # Detect techniques
    tabs = detect_techniques(tabs)


    # Save final JSON
    return save_lead_tabs(
        tabs,
        output_file
    )
# ==================================
# Guitar technique detection
# ==================================

def detect_techniques(tabs):

    if not tabs:
        return tabs


    for i in range(len(tabs) - 1):

        current = tabs[i]
        nxt = tabs[i + 1]


        # Default
        current["technique"] = ""


        # Only compare notes inside same phrase
        if current["phrase"] != nxt["phrase"]:
            continue


        time_gap = (
            nxt["start"]
            -
            current["end"]
        )


        fret_diff = (
            nxt["fret"]
            -
            current["fret"]
        )


        same_string = (
            current["string"]
            ==
            nxt["string"]
        )


        # --------------------------
        # Hammer-on
        # Example: 5h7
        # --------------------------
        if (
            same_string
            and 1 <= fret_diff <= 3
            and time_gap < 0.12
        ):

            current["technique"] = "h"


        # --------------------------
        # Pull-off
        # Example: 7p5
        # --------------------------
        elif (
            same_string
            and -3 <= fret_diff <= -1
            and time_gap < 0.12
        ):

            current["technique"] = "p"


        # --------------------------
        # Slide
        # Example: 5/10
        # --------------------------
        elif (
            same_string
            and abs(fret_diff) > 3
            and time_gap < 0.15
        ):

            current["technique"] = "/"


        # --------------------------
        # Possible bend
        # --------------------------
        elif (
            same_string
            and abs(fret_diff) <= 2
            and current["duration"] > 0.7
            and time_gap < 0.05
        ):

            current["technique"] = "b"


    # Last note
    tabs[-1]["technique"] = ""


    return tabs


# ==================================
# Save lead tabs
# ==================================

def save_lead_tabs(
    tabs,
    output_file
):

    result = {

        "total_notes": len(tabs),

        "total_phrases": (
            max(
                note["phrase"]
                for note in tabs
            )
            if tabs else 0
        ),

        "tabs": tabs
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


    print("\n" + "="*50)
    print("✅ Lead Guitar V3.1 Complete")
    print("="*50)

    print(
        f"Notes saved: {len(tabs)}"
    )

    print(
        f"Output: {output_file}"
    )


    return result
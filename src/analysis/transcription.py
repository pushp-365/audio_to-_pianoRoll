import os
import json
import pretty_midi

from basic_pitch.inference import predict


def midi_to_notes(midi_path):
    """
    Convert MIDI file into MusicMind note JSON format
    """

    midi = pretty_midi.PrettyMIDI(midi_path)

    notes = []

    for instrument in midi.instruments:

        for note in instrument.notes:

            notes.append({
                "pitch": note.pitch,
                "note": pretty_midi.note_number_to_name(
                    note.pitch
                ),
                "start": round(
                    note.start,
                    3
                ),
                "end": round(
                    note.end,
                    3
                ),
                "velocity": note.velocity
            })

    notes.sort(
        key=lambda x: x["start"]
    )

    return notes


def transcribe_notes(
    audio_path,
    output_dir="outputs/notes"
):
    """
    Audio → MIDI → JSON notes
    """

    print("\n" + "=" * 50)
    print("🎹 BASIC PITCH TRANSCRIPTION ENGINE")
    print("=" * 50)

    print(f"Loading: {audio_path}")

    os.makedirs(
        output_dir,
        exist_ok=True
    )


    # ---------------------------
    # Output paths
    # ---------------------------

    name = os.path.splitext(
        os.path.basename(audio_path)
    )[0]

    midi_file = os.path.join(
        output_dir,
        name + ".mid"
    )

    json_file = os.path.join(
        output_dir,
        name + ".json"
    )


    # ---------------------------
    # Run Basic Pitch
    # ---------------------------

    print("Detecting notes...")

    model_output, midi_data, note_events = predict(
        audio_path
    )


    # Save MIDI
    midi_data.write(
        midi_file
    )

    print(f"MIDI saved: {midi_file}")


    # ---------------------------
    # MIDI → JSON
    # ---------------------------

    notes = midi_to_notes(
        midi_file
    )


    result = {
        "file": os.path.basename(
            audio_path
        ),
        "total_notes": len(notes),
        "notes": notes
    }


    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
            ensure_ascii=False
        )


    print("\n" + "=" * 50)
    print("✅ Transcription complete")
    print("=" * 50)

    print(
        f"Total notes: {len(notes)}"
    )

    print(
        f"JSON saved: {json_file}"
    )

    return result
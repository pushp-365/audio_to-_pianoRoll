import json
import os


STRING_NAMES = [
    "e",
    "B",
    "G",
    "D",
    "A",
    "E"
]


def render_lead_tabs(
    input_file="outputs/tabs/lead_tabs.json",
    output_file="outputs/tabs/lead_ascii.txt",
    notes_per_line=30
):

    print("\n" + "=" * 50)
    print("🎸 LEAD TAB RENDERER")
    print("=" * 50)


    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)


    notes = data["tabs"]


    result = []


    for chunk_start in range(
        0,
        len(notes),
        notes_per_line
    ):

        chunk = notes[
            chunk_start:
            chunk_start + notes_per_line
        ]


        lines = {
            "e": "e|",
            "B": "B|",
            "G": "G|",
            "D": "D|",
            "A": "A|",
            "E": "E|"
        }


        for note in chunk:

            # Which string?
            target = STRING_NAMES[
                note["string"] - 1
            ]


            # Fret + technique
            text = (
                str(note["fret"])
                +
                note.get(
                    "technique",
                    ""
                )
            )


            # Dynamic spacing
            width = max(
                4,
                len(text) + 2
            )


            for string in STRING_NAMES:

                if string == target:

                    lines[string] += (
                        text
                        +
                        "-" *
                        (
                            width - len(text)
                        )
                    )

                else:

                    lines[string] += (
                        "-" *
                        width
                    )


        # close tab block
        for string in STRING_NAMES:

            lines[string] += "|"


        block = (
            lines["e"] + "\n" +
            lines["B"] + "\n" +
            lines["G"] + "\n" +
            lines["D"] + "\n" +
            lines["A"] + "\n" +
            lines["E"]
        )


        result.append(block)


    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n\n".join(result)
        )


    print(
        f"Total notes rendered: {len(notes)}"
    )

    print(
        f"Saved to: {output_file}"
    )


    return result
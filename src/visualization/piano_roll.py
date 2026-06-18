import os
import json
import math

from PIL import (
    Image,
    ImageDraw,
    ImageFont
)


# ==========================
# DISPLAY SETTINGS
# ==========================

WIDTH = 1920
HEIGHT = 1080

KEYBOARD_WIDTH = 120
TOP_BAR_HEIGHT = 60

PAGE_SECONDS = 20


# ==========================
# COLORS
# ==========================

BG = (20, 22, 28)

GRID_LIGHT = (45, 48, 55)
GRID_DARK = (35, 37, 43)

BAR_LINE = (90, 90, 100)
BEAT_LINE = (55, 55, 65)

WHITE_KEY = (220, 220, 220)
BLACK_KEY = (40, 40, 40)

C_KEY = (255, 180, 50)

NOTE_COLOR = (255, 195, 30)
NOTE_BORDER = (255, 230, 120)

TEXT = (230, 230, 230)


# ==========================
# MUSIC HELPERS
# ==========================

NOTE_NAMES = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B"
]


BLACK_NOTES = {
    1, 3, 6, 8, 10
}


def midi_name(number):

    note = NOTE_NAMES[number % 12]

    octave = number // 12 - 1

    return f"{note}{octave}"


def is_black_key(midi):

    return midi % 12 in BLACK_NOTES


def load_font(size):

    try:
        return ImageFont.truetype(
            "arial.ttf",
            size
        )

    except:
        return ImageFont.load_default()


# ==========================
# CANVAS
# ==========================

def create_canvas():

    img = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BG
    )

    draw = ImageDraw.Draw(img)

    return img, draw


# ==========================
# POSITION HELPERS
# ==========================

def time_to_x(
    time,
    page_start
):

    usable_width = (
        WIDTH -
        KEYBOARD_WIDTH
    )

    return (
        KEYBOARD_WIDTH +
        (
            (time - page_start)
            /
            PAGE_SECONDS
        )
        *
        usable_width
    )


def pitch_to_y(
    pitch,
    min_pitch,
    max_pitch
):

    usable_height = (
        HEIGHT -
        TOP_BAR_HEIGHT
    )


    total_notes = (
        max_pitch -
        min_pitch +
        1
    )


    note_height = (
        usable_height /
        total_notes
    )


    return (
        HEIGHT -
        ((pitch - min_pitch + 1)
        * note_height)
    )
# ==========================
# PIANO KEYBOARD
# ==========================

def draw_keyboard(
    draw,
    min_pitch,
    max_pitch
):

    usable_height = (
        HEIGHT -
        TOP_BAR_HEIGHT
    )

    total_notes = (
        max_pitch -
        min_pitch +
        1
    )

    note_height = (
        usable_height /
        total_notes
    )


    font = load_font(18)


    for pitch in range(
        min_pitch,
        max_pitch + 1
    ):

        y = pitch_to_y(
            pitch,
            min_pitch,
            max_pitch
        )

        y2 = y + note_height


        # --------------------
        # White / black keys
        # --------------------

        if is_black_key(pitch):

            color = BLACK_KEY

        else:

            color = WHITE_KEY


        # Highlight C notes
        if pitch % 12 == 0:

            color = C_KEY


        draw.rectangle(
            [
                0,
                y,
                KEYBOARD_WIDTH,
                y2
            ],
            fill=color,
            outline=(0,0,0)
        )


        # --------------------
        # Note labels
        # --------------------

        name = midi_name(
            pitch
        )


        text_color = (
            (0,0,0)
            if not is_black_key(pitch)
            else TEXT
        )


        draw.text(
            (
                15,
                y + 5
            ),
            name,
            font=font,
            fill=text_color
        )


# ==========================
# BACKGROUND LANES
# ==========================

def draw_note_lanes(
    draw,
    min_pitch,
    max_pitch
):

    usable_height = (
        HEIGHT -
        TOP_BAR_HEIGHT
    )


    total_notes = (
        max_pitch -
        min_pitch +
        1
    )


    note_height = (
        usable_height /
        total_notes
    )


    for pitch in range(
        min_pitch,
        max_pitch + 1
    ):

        y = pitch_to_y(
            pitch,
            min_pitch,
            max_pitch
        )

        y2 = y + note_height


        # --------------------
        # Piano roll rows
        # --------------------

        if is_black_key(pitch):

            color = GRID_DARK

        else:

            color = GRID_LIGHT


        # Make C rows slightly visible
        if pitch % 12 == 0:

            color = (
                65,
                55,
                35
            )


        draw.rectangle(
            [
                KEYBOARD_WIDTH,
                y,
                WIDTH,
                y2
            ],
            fill=color
        )


        # Horizontal line

        draw.line(
            [
                KEYBOARD_WIDTH,
                y,
                WIDTH,
                y
            ],
            fill=(55,55,55),
            width=1
        )


# ==========================
# TOP BAR
# ==========================

def draw_top_bar(draw):

    draw.rectangle(
        [
            0,
            0,
            WIDTH,
            TOP_BAR_HEIGHT
        ],
        fill=(15,15,20)
    )


    draw.line(
        [
            0,
            TOP_BAR_HEIGHT,
            WIDTH,
            TOP_BAR_HEIGHT
        ],
        fill=(90,90,90),
        width=2
    )
# ==========================
# TIME GRID
# ==========================

def draw_time_grid(
    draw,
    tempo,
    page_start,
    page_end
):
    """
    Draw beat and measure lines.
    Assumes 4/4 time.
    """

    beat_duration = 60 / tempo
    measure_duration = beat_duration * 4


    # --------------------------
    # Beat lines
    # --------------------------

    beat = (
        math.floor(
            page_start / beat_duration
        ) * beat_duration
    )


    while beat <= page_end:

        x = time_to_x(
            beat,
            page_start
        )


        draw.line(
            [
                x,
                TOP_BAR_HEIGHT,
                x,
                HEIGHT
            ],
            fill=BEAT_LINE,
            width=1
        )


        beat += beat_duration


    # --------------------------
    # Measure lines
    # --------------------------

    measure = (
        math.floor(
            page_start / measure_duration
        ) * measure_duration
    )


    while measure <= page_end:

        x = time_to_x(
            measure,
            page_start
        )


        draw.line(
            [
                x,
                TOP_BAR_HEIGHT,
                x,
                HEIGHT
            ],
            fill=BAR_LINE,
            width=3
        )


        measure += measure_duration


# ==========================
# TOP TIMELINE
# ==========================

def draw_timeline(
    draw,
    tempo,
    page_start,
    page_end
):
    """
    Draw measure numbers at the top.
    """

    font = load_font(20)

    beat_duration = 60 / tempo
    measure_duration = beat_duration * 4


    measure = (
        math.floor(
            page_start / measure_duration
        ) * measure_duration
    )


    measure_number = (
        int(
            measure / measure_duration
        ) + 1
    )


    while measure <= page_end:

        x = time_to_x(
            measure,
            page_start
        )


        # Measure number
        draw.text(
            (
                x + 10,
                15
            ),
            str(measure_number),
            font=font,
            fill=TEXT
        )


        # Small ticks for beats
        for i in range(4):

            beat_x = (
                x +
                (i * (
                    (WIDTH - KEYBOARD_WIDTH)
                    / PAGE_SECONDS
                    * beat_duration
                ))
            )


            if beat_x > WIDTH:
                break


            draw.line(
                [
                    beat_x,
                    45,
                    beat_x,
                    TOP_BAR_HEIGHT
                ],
                fill=TEXT,
                width=1
            )


        measure += measure_duration
        measure_number += 1


# ==========================
# PAGE HEADER
# ==========================

def draw_page_info(
    draw,
    page_number,
    page_start,
    page_end
):
    """
    Show page time range.
    """

    font = load_font(16)


    text = (
        f"Page {page_number} | "
        f"{page_start:.1f}s - {page_end:.1f}s"
    )


    draw.text(
        (
            WIDTH - 260,
            18
        ),
        text,
        font=font,
        fill=(180, 180, 180)
    )
# ==========================
# MIDI NOTE DRAWING
# ==========================

def draw_notes(
    draw,
    notes,
    page_start,
    page_end,
    min_pitch,
    max_pitch
):

    for note in notes:

        start = note["start"]
        end = note["end"]


        # Skip notes outside page
        if end < page_start or start > page_end:
            continue


        # Clip notes crossing page boundaries
        start = max(start, page_start)
        end = min(end, page_end)


        x1 = time_to_x(
            start,
            page_start
        )

        x2 = time_to_x(
            end,
            page_start
        )


        y = pitch_to_y(
            note["pitch"],
            min_pitch,
            max_pitch
        )


        note_height = (
            HEIGHT - TOP_BAR_HEIGHT
        ) / (
            max_pitch - min_pitch + 1
        )


        velocity = note.get(
            "velocity",
            100
        )


        # Velocity controls brightness
        brightness = (
            100 +
            int(
                velocity / 127 * 155
            )
        )


        color = (
            brightness,
            180,
            40
        )


        # Main note block
        draw.rounded_rectangle(
            [
                x1,
                y + 2,
                x2,
                y + note_height - 2
            ],
            radius=6,
            fill=color,
            outline=NOTE_BORDER,
            width=2
        )


# ==========================
# MAIN GENERATOR
# ==========================

def create_piano_roll(
    notes_file,
    tempo,
    output_folder="outputs/piano_roll"
):

    print("\n" + "="*50)
    print("🎹 MusicMind FL Piano Roll")
    print("="*50)


    # Load notes
    with open(
        notes_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    notes = data["notes"]


    if not notes:
        raise Exception(
            "No notes found!"
        )


    # Create output folder
    os.makedirs(
        output_folder,
        exist_ok=True
    )


    # Song range
    min_pitch = min(
        n["pitch"] for n in notes
    )


    max_pitch = max(
        n["pitch"] for n in notes
    )


    duration = max(
        n["end"] for n in notes
    )


    pages = math.ceil(
        duration / PAGE_SECONDS
    )


    print(
        f"Song length: {duration:.2f}s"
    )

    print(
        f"Pages: {pages}"
    )


    # ======================
    # Generate pages
    # ======================

    for page in range(pages):

        page_start = (
            page * PAGE_SECONDS
        )


        page_end = min(
            duration,
            page_start + PAGE_SECONDS
        )


        print(
            f"Rendering page {page+1}/{pages}"
        )


        img, draw = create_canvas()


        # Draw order matters

        draw_top_bar(
            draw
        )


        draw_note_lanes(
            draw,
            min_pitch,
            max_pitch
        )


        draw_keyboard(
            draw,
            min_pitch,
            max_pitch
        )


        draw_time_grid(
            draw,
            tempo,
            page_start,
            page_end
        )


        draw_timeline(
            draw,
            tempo,
            page_start,
            page_end
        )


        draw_notes(
            draw,
            notes,
            page_start,
            page_end,
            min_pitch,
            max_pitch
        )


        draw_page_info(
            draw,
            page + 1,
            page_start,
            page_end
        )


        # Save image

        filename = os.path.join(
            output_folder,
            f"page_{page+1:03}.png"
        )


        img.save(
            filename,
            quality=100
        )


        print(
            f"Saved {filename}"
        )


    print("\n" + "="*50)
    print("✅ Piano Roll Complete")
    print("="*50)


    print(
        f"Images saved in: {output_folder}"
    )
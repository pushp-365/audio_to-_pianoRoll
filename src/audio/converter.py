import os
import subprocess
import shutil


def get_ffmpeg():
    ffmpeg = shutil.which("ffmpeg")

    if ffmpeg:
        return ffmpeg

    raise FileNotFoundError(
        "FFmpeg not found.\n"
        "Please install FFmpeg and add it to your PATH.\n"
        "See the installation guide in README.md"
    )


def convert_audio(path):
    os.makedirs("outputs", exist_ok=True)

    output_path = "outputs/input.wav"

    ffmpeg = get_ffmpeg()

    command = [
        ffmpeg,
        "-y",
        "-i",
        path,
        "-ar",
        "44100",
        "-ac",
        "2",
        output_path,
    ]

    print("Converting with FFmpeg...")

    subprocess.run(command, check=True)

    print("Conversion complete!")

    return output_path
import os
import sys
import subprocess
import torch


def separate_audio(
    path,
    model="mdx_extra_q",
    device=None,
    output_dir="outputs/separated"
):
    """
    Separate audio into stems using Demucs.

    Parameters:
        path (str):
            Path to input audio file.

        model (str):
            Demucs model.
            Options:
            - mdx_extra_q (fast)
            - htdemucs (high quality)
            - htdemucs_ft (best quality)

        device (str):
            cuda or cpu.
            Automatically selected if None.

        output_dir (str):
            Directory to store separated stems.

    Returns:
        bool:
            True if successful, False otherwise.
    """

    # Automatically select device
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Build Demucs command
    command = [
        sys.executable,
        "-m",
        "demucs",
        "-n",
        model,
        "--device",
        device,
        "--out",
        output_dir,
        path
    ]

    # Display information
    print("\n" + "=" * 60)
    print("🎵 AI MUSIC SEPARATION ENGINE")
    print("=" * 60)
    print(f"Input  : {path}")
    print(f"Model  : {model}")
    print(f"Device : {device}")

    if device == "cuda":
        print(f"GPU    : {torch.cuda.get_device_name(0)}")

    print(f"Output : {output_dir}")
    print("=" * 60)

    # Run Demucs
    try:
        subprocess.run(
            command,
            check=True
        )

    except FileNotFoundError:
        print("\n❌ Python interpreter not found.")
        return False

    except subprocess.CalledProcessError as error:
        print("\n❌ Demucs failed.")
        print(f"Error code: {error.returncode}")
        return False

    except Exception as error:
        print("\n❌ Unexpected error:")
        print(error)
        return False

    print("\n" + "=" * 60)
    print("✅ Separation completed successfully!")
    print("=" * 60)

    return True
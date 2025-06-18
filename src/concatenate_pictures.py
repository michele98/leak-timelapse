import os
import uuid
import shutil
import subprocess


def concatenate_pictures(input_folder: str, output_path: str, fps: int = 10, workdir: str = None):
    """
    Creates a video from images in the input_folder using ffmpeg and saves it to output_path.

    Args:
        input_folder (str): Path to the folder containing input images.
        output_path (str): Path to save the output video.
    """

    # Create workdir if it does not exist
    workdir_created = False
    if workdir is None:
        workdir = os.path.abspath(os.path.join("temp", uuid.uuid4().hex))
        os.makedirs(workdir, exist_ok=True)
        workdir_created = True


    # Get a sorted list of image files in the input folder
    image_files = sorted(
        [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    )

    # Create a temporary file to store the list of images
    file_list_path = os.path.join(workdir, "file_list.txt")
    with open(file_list_path, "w") as f:
        for image_file in image_files:
            f.write(f"file '{os.path.join(input_folder, image_file)}'\n")

    # Create the output directory if it does not exist
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    try:
        # ffmpeg command to create a video from the image list
        command = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-f", "concat",  # Use concat format
            "-safe", "0",  # Allow unsafe file paths
            "-i", file_list_path,  # Input file list
            "-c:v", "libx264",  # Use H.264 codec
            "-pix_fmt", "yuv420p",  # Pixel format for compatibility
            "-r", str(fps),  # Set frame rate (adjust as needed)
            "-x264-params", "keyint=1",  # Make every frame a key frame
            output_path  # Output video file
        ]

        # Run the ffmpeg command
        subprocess.run(command, check=True)
    finally:
        if workdir_created:
            shutil.rmtree(workdir)


def concatenate_pictures_gif(input_folder: str, output_path: str, fps: int = 5, resize=512, last_delay_multiplier=2):
    """
    Creates a GIF from images in the input_folder using ffmpeg and saves it to output_path.

    Args:
        input_folder (str): Path to the folder containing input images.
        output_path (str): Path to save the output GIF.
        fps (int): Frames per second for the GIF.
        resize (int): Size of the output GIF.
    """

    # Create the output directory if it does not exist
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    command = [
        "convert",
        "-resize", f"{resize}x{resize}",
        "-delay", f"{100/fps}",
        "-loop", "0",
        f"{input_folder}/*.jpg",
        output_path
        ]

    subprocess.run(command, check=True)

import os
import uuid
import shutil
import subprocess


def concatenate_pictures(input_folder: str, output_path: str, fps: int = 10, workdir: str = None, frame_multiplier: int = 5, loop=True, size: int = None):
    """
    Creates a video from images in the input_folder using ffmpeg and saves it to output_path.

    Args:
        input_folder (str): Path to the folder containing input images.
        output_path (str): Path to save the output video.
        fps (int): fps of the output video.
        frame_multiplier (int): how many times to duplicate each frame.
        loop (bool): if True, the video is looped.
            If False, the multiplied frames are put next to each other, effectively slowing down the video.
        size (int): width and height of the output video. If not provided, use the size of the input imagesy
    """

    # Create workdir if it does not exist
    workdir_created = False
    if workdir is None:
        workdir = os.path.abspath(os.path.join("temp", "frames", uuid.uuid4().hex))
        os.makedirs(workdir, exist_ok=True)
        workdir_created = True
    else:
        # Work in the frames subfolder in order not to mess up other things
        workdir = os.path.join(workdir, "frames")
        os.makedirs(workdir, exist_ok=True)

    for filename in [name for name in os.listdir(input_folder) if name.lower().endswith(('.jpg', '.jpeg', '.png'))]:
        for i in range(frame_multiplier):
            if loop:
                target_filename = f"{i:04d}_" + filename
            else:
                target_filename = filename.split(".")[-2] + f"_{i:04d}." + filename.split(".")[-1]
            shutil.copy(os.path.join(input_folder, filename), os.path.join(workdir, target_filename))

    # Create a temporary file to store the list of images
    file_list_path = os.path.join(workdir, "file_list.txt")
    with open(file_list_path, "w") as f:
        for image_file in sorted(name for name in os.listdir(workdir) if name!="file_list.txt"):
            f.write(f"file '{os.path.join(workdir, image_file)}'\n")

    # Create the output directory if it does not exist
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    try:
        # ffmpeg command to create a video from the image list and resize it
        command = [
            "ffmpeg",
            "-y",  # Overwrite output file if it exists
            "-f", "concat",  # Use concat format
            "-safe", "0",  # Allow unsafe file paths
            "-i", file_list_path,  # Input file list
            "-c:v", "libx264",  # Use H.264 codec
            "-pix_fmt", "yuv420p",  # Pixel format for compatibility
            "-r", str(fps),  # Set frame rate (adjust as needed)
        ]

        if size is not None:
            command += ["-vf", f"scale={size}:-1"]

        command += [
            "-crf", "27",
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

import os
import shutil

from src import concatenate_pictures, align_all_images, concatenate_pictures_gif


IMAGE_LIST = sorted(os.listdir("pictures"))[2:]

FRAMES_LIST_VIDEO = [
    "20250611_232336.jpg",
    "20250613_211243.jpg",
    "20250615_011058.jpg",
    "20250615_222355.jpg",
    "20250616_195033.jpg",
    "20250617_193733.jpg",
    "20250618_184236.jpg",
    "20250619_194322.jpg"
] # Subset of frames used for video creation


def main():
    # Create ALIGNED_PICTURES_FOLDER

    PICTURES_FOLDER = os.path.abspath("pictures")
    ALIGNED_PICTURES_FOLDER = os.path.abspath("aligned_pictures")

    WORKDIR = os.path.abspath("temp/main")
    if os.path.exists(WORKDIR):
        shutil.rmtree(WORKDIR)
    os.makedirs(WORKDIR)

    # Create or reset ALIGNED_FOLDER
    if not os.path.exists(ALIGNED_PICTURES_FOLDER):
        os.makedirs(ALIGNED_PICTURES_FOLDER)

    if sorted([name for name in os.listdir(ALIGNED_PICTURES_FOLDER) if name.lower().endswith(('.jpg', '.jpeg', '.png'))]) != sorted(IMAGE_LIST):
        shutil.rmtree(ALIGNED_PICTURES_FOLDER)
        os.makedirs(ALIGNED_PICTURES_FOLDER)

        input_folder = os.path.join(WORKDIR, "inputs")
        if os.path.exists(input_folder):
            shutil.rmtree(input_folder)
        os.makedirs(input_folder)

        for filename in IMAGE_LIST:
            shutil.copy(os.path.join(PICTURES_FOLDER, filename), os.path.join(input_folder, filename))

        align_all_images(input_folder, ALIGNED_PICTURES_FOLDER, overlay_timestamps=True)

    FRAMES_FOLDER = os.path.join(WORKDIR, "video_frames")
    os.makedirs(FRAMES_FOLDER, exist_ok=True)
    FRAMES_FOLDER_TIMESTAMPS = os.path.join(WORKDIR, "video_frames_timestamps")
    os.makedirs(FRAMES_FOLDER_TIMESTAMPS, exist_ok=True)

    for filename in FRAMES_LIST_VIDEO:
        shutil.copy(os.path.join(ALIGNED_PICTURES_FOLDER, filename), os.path.join(FRAMES_FOLDER, filename))
        shutil.copy(os.path.join(ALIGNED_PICTURES_FOLDER, "with_timestamps", filename), os.path.join(FRAMES_FOLDER_TIMESTAMPS, filename))

    output_path = os.path.abspath("out/perdita_loop.mp4")
    concatenate_pictures(FRAMES_FOLDER, output_path, fps=25, frame_multiplier=20, loop=True, size=1024)
    print(f"Video created successfully at {output_path}")

    output_path = os.path.abspath("out/perdita.mp4")
    concatenate_pictures(FRAMES_FOLDER_TIMESTAMPS, output_path, fps=25, frame_multiplier=5, loop=False, size=1024)
    print(f"Video created successfully at {output_path}")

    output_path = os.path.abspath("out/perdita.gif")
    concatenate_pictures_gif(FRAMES_FOLDER_TIMESTAMPS, output_path, fps=3, resize=1024, last_delay_multiplier=2)
    print(f"GIF created successfully at {output_path}")


if __name__ == "__main__":
    main()
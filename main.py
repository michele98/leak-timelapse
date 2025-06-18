import os
import shutil

from src import concatenate_pictures, align_all_images, concatenate_pictures_gif


FRAMES_LIST = [
    "20250611_232336.jpg",
    "20250613_211243.jpg",
    "20250615_011058.jpg",
    "20250615_222355.jpg",
    "20250616_195033.jpg",
    "20250617_193733.jpg",
    "20250618_184236.jpg"
]


if __name__ == "__main__":
    # Create ALIGNED_PICTURES_FOLDER

    PICTURES_FOLDER = os.path.abspath("pictures")
    ALIGNED_PICTURES_FOLDER = os.path.abspath("aligned_pictures")

    WORKDIR = os.path.abspath("temp")
    if os.path.exists(WORKDIR):
        shutil.rmtree(WORKDIR)
    os.makedirs(WORKDIR)

    # Create or reset ALIGNED_FOLDER
    if not os.path.exists(ALIGNED_PICTURES_FOLDER):
        os.makedirs(ALIGNED_PICTURES_FOLDER)

    if sorted(os.listdir(ALIGNED_PICTURES_FOLDER)) != sorted(FRAMES_LIST):
        shutil.rmtree(ALIGNED_PICTURES_FOLDER)
        os.makedirs(ALIGNED_PICTURES_FOLDER)

        input_folder = os.path.join(WORKDIR, "inputs")
        if os.path.exists(input_folder):
            shutil.rmtree(input_folder)
        os.makedirs(input_folder)

        for filename in FRAMES_LIST:
            shutil.copy(os.path.join(PICTURES_FOLDER, filename), os.path.join(input_folder, filename))

        align_all_images(input_folder, ALIGNED_PICTURES_FOLDER)


    output_path = os.path.abspath("out/perdita.mp4")
    concatenate_pictures(ALIGNED_PICTURES_FOLDER, output_path, fps=7)
    print(f"Video created successfully at {output_path}")

    output_path = os.path.abspath("out/perdita.gif")
    concatenate_pictures_gif(ALIGNED_PICTURES_FOLDER, output_path, fps=3, resize=1024, last_delay_multiplier=2)
    print(f"GIF created successfully at {output_path}")

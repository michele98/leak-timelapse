import cv2
import numpy as np
from typing import Tuple


def get_overlay_text(image_name):
    image_name = image_name.split(".")[0]

    date, time = image_name.split("_")

    year = date[:4]
    month = date[4:6]
    day = date[6:]

    hour = time[:2]
    minute = time[2:4]
    second = time[4:6]

    return f"{day}/{month}/{year}\n{hour}:{minute}"


def write_text_on_image(
        image: np.ndarray,
        text: str,
        position: Tuple[int] = (100, 200),
        font_scale: int = 6,
        color: Tuple[int] = (255, 255, 255),
        thickness: int = 8,
        outline_color: Tuple[int] = (0, 0, 0),
        outline_thickness: int = 1,
        line_spacing: int = 10
        ) -> np.ndarray:
    """
    Writes text on an image with an outline and saves the output.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        text (str): Text to write on the image.
        position (tuple): (x, y) coordinates for the text.
        font_scale (float): Scale of the font. Default is 1.
        color (tuple): Color of the text in BGR format. Default is white (255, 255, 255).
        thickness (int): Thickness of the text. Default is 2.
        outline_color (tuple): Color of the outline in BGR format. Default is black (0, 0, 0).
        outline_thickness (int): Thickness of the outline. Default is 1.
        line_spacing (int): Additional spacing between lines. Default is 10.

    """
    # Load the image
    image = image.copy()

    x, y = position
    font = cv2.FONT_HERSHEY_SIMPLEX
    for line in text.splitlines():
        cv2.putText(image, line, (x, y), font, font_scale, outline_color, outline_thickness)
        cv2.putText(image, line, (x, y), font, font_scale, color, thickness)

        # Move to the next line
        y += int(font_scale * 30) + line_spacing

    return image

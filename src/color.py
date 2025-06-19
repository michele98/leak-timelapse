import cv2
import numpy as np
from typing import Tuple


def histogram_equalization_color(image: np.ndarray, tile_size: Tuple[int] = (8,8)) -> np.ndarray:
    """Perform histogram equalization on a color image using YCrCb color space."""
    # Convert the image to YCrCb color space
    ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    y_channel, cr_channel, cb_channel = cv2.split(ycrcb_image)
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to the Y channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=tile_size)
    y_equalized = clahe.apply(y_channel)
    ycrcb_equalized = cv2.merge((y_equalized, cr_channel, cb_channel))
    return cv2.cvtColor(ycrcb_equalized, cv2.COLOR_YCR_CB2BGR)

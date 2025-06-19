import os
import cv2
import time
import numpy as np

from src.tag_image import write_text_on_image, get_overlay_text


def align_images(image1: np.ndarray, image2: np.ndarray) -> np.ndarray:
    """
    Aligns image2 to image1 using SIFT and homography.

    Args:
        image1 (np.ndarray): The reference image.
        image2 (np.ndarray): The image to be aligned.

    Returns:
        np.ndarray: The aligned version of image2.
    """
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Initialize SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and descriptors
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

    # Match descriptors using FLANN-based matcher
    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Filter matches using Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Extract matched keypoints
    points1 = np.float32([keypoints1[m.queryIdx].pt for m in good_matches])
    points2 = np.float32([keypoints2[m.trainIdx].pt for m in good_matches])

    # Compute homography
    homography, _ = cv2.findHomography(points2, points1, cv2.RANSAC)

    # Warp image2 to align with image1
    height, width, _ = image1.shape
    aligned_image2 = cv2.warpPerspective(image2, homography, (width, height))

    return aligned_image2


def compute_sift(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.SIFT_create().detectAndCompute(gray, None)


def compute_homography(keypoints1, descriptors1, keypoints2, descriptors2) -> np.ndarray:
    # Match descriptors using FLANN-based matcher
    flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Filter matches using Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Extract matched keypoints
    points1 = np.float32([keypoints1[m.queryIdx].pt for m in good_matches])
    points2 = np.float32([keypoints2[m.trainIdx].pt for m in good_matches])

    # Compute homography
    homography, _ = cv2.findHomography(points2, points1, cv2.RANSAC)

    return homography


def apply_homography(image: np.ndarray, homography: np.ndarray):
    height, width, _ = image.shape
    return cv2.warpPerspective(image, homography, (width, height))



def align_all_images(input_folder: str, output_folder: str, reference_image_name: str = None, overlay_timestamps: bool = False):
    os.makedirs(output_folder, exist_ok=True)
    if overlay_timestamps:
        os.makedirs(os.path.join(output_folder, "with_timestamps"), exist_ok=True)

    image_names = sorted(os.listdir(input_folder))

    if reference_image_name is None:
        reference_image_name = image_names[0]
        image_names = image_names[1:]

    print(f"Aligning images in {input_folder} with reference image {reference_image_name}")

    image_paths = [os.path.join(input_folder, name) for name in image_names]
    reference_image_path = os.path.join(input_folder, reference_image_name)

    images = [cv2.imread(path) for path in image_paths]
    reference_image = cv2.imread(reference_image_path)

    CROP_PRE = 3000
    CROP_POST = 200

    # save reference image and aligned images to output folder
    cropped_reference_image = reference_image[:CROP_PRE, -CROP_PRE:]
    cv2.imwrite(os.path.join(output_folder, reference_image_name), cropped_reference_image[CROP_POST:-CROP_POST, CROP_POST:-CROP_POST])
    if overlay_timestamps:
        output_path_with_timestamp = os.path.join(output_folder, "with_timestamps", reference_image_name)
        text = get_overlay_text(reference_image_name)
        tagged_image = write_text_on_image(cropped_reference_image[CROP_POST:-CROP_POST, CROP_POST:-CROP_POST], text)
        cv2.imwrite(output_path_with_timestamp, tagged_image)

    t0 = time.time()
    # compute keypoints and descriptors in reference
    print("Reference image")
    kp_ref, des_ref = compute_sift(cropped_reference_image)
    for i, (image, image_name) in enumerate(zip(images, image_names)):
        print(f"{i+1} of {len(images)}")
        cropped_image = image[:CROP_PRE, -CROP_PRE:]
        kp_target, des_target = compute_sift(cropped_image)
        homography = compute_homography(kp_ref, des_ref, kp_target, des_target)
        aligned_image = apply_homography(cropped_image, homography)
        # aligned_image = align_images(cropped_reference_image, image[:VERTICAL_CROP_PRE])

        output_path = os.path.join(output_folder, image_name)
        cv2.imwrite(output_path, aligned_image[CROP_POST:-CROP_POST, CROP_POST:-CROP_POST])
        if overlay_timestamps:
            output_path_with_timestamp = os.path.join(output_folder, "with_timestamps", image_name)
            text = get_overlay_text(image_name)
            tagged_image = write_text_on_image(aligned_image[CROP_POST:-CROP_POST, CROP_POST:-CROP_POST], text)
            cv2.imwrite(output_path_with_timestamp, tagged_image)
    t1 = time.time()
    print(f"Done in {t1-t0:.3g} s.")

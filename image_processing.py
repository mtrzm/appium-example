from pathlib import Path
from typing import Optional, Tuple

import cv2
from PIL import Image
from skimage.metrics import structural_similarity


class COLORS:
    BLACK = (0, 0, 0)


def ssim(
    image_1: Path, image_2: Path, threshold: float = 0.99
) -> Tuple[float, Optional[Path]]:
    """Compares images using Structural Similarity Index.

    Code adapted from: https://stackoverflow.com/a/71634759

    If SSIM is below provided threshold, the comparison image will be generated.

    Args:
        image_1: path to first file for comparison
        image_2: path to second file for comparison
        threshold: threshold for image equality

    Returns:
        SSIM score and optionally path to comparison image
    """
    img1 = cv2.imread(str(image_1), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(str(image_2), cv2.IMREAD_GRAYSCALE)

    score, diff = structural_similarity(img1, img2, full=True)
    # print(f"Similarity Score: {score * 100:.2f}%")

    if score >= threshold:
        return score, None

    diff = (diff * 255).astype("uint8")

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # reread the image to get colored comparison
    img2 = cv2.imread(str(image_2))

    for c in contours:
        area = cv2.contourArea(c)
        if area > 100:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img2, (x, y), (x + w, y + h), COLORS.BLACK, 2)
    
    diff = image_1.parent / f"diff-{image_1.name}-{image_2.name}.png"
    cv2.imwrite(str(diff), img2)
    return score, diff


def get_size(im_path: Path) -> Tuple[int, int]:
    """Returns image size as tuple (width, height)"""
    return Image.open(im_path).size


def resize_to_fit(
        im_to_resize: Path, target_size_image: Path, output_name: Path = None
    ) -> Path:
    """Resize image with preserving ICC profile.

    Args:
        im_to_resize: path to file to be resized
        target_size_image: path to file from which dimensions will be read
        output_name: name to which save resized image

    Returns:
        Path to resized file
    """
    target_size = get_size(target_size_image)
    img = Image.open(im_to_resize)
    resized = img.resize(target_size)

    if output_name is None:
        output_name = im_to_resize.with_stem(f"{im_to_resize.stem}-resized")
    
    resized.save(output_name, icc_profile=img.info.get("icc_profile"))
    return output_name

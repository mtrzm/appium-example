"""Library for reading and processing images."""
from pathlib import Path
from typing import Tuple

from PIL import Image


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

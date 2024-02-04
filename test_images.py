import pathlib

import pytest

import image_processing
import lib_appium

TEST_DATA = pathlib.Path("test_data")
IMAGE_1 = TEST_DATA / "IMAGE_1.png"
IMAGE_2 = TEST_DATA / "IMAGE_2.png"
EXPORTED = TEST_DATA / "IMAGE_1.jpg"
THRESHOLD = 0.99


@pytest.mark.parametrize("input_image", [IMAGE_1])
def test_load_image(driver, input_image):
    screenshot_path = lib_appium.take_screenshot(driver)
    resized = image_processing.resize_to_fit(screenshot_path, input_image)
    score, comparison = image_processing.ssim(input_image, resized, THRESHOLD)

    assert score > THRESHOLD, f"Image similarity ({score:.2f}) below threshold ({THRESHOLD}), difference saved to: {comparison.absolute()}"


@pytest.mark.parametrize("input_image", [IMAGE_1])
def test_export(driver, input_image):
    exported = lib_appium.export_file(driver)

    assert exported.exists()


@pytest.mark.parametrize("exported_image, reference", [(EXPORTED, IMAGE_2)])
def test_compare_exported(exported_image, reference):
    score, comparison = image_processing.ssim(exported_image, reference, THRESHOLD)
    assert score > THRESHOLD, f"Image similarity ({score:.2f}) below threshold ({THRESHOLD}), difference saved to: {comparison.absolute()}"

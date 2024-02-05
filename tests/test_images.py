"""
Test Plan:
1. Start any Image Editing application for desktop that can import & export images with different formats (ex. Paint)
2. Import Image: IMAGE_1
3. Verify with image comparison that the imported Image looks correctly in the Image Editor
4. Export the Image in JPG format to a local drive
5. Verify that the exported image exists
6. Verify with image comparison whether the exported image is equal to IMAGE_2 (to be failed)
7. Generate an error report 

"""
import pathlib

import allure
import pytest

from lib import image_processing
from lib import lib_appium

TEST_DATA = pathlib.Path(__file__).parent.parent / "test_data"
IMAGE_1 = TEST_DATA / "IMAGE_1.png"
IMAGE_2 = TEST_DATA / "IMAGE_2.png"
EXPORTED = TEST_DATA / "IMAGE_1.jpg"
THRESHOLD = 0.99


@pytest.mark.parametrize("input_image", [IMAGE_1])
def test_load_image(driver, input_image):
    """Verifies that loaded image is properly displayed.
    
    Test steps:
    1. Open IMAGE_1.png
    2. Save screenshot
    3. Resize screenshot to the same size as input file
    4. Calculate SSIM for input file and the screenshot
    """
    screenshot_path = lib_appium.take_screenshot(driver)
    resized = image_processing.resize_to_fit(screenshot_path, input_image)
    score, comparison = image_processing.ssim(input_image, resized, THRESHOLD)
    if comparison:
        allure.attach.file(input_image, name="Input image", attachment_type=allure.attachment_type.PNG)
        allure.attach.file(resized, name="Screenshot", attachment_type=allure.attachment_type.PNG)
        allure.attach.file(comparison, name="Comparison", attachment_type=allure.attachment_type.PNG)

    assert (
        score > THRESHOLD
    ), f"Image similarity ({score:.2f}) below threshold ({THRESHOLD}), difference saved to: {comparison.absolute()}"


@pytest.mark.parametrize("input_image", [IMAGE_1])
def test_export(driver, input_image):
    """Verifies that Preview app is able to export input file to JPEG.

    Test steps:
    1. Open IMAGE_1.png
    2. Export file to JPEG format
    3. Verify that screenshot file is created
    """
    exported = lib_appium.export_file(driver)

    assert exported.exists()


@pytest.mark.parametrize("exported_image, reference", [(EXPORTED, IMAGE_2)])
def test_compare_exported(exported_image, reference):
    """Compares saved file with reference image.

    Test depends on execution of `test_export`. Scenario was split into separate
    tests to add granurality to the report.

    Test steps:
    1. Calculate SSIM for exported image and reference file
    """
    score, comparison = image_processing.ssim(exported_image, reference, THRESHOLD)
    if comparison:
        allure.attach.file(exported_image, name="Exported image", attachment_type=allure.attachment_type.PNG)
        allure.attach.file(reference, name="Reference image", attachment_type=allure.attachment_type.PNG)
        allure.attach.file(comparison, name="Comparison", attachment_type=allure.attachment_type.PNG)
    assert (
        score > THRESHOLD
    ), f"Image similarity ({score:.2f}) below threshold ({THRESHOLD}), difference saved to: {comparison.absolute()}"

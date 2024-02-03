import pathlib

import pytest

import lib_appium


IMAGE_1 = pathlib.Path("test_data/IMAGE_1.png")
IMAGE_2 = pathlib.Path("test_data/IMAGE_2.png")


@pytest.mark.parametrize("path", [IMAGE_1])
def test_screenshot(driver, path):
    screenshot_path = lib_appium.take_screenshot(driver)

    assert screenshot_path.exists()


@pytest.mark.parametrize("path", [IMAGE_1])
def test_export(driver, path):
    exported = lib_appium.export_file(driver)

    assert exported.exists()

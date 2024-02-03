import pathlib

import pytest

import lib_appium


IMAGE_1 = pathlib.Path("test_data/IMAGE_1.png")
IMAGE_2 = pathlib.Path("test_data/IMAGE_2.png")


@pytest.mark.parametrize("path", [IMAGE_1])
def test_export(path):
    service, driver = lib_appium.start_driver()
    lib_appium.open_file(driver)
    exported = lib_appium.export_file(driver)
    lib_appium.stop_driver(service, driver)

    assert exported.exists()

import pytest

from lib import lib_appium


@pytest.fixture
def driver():
    service, driver = lib_appium.start_driver()
    lib_appium.open_file(driver)
    yield driver

    lib_appium.stop_driver(service, driver)

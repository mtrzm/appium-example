import pathlib
import time

from appium import webdriver
from appium.options.mac import Mac2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy


PAGE_SOURCE = pathlib.Path(__file__).parent / "tmp/page_source.xml"
IMAGE_1 = pathlib.Path("test_data/IMAGE_1.png")


def configure_options():
    options = Mac2Options()
    options.bundle_id = "com.apple.Preview"
    options.platform_name = "mac"
    options.arguments = [str(IMAGE_1)]
    options.show_server_logs = True
    return options


def open_file(driver, file_path=None):
    """Opens file from file_path in Preview App.

    Currently I'm not able to reliably open requested file, so I've hardcoded
    using recent files in Preview App.

    When I'm using Mac2Options.arguments, the requested file is sometimes opened,
    sometimes not opened and there's also error about missing file permissions.
    """
    driver.find_element(by=AppiumBy.XPATH, value='//XCUIElementTypeMenuItem[@title="IMAGE_1.png —  test_data"]').click()
    time.sleep(1)


def export_file(driver):
    driver.find_element(by=AppiumBy.XPATH, value='//XCUIElementTypeMenuItem[@title="Export…"]').click()
    time.sleep(1)

    save_panel = driver.find_element(by=AppiumBy.XPATH, value='//XCUIElementTypeSheet[@identifier="save-panel"]')
    format_selection = save_panel.find_element(by=AppiumBy.XPATH, value='//XCUIElementTypePopUpButton[@identifier="_NS:120"]')
    format_selection.click()
    time.sleep(0.5)
    format_selection.find_element(by=AppiumBy.XPATH, value='//XCUIElementTypeMenuItem[@title="JPEG"]').click()
    time.sleep(0.5)

    save_panel.find_element(by=AppiumBy.XPATH, value='//XCUIElementTypeButton[@identifier="OKButton"]').click()
    time.sleep(2)
    return IMAGE_1.with_suffix(".jpg")


def start_driver():
    options = configure_options()

    appium_service = AppiumService()
    appium_service.start()

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    time.sleep(2)
    return appium_service, driver


def stop_driver(service, driver):
    driver.quit()
    service.stop()


# service, driver = start_driver()
# open_file(driver)
# export_file(driver)
# stop_driver(service, driver)

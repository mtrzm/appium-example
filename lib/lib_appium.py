"""Simple wrapper for Appium to automate Preview application on MacOS.

Sleep times are arbitrary numbers. Probably could be optimized.
"""
import pathlib
import time
from typing import Tuple

from appium import webdriver
from appium.options.mac import Mac2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy

PAGE_SOURCE = pathlib.Path(__file__).parent.parent / "tmp/page_source.xml"
IMAGE_1 = pathlib.Path("test_data/IMAGE_1.png")


class XPaths:
    """XPaths for page objects. This is not a complete list."""

    BUTTON = "XCUIElementTypeButton"
    IMAGE = "XCUIElementTypeImage"
    MENU_ITEM = "XCUIElementTypeMenuItem"
    POP_UP_BUTTON = "XCUIElementTypePopUpButton"
    TYPE_SHEET = "XCUIElementTypeSheet"
    WINDOW = "XCUIElementTypeWindow"


def configure_options() -> Mac2Options:
    """Configures start options for Appium driver.

    Driver should load `Preview` application as DUT and open
    IMAGE_1.png at startup.

    Returns:
        Mac2Options object with start options.
    """
    options = Mac2Options()
    options.bundle_id = "com.apple.Preview"
    options.platform_name = "mac"
    options.arguments = [str(IMAGE_1)]
    options.show_server_logs = True
    return options


def open_file(driver: webdriver.Remote, file_path: pathlib.Path = None) -> None:
    """Opens file from file_path in Preview App.

    Currently I'm not able to reliably open requested file, so I've hardcoded
    using recent files in Preview App.

    When I'm using Mac2Options.arguments, the requested file is sometimes opened,
    sometimes not and there's also sometimes error about missing file permissions.

    Args:
        driver: web driver for Preview App
    """
    driver.find_element(
        by=AppiumBy.XPATH,
        value=f'//{XPaths.MENU_ITEM}[@title="IMAGE_1.png —  test_data"]',
    ).click()
    time.sleep(1)


def export_file(driver: webdriver.Remote) -> pathlib.Path:
    """Exports current file to JPEG format.

    Only happy path is covered. Function is not expecting errors like missing
    image, inactive buttons, overwritting existing file.

    Args:
        driver: web driver for Preview App

    Returns:
        Path to exported JPEG file.
    """
    driver.find_element(
        by=AppiumBy.XPATH, value=f'//{XPaths.MENU_ITEM}[@title="Export…"]'
    ).click()
    time.sleep(1)

    save_panel = driver.find_element(
        by=AppiumBy.XPATH, value=f'//{XPaths.TYPE_SHEET}[@identifier="save-panel"]'
    )
    # TODO check if ID for format selection is permanent
    format_selection = save_panel.find_element(
        by=AppiumBy.XPATH, value=f'//{XPaths.POP_UP_BUTTON}[@identifier="_NS:120"]'
    )
    format_selection.click()
    time.sleep(0.5)
    format_selection.find_element(
        by=AppiumBy.XPATH, value=f'//{XPaths.MENU_ITEM}[@title="JPEG"]'
    ).click()
    time.sleep(0.5)

    save_panel.find_element(
        by=AppiumBy.XPATH, value=f'//{XPaths.BUTTON}[@identifier="OKButton"]'
    ).click()
    time.sleep(2)
    return IMAGE_1.with_suffix(".jpg")


def take_screenshot(driver: webdriver.Remote):
    """Saves screenshot of currently opened image.

    Only happy path is covered. Function is not expecting errors.

    Args:
        driver: web driver for Preview App

    Returns:
        Path to screenshot as PNG file.
    """
    target_path = IMAGE_1.with_stem(f"{IMAGE_1.stem}-screenshot")

    preview_app = driver.find_element(
        by=AppiumBy.XPATH,
        value=f'//{XPaths.WINDOW}[@identifier="PVDocumentWindow"]',
    )
    image = preview_app.find_element(by=AppiumBy.XPATH, value=f"//{XPaths.IMAGE}")
    image.screenshot(str(target_path))

    return target_path


def start_driver() -> Tuple[AppiumService, webdriver.Remote]:
    """Starts Appium session for Preview App.
    
    Returns:
        AppiumService and webdriver objects.
    """
    options = configure_options()

    appium_service = AppiumService()
    appium_service.start()

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    time.sleep(2)
    return appium_service, driver


def stop_driver(service: AppiumService, driver: webdriver.Remote):
    """Stops Appium session.
    
    Args:
        service: AppiumService instance
        driver: webdriver instance
    """
    driver.quit()
    service.stop()


def _dump_page_source(
    driver: webdriver.Remote, export_file: pathlib.Path = PAGE_SOURCE
):
    export_file.write_text(driver.page_source)

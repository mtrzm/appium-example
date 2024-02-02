import pathlib
import time

from appium import webdriver
from appium.options.mac import Mac2Options
from appium.webdriver.appium_service import AppiumService


options = Mac2Options()
options.bundle_id = "com.apple.ActivityMonitor"

appium_service = AppiumService()
appium_service.start()

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
time.sleep(5)

with open(f"{str(pathlib.Path(__file__).parent)}/page_source_activity_monitor.xml", "w") as ps:
    ps.write(driver.page_source)

appium_service.stop()

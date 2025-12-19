from selenium import webdriver
import pytest
import os
from datetime import datetime
from pytest_html import extras

def pytest_addoption(parser):
    parser.addoption(
        "--browsername", action="store", default="firefox", help="browser selection"
    )

@pytest.fixture(scope="function")
def browserinvoke(request):
    browsername = request.config.getoption("browsername")
    if browsername == "chrome":
        chromeoptions = webdriver.ChromeOptions()
        chromeoptions.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chromeoptions)
    elif browsername == "firefox":
        firefoxoptions = webdriver.FirefoxOptions()
        firefoxoptions.add_argument("--start-maximized")
        driver = webdriver.Firefox(options=firefoxoptions)
    driver.implicitly_wait(5)

    yield driver
    driver.close()

# ------------ HTML REPORT + SCREENSHOT HOOK ------------ #

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "reports", "screenshots")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:

        driver = (
            item.funcargs.get("browserinvoke")
            or item.funcargs.get("driver")
        )

        if driver:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)

            filename = f"{item.name}.png"
            file_path = os.path.join(SCREENSHOT_DIR, filename)

            driver.save_screenshot(file_path)

            extra = extras.image(file_path)
            if hasattr(rep, "extra"):
                rep.extra.append(extra)
            else:
                rep.extra = [extra]



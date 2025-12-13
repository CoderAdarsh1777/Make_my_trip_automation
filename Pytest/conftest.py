from selenium import webdriver
import pytest
import os
from datetime import datetime

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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Called after each phase of a test.
    Here we:
    - record the report on the item (rep_setup, rep_call, rep_teardown)
    - if the test FAILED in the 'call' phase, take a screenshot
      with the 'browserinvoke' driver and attach it to the HTML report.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    # Only care about actual test body failures
    if rep.when != "call" or not rep.failed:
        return

    # Get WebDriver from the test's fixtures
    driver = item.funcargs.get("browserinvoke", None)
    if driver is None:
        return

    # Base directory = the folder where THIS conftest.py lives (Pytest/)
    base_dir = os.path.dirname(__file__)
    reports_dir = os.path.join(base_dir, "reports")
    screenshots_dir = os.path.join(reports_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{item.name}_{timestamp}.png"
    file_path = os.path.join(screenshots_dir, file_name)

    # Take screenshot
    driver.save_screenshot(file_path)

    # Attach to pytest-html report (if plugin is installed/used)
    try:
        from pytest_html import extras

        extras = getattr(rep, "extra", [])
        extras.append(extras.image(file_path))
        rep.extras = extras
    except ImportError:
        # pytest-html not being used; ignore
        pass



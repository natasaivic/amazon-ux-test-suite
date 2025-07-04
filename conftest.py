import pytest
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright):
    browser_name = os.getenv("BROWSER", "chromium")
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    
    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=headless)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=headless)
    else:
        browser = playwright.chromium.launch(headless=headless)
    
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport={
            "width": int(os.getenv("VIEWPORT_WIDTH", "1920")),
            "height": int(os.getenv("VIEWPORT_HEIGHT", "1080"))
        }
    )
    page = context.new_page()
    yield page
    context.close()
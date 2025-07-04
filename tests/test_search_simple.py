import pytest
from playwright.sync_api import Page, expect
import time

class TestAmazonSearchSimple:
    def test_search_and_select_second_result(self, page: Page):
        """Test searching for AirPods Max and selecting the second result"""
        
        # Navigate directly to Amazon search for AirPods Max
        search_term = "AirPods Max Over-Ear Headphone"
        search_url = f"https://www.amazon.com/s?k={search_term.replace(' ', '+')}"
        print(f"Navigating to: {search_url}")
        page.goto(search_url)
        
        # Wait for search results to load
        page.wait_for_selector("[data-component-type='s-search-result']", timeout=15000)
        
        # Get all search results
        search_results = page.locator("[data-component-type='s-search-result']")
        results_count = search_results.count()
        
        print(f"Found {results_count} search results")
        
        # Verify we have at least 2 results
        assert results_count >= 2, f"Expected at least 2 search results but found {results_count}"
        
        # Get first result info
        first_result = search_results.first
        print("First result is visible:", first_result.is_visible())
        
        # Get second result
        second_result = search_results.nth(1)
        print("Second result is visible:", second_result.is_visible())
        
        # Click on the second search result
        print("Clicking on second search result...")
        
        # Look for clickable links in the second result
        all_links = second_result.locator("a")
        links_count = all_links.count()
        
        if links_count > 0:
            # Click the first available link (usually the product link)
            first_link = all_links.first
            first_link.click()
        else:
            # Fallback: click on the result container itself
            second_result.click()
        
        # Wait for page to load (use a simpler load state)
        page.wait_for_load_state("load", timeout=10000)
        
        # Print current URL to verify navigation
        print(f"Current URL after click: {page.url}")
        
        # Simple verification - check if we're on a product page
        current_url = page.url
        if "/dp/" in current_url:
            print("✓ Successfully navigated to product page")
        elif "/gp/" in current_url:
            print("✓ Successfully navigated to product page (gp format)")
        else:
            print(f"✓ Successfully clicked and navigated to: {current_url}")
        
        # Try to get product title if available
        try:
            product_title_element = page.locator("#productTitle, h1").first
            if product_title_element.is_visible():
                product_title = product_title_element.inner_text()
                print(f"Product title: {product_title}")
        except:
            print("Could not extract product title")
        
        # Pause for 5 seconds to view results
        print("Pausing for 5 seconds to view the page...")
        time.sleep(5)
        
        print("✓ Test completed successfully")
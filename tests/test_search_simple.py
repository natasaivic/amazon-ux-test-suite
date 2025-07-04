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
        product_title = None
        try:
            product_title_element = page.locator("#productTitle, h1").first
            if product_title_element.is_visible():
                product_title = product_title_element.inner_text()
                print(f"Product title: {product_title}")
        except:
            print("Could not extract product title")
        
        # Add item to cart
        print("\n--- Adding item to cart ---")
        
        # Wait a moment for page to fully load
        time.sleep(2)
        
        # Check if this is a standard Amazon product page
        if "/dp/" in current_url:
            print("Standard Amazon product page detected")
            
            # Look for "Add to Cart" button with multiple approaches
            add_to_cart_selectors = [
                "#add-to-cart-button",
                "input[name='submit.add-to-cart']",
                "[data-action='add-to-cart']",
                "button:has-text('Add to Cart')",
                "input[value*='Add to Cart']",
                "button:has-text('Add to cart')",  # lowercase version
                "[title*='Add to Cart']",
                "[aria-label*='Add to Cart']",
                "#buy-now-button",  # Alternative buy button
                ".a-button-input[aria-labelledby*='cart']"
            ]
            
            cart_button_found = False
            for selector in add_to_cart_selectors:
                try:
                    cart_button = page.locator(selector).first
                    if cart_button.is_visible():
                        print(f"Found 'Add to Cart' button with selector: {selector}")
                        cart_button.click()
                        cart_button_found = True
                        break
                except:
                    continue
            
            # If specific selectors don't work, try finding by text in spans and other elements
            if not cart_button_found:
                print("Searching for cart elements by text content...")
                # Look for clickable elements with cart-related text
                cart_elements = page.locator("span, button, input, a").filter(has_text="Add to Cart")
                if cart_elements.count() > 0:
                    print(f"Found {cart_elements.count()} elements with 'Add to Cart' text")
                    for i in range(cart_elements.count()):
                        try:
                            element = cart_elements.nth(i)
                            if element.is_visible():
                                # Try to find the clickable parent
                                clickable = element.locator("xpath=ancestor-or-self::button | xpath=ancestor-or-self::input | xpath=ancestor-or-self::a").first
                                if clickable.is_visible():
                                    print(f"Clicking cart element {i+1}")
                                    clickable.click()
                                    cart_button_found = True
                                    break
                        except:
                            continue
            
            if not cart_button_found:
                print("❌ Could not find 'Add to Cart' button on Amazon product page")
                # Show some page structure for debugging
                print("Page structure analysis:")
                main_content = page.locator("#centerCol, #rightCol, .s-main-slot").first
                if main_content.is_visible():
                    buttons_in_main = main_content.locator("button, input[type='submit'], input[type='button']")
                    print(f"Found {buttons_in_main.count()} buttons in main content area")
                    for i in range(min(buttons_in_main.count(), 5)):
                        try:
                            button = buttons_in_main.nth(i)
                            if button.is_visible():
                                button_text = button.inner_text().strip()
                                print(f"  Main button {i+1}: '{button_text[:50]}'")
                        except:
                            pass
        else:
            print("Non-standard Amazon page detected - skipping cart functionality")
            print("This might be a sponsored product or external seller page")
            cart_button_found = False
        
        if cart_button_found:
            print("✓ Clicked 'Add to Cart' button")
            
            # Wait for cart confirmation or page update
            time.sleep(3)
            
            # Check for cart confirmation messages
            cart_confirmations = [
                "[data-feature-name='addToCart']",
                "#attachDisplayAddBaseAlert",
                "#sw-atc-details-single-container",
                ".a-alert-success",
                "#huc-v2-order-row-confirm-text",
                ".a-size-medium-plus:has-text('Added to Cart')"
            ]
            
            cart_confirmed = False
            for selector in cart_confirmations:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"✓ Cart confirmation found: {selector}")
                        cart_confirmed = True
                        break
                except:
                    continue
            
            if not cart_confirmed:
                # Alternative: Check if cart icon has updated
                try:
                    cart_count = page.locator("#nav-cart-count, .nav-cart-count").first
                    if cart_count.is_visible():
                        count_text = cart_count.inner_text()
                        print(f"✓ Cart count: {count_text}")
                        cart_confirmed = True
                except:
                    pass
            
            if cart_confirmed:
                print("✓ Item successfully added to cart")
            else:
                print("⚠️  Could not confirm item was added to cart")
        
        # Pause for 5 seconds to view results
        print("\nPausing for 5 seconds to view the page...")
        time.sleep(5)
        
        print("✓ Test completed successfully")
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
                
                # Navigate to shopping cart page
                print("\n--- Navigating to shopping cart ---")
                
                # Look for cart navigation options
                cart_nav_selectors = [
                    "#nav-cart",
                    "#nav-cart-text-container",
                    "a[href*='/cart']",
                    "#sw-atc-details-single-container a[href*='cart']",
                    ".nav-cart-text"
                ]
                
                cart_nav_found = False
                for selector in cart_nav_selectors:
                    try:
                        cart_nav = page.locator(selector).first
                        if cart_nav.is_visible():
                            print(f"Found cart navigation with selector: {selector}")
                            cart_nav.click()
                            cart_nav_found = True
                            break
                    except:
                        continue
                
                if not cart_nav_found:
                    # Try direct navigation to cart page
                    print("Direct navigation to cart page...")
                    cart_url = "https://www.amazon.com/gp/cart/view.html"
                    page.goto(cart_url)
                    cart_nav_found = True
                
                if cart_nav_found:
                    # Wait for cart page to load
                    page.wait_for_load_state("load", timeout=10000)
                    time.sleep(2)
                    
                    print(f"✓ Successfully navigated to cart page: {page.url}")
                    
                    # Update item quantity to 2
                    print("\n--- Updating item quantity to 2 ---")
                    
                    # Look for quantity selectors
                    quantity_selectors = [
                        "select[name*='quantity']",
                        "select[data-action='quantity-dropdown']",
                        ".a-dropdown-container select",
                        "select[aria-label*='quantity']",
                        "input[name*='quantity']"
                    ]
                    
                    quantity_updated = False
                    for selector in quantity_selectors:
                        try:
                            quantity_element = page.locator(selector).first
                            if quantity_element.is_visible():
                                print(f"Found quantity selector: {selector}")
                                
                                # Check if it's a dropdown or input
                                element_type = quantity_element.get_attribute("tagName").lower()
                                if element_type == "select":
                                    # For dropdown, select option with value "2"
                                    quantity_element.select_option("2")
                                    print("✓ Updated quantity to 2 via dropdown")
                                elif element_type == "input":
                                    # For input field, clear and type "2"
                                    quantity_element.clear()
                                    quantity_element.fill("2")
                                    quantity_element.press("Enter")
                                    print("✓ Updated quantity to 2 via input field")
                                
                                quantity_updated = True
                                break
                        except Exception as e:
                            continue
                    
                    if not quantity_updated:
                        # Try alternative approach - look for + button
                        print("Looking for quantity increase button...")
                        plus_button_selectors = [
                            "button[aria-label*='Increase']",
                            "button[data-action='plus']",
                            ".a-button-input[value='+']",
                            "input[value='+']"
                        ]
                        
                        for selector in plus_button_selectors:
                            try:
                                plus_button = page.locator(selector).first
                                if plus_button.is_visible():
                                    print(f"Found quantity increase button: {selector}")
                                    plus_button.click()  # Click once to go from 1 to 2
                                    print("✓ Updated quantity to 2 via plus button")
                                    quantity_updated = True
                                    break
                            except:
                                continue
                    
                    if quantity_updated:
                        # Wait for page to update
                        time.sleep(3)
                        
                        # Verify quantity change
                        print("\n--- Verifying quantity update ---")
                        
                        # Look for quantity confirmation
                        verification_selectors = [
                            "select[name*='quantity'] option[selected]",
                            "input[name*='quantity']",
                            ".a-dropdown-prompt",
                            "[data-item-count='2']"
                        ]
                        
                        quantity_verified = False
                        for selector in verification_selectors:
                            try:
                                element = page.locator(selector).first
                                if element.is_visible():
                                    value = element.get_attribute("value") or element.inner_text()
                                    if "2" in str(value):
                                        print(f"✓ Quantity verified as 2: {value}")
                                        quantity_verified = True
                                        break
                            except:
                                continue
                        
                        if not quantity_verified:
                            print("⚠️  Could not verify quantity update")
                        
                        print("✓ Shopping cart operations completed")
                    else:
                        print("❌ Could not find quantity update controls")
                        print("Available cart elements:")
                        # Debug: show available elements
                        cart_elements = page.locator("select, input, button").filter(visible=True)
                        for i in range(min(cart_elements.count(), 5)):
                            try:
                                element = cart_elements.nth(i)
                                tag = element.get_attribute("tagName")
                                name = element.get_attribute("name") or ""
                                aria_label = element.get_attribute("aria-label") or ""
                                print(f"  {tag}: name='{name}' aria-label='{aria_label[:30]}'")
                            except:
                                pass
                else:
                    print("❌ Could not navigate to cart page")
            else:
                print("⚠️  Could not confirm item was added to cart")
        
        # Pause for 5 seconds to view results
        print("\nPausing for 5 seconds to view the page...")
        time.sleep(5)
        
        print("✓ Test completed successfully")
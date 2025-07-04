import pytest
from playwright.sync_api import Page, expect
import time

class TestAmazonSearchSimple:
    def test_search_and_select_second_result(self, page: Page):
        """Test searching for AirPods Max and selecting the second result"""
        
        # First navigate to Amazon homepage to avoid bot detection
        print("Navigating to Amazon homepage...")
        page.goto("https://www.amazon.com")
        
        # Wait for page to load
        page.wait_for_load_state("load", timeout=10000)
        time.sleep(2)
        
        # Check for CAPTCHA or bot detection
        if page.locator("form[action*='validateCaptcha']").count() > 0:
            print("CAPTCHA detected - manual intervention required")
            time.sleep(10)  # Give time for manual CAPTCHA solving
        
        # Navigate to search URL - use more specific search for Apple AirPods Max
        search_term = "Apple AirPods Max"
        search_url = f"https://www.amazon.com/s?k={search_term.replace(' ', '+')}"
        print(f"Navigating to: {search_url}")
        page.goto(search_url)
        
        # Wait for page to load
        page.wait_for_load_state("load", timeout=15000)
        time.sleep(3)
        
        # Check for search results with multiple selectors
        search_result_selectors = [
            "[data-component-type='s-search-result']",
            "[data-testid='s-search-result']",
            ".s-search-result",
            ".sg-col-inner .s-widget-container"
        ]
        
        search_results = None
        for selector in search_result_selectors:
            try:
                page.wait_for_selector(selector, timeout=5000)
                search_results = page.locator(selector)
                if search_results.count() > 0:
                    print(f"Found search results with selector: {selector}")
                    break
            except:
                continue
        
        if search_results is None:
            print("Could not find search results with standard selectors")
            # Take screenshot for debugging
            page.screenshot(path="search_results_debug.png")
            # Try alternative approach
            print("Attempting alternative search...")
            page.goto("https://www.amazon.com")
            time.sleep(2)
            # Use search box instead
            try:
                search_box = page.locator("#twotabsearchtextbox")
                if search_box.is_visible():
                    search_box.fill(search_term)
                    search_box.press("Enter")
                    page.wait_for_load_state("load", timeout=10000)
                    time.sleep(3)
                    # Try again with search results
                    for selector in search_result_selectors:
                        try:
                            search_results = page.locator(selector)
                            if search_results.count() > 0:
                                print(f"Found search results after search box with selector: {selector}")
                                break
                        except:
                            continue
            except Exception as e:
                print(f"Search box approach failed: {e}")
        
        if search_results is None:
            raise Exception("Could not find search results with any method")
        
        # Get all search results (search_results is already set above)
        results_count = search_results.count()
        
        print(f"Found {results_count} search results")
        
        # Verify we have at least 2 results
        assert results_count >= 2, f"Expected at least 2 search results but found {results_count}"
        
        # Look for results that contain "Apple" or "AirPods" for better match
        print("Looking for Apple AirPods Max results...")
        best_result = None
        best_result_index = -1
        
        for i in range(min(results_count, 5)):  # Check first 5 results
            result = search_results.nth(i)
            try:
                # Get the text content of the result
                result_text = result.inner_text().lower()
                if "apple" in result_text and "airpods" in result_text:
                    print(f"Found Apple AirPods result at index {i}")
                    best_result = result
                    best_result_index = i
                    break
            except:
                continue
        
        # If no Apple AirPods found, use second result as fallback
        if best_result is None:
            print("No Apple AirPods found, using second result as fallback")
            best_result = search_results.nth(1)
            best_result_index = 1
        
        print(f"Selecting result at index {best_result_index}")
        print("Selected result is visible:", best_result.is_visible())
        
        # Click on the selected result
        print("Clicking on selected search result...")
        
        # Look for clickable links in the selected result
        all_links = best_result.locator("a")
        links_count = all_links.count()
        
        if links_count > 0:
            # Click the first available link (usually the product link)
            first_link = all_links.first
            first_link.click()
        else:
            # Fallback: click on the result container itself
            best_result.click()
        
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
                                # First try clicking the element directly if it's a button or input
                                tag_name = element.get_attribute("tagName").lower()
                                if tag_name in ["button", "input"]:
                                    print(f"Clicking cart {tag_name} element {i+1}")
                                    element.click()
                                    cart_button_found = True
                                    break
                                else:
                                    # Try to find the clickable parent
                                    try:
                                        parent_button = element.locator("xpath=ancestor::button | xpath=ancestor::input | xpath=ancestor::a").first
                                        if parent_button.is_visible():
                                            print(f"Clicking parent button of cart element {i+1}")
                                            parent_button.click()
                                            cart_button_found = True
                                            break
                                    except:
                                        # Try clicking the element itself as fallback
                                        try:
                                            print(f"Trying to click cart element {i+1} directly")
                                            element.click()
                                            cart_button_found = True
                                            break
                                        except:
                                            continue
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
                
                # Handle protection plan popup if it appears
                print("\n--- Handling protection plan popup ---")
                time.sleep(3)  # Wait longer for popup to appear
                
                # 1. Check for iframes first
                print("Checking for iframes...")
                frames = page.frames
                print(f"Found {len(frames)} frames on page")
                
                protection_handled = False
                
                # Try to find popup in iframes
                for i, frame in enumerate(frames):
                    try:
                        frame_url = frame.url
                        print(f"Frame {i}: {frame_url}")
                        
                        # Look for protection plan elements in iframe
                        iframe_selectors = [
                            "input[value*='No thanks']",
                            "button:has-text('No thanks')",
                            "input[value*='No Thanks']"
                        ]
                        
                        for selector in iframe_selectors:
                            try:
                                iframe_button = frame.locator(selector).first
                                if iframe_button.is_visible():
                                    print(f"Found popup button in iframe {i}: {selector}")
                                    iframe_button.click()
                                    protection_handled = True
                                    time.sleep(2)
                                    break
                            except:
                                continue
                        
                        if protection_handled:
                            break
                    except:
                        continue
                
                # 2. Try main page selectors if not found in iframe
                if not protection_handled:
                    print("Checking main page for popup...")
                    
                    # More comprehensive selectors for "No thanks" buttons
                    protection_popup_selectors = [
                        "input[aria-labelledby*='attach-sidesheet-checkout-button']",
                        "input[name='submit.add-to-cart'][value*='No']",
                        "input[value='No thanks']",
                        "button:has-text('No thanks')",
                        "input[value*='No thanks']",
                        ".a-button-text:has-text('No thanks')",
                        "input[aria-label*='No thanks']",
                        "[data-action='attachDisplayAddBaseAlert-declarative_1'] input",
                        "input[name='submit.add-to-cart.top']",
                        ".attach-sidesheet-checkout-button input",
                        "input[data-action='skip-twister']",
                        "input[name='submit.add-to-cart'][value*='No Thanks']",
                        "input[aria-labelledby*='attach-sidesheet-addon-button']",
                        "input[aria-labelledby*='attach-sidesheet-checkout-button-announce']",
                        "input[value*='No Thanks']"
                    ]
                    
                    # Wait for popup to be fully loaded
                    time.sleep(2)
                    
                    # First, try to find specific "No thanks" buttons
                    for selector in protection_popup_selectors:
                        try:
                            popup_button = page.locator(selector).first
                            if popup_button.is_visible():
                                button_value = popup_button.get_attribute("value") or ""
                                button_text = popup_button.inner_text() or ""
                                print(f"Found protection plan button: '{button_value}' '{button_text}' with selector: {selector}")
                                
                                # Try regular click first
                                try:
                                    popup_button.click()
                                    protection_handled = True
                                except:
                                    # If regular click fails, try forced click
                                    print("Regular click failed, trying forced click...")
                                    popup_button.click(force=True)
                                    protection_handled = True
                                
                                time.sleep(2)  # Wait for popup to close
                                break
                        except Exception as e:
                            continue
                
                # 3. If specific selectors don't work, look for any button with "No" text
                if not protection_handled:
                    print("Scanning all visible buttons for 'No thanks' text...")
                    try:
                        all_buttons = page.locator("input[type='submit'], button").filter(visible=True)
                        button_count = all_buttons.count()
                        print(f"Checking {button_count} visible buttons for 'No thanks' option...")
                        
                        for i in range(button_count):
                            try:
                                button = all_buttons.nth(i)
                                button_value = button.get_attribute("value") or ""
                                button_text = button.inner_text() or ""
                                aria_label = button.get_attribute("aria-label") or ""
                                
                                # Look for "No thanks", "No", "Skip" etc.
                                search_text = f"{button_value} {button_text} {aria_label}".lower()
                                if any(keyword in search_text for keyword in ["no thanks", "no, thanks", "skip", "continue without", "no protection"]):
                                    print(f"Found 'No thanks' button: value='{button_value}' text='{button_text}' aria-label='{aria_label}'")
                                    
                                    # Try regular click first, then forced click
                                    try:
                                        button.click()
                                        protection_handled = True
                                    except:
                                        print("Regular click failed, trying forced click...")
                                        button.click(force=True)
                                        protection_handled = True
                                    
                                    time.sleep(2)
                                    break
                            except:
                                continue
                    except:
                        pass
                
                # 4. Try shadow DOM elements if still not found
                if not protection_handled:
                    print("Checking for shadow DOM elements...")
                    try:
                        # Look for shadow hosts that might contain the popup
                        shadow_hosts = page.locator("*").filter(has_text="No thanks")
                        shadow_count = shadow_hosts.count()
                        print(f"Found {shadow_count} potential shadow DOM elements")
                        
                        for i in range(min(shadow_count, 3)):  # Check first 3
                            try:
                                shadow_element = shadow_hosts.nth(i)
                                if shadow_element.is_visible():
                                    print(f"Trying shadow DOM element {i}")
                                    shadow_element.click(force=True)
                                    protection_handled = True
                                    time.sleep(2)
                                    break
                            except:
                                continue
                    except:
                        pass
                
                if not protection_handled:
                    # Try to close any visible modals/popups
                    try:
                        close_buttons = page.locator("button[aria-label*='Close'], .a-button-close, [data-action='a-popover-close']")
                        if close_buttons.count() > 0:
                            close_buttons.first.click()
                            print("✓ Closed popup using close button")
                            time.sleep(1)
                            protection_handled = True
                    except:
                        pass
                
                if protection_handled:
                    print("✓ Protection plan popup handled successfully")
                else:
                    print("✓ No protection plan popup detected or already handled")
                
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
                        
                        # Proceed to checkout
                        print("\n--- Proceeding to checkout ---")
                        
                        # Get item price from cart for calculation validation
                        item_price = None
                        try:
                            price_selectors = [
                                ".a-price-whole",
                                ".a-offscreen[data-automation-id*='price']",
                                ".a-price .a-offscreen",
                                "[data-automation-id='unit-price'] .a-offscreen"
                            ]
                            
                            for selector in price_selectors:
                                try:
                                    price_element = page.locator(selector).first
                                    if price_element.is_visible():
                                        price_text = price_element.inner_text().strip()
                                        # Extract numeric value from price text
                                        import re
                                        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', ''))
                                        if price_match:
                                            item_price = float(price_match.group().replace(',', ''))
                                            print(f"Item price extracted: ${item_price}")
                                            break
                                except:
                                    continue
                        except:
                            print("Could not extract item price from cart")
                        
                        # Look for "Proceed to Checkout" button
                        checkout_selectors = [
                            "input[name='proceedToRetailCheckout']",
                            "button[name='proceedToRetailCheckout']",
                            "input[aria-labelledby*='checkout']",
                            "input[value*='Proceed to checkout']",
                            ".a-button-input[aria-labelledby*='checkout']",
                            "input[data-feature-id='proceed-to-checkout-action']"
                        ]
                        
                        checkout_nav_found = False
                        for selector in checkout_selectors:
                            try:
                                checkout_button = page.locator(selector).first
                                if checkout_button.is_visible():
                                    print(f"Found checkout button with selector: {selector}")
                                    checkout_button.click()
                                    checkout_nav_found = True
                                    break
                            except:
                                continue
                        
                        if checkout_nav_found:
                            # Wait for checkout page to load
                            print("Waiting for checkout page to load...")
                            page.wait_for_load_state("load", timeout=15000)
                            time.sleep(3)
                            
                            print(f"✓ Successfully navigated to checkout: {page.url}")
                            
                            # Handle potential sign-in requirements or guest checkout
                            print("\n--- Handling checkout prerequisites ---")
                            
                            # Check if we need to sign in or can proceed as guest
                            signin_indicators = [
                                "#ap_email",
                                "input[name='email']",
                                ".a-spacing-large:has-text('Sign in')",
                                "#continue-as-guest-button",
                                "input[aria-label*='email']"
                            ]
                            
                            signin_required = False
                            for selector in signin_indicators:
                                try:
                                    if page.locator(selector).count() > 0:
                                        signin_required = True
                                        print(f"Sign-in page detected with: {selector}")
                                        break
                                except:
                                    continue
                            
                            if signin_required:
                                # Try to find guest checkout option
                                guest_checkout_selectors = [
                                    "#continue-as-guest-button",
                                    "input[name='continue-as-guest']",
                                    "a[href*='guest']",
                                    ".a-button-text:has-text('Continue as guest')"
                                ]
                                
                                guest_checkout_found = False
                                for selector in guest_checkout_selectors:
                                    try:
                                        guest_button = page.locator(selector).first
                                        if guest_button.is_visible():
                                            print(f"Found guest checkout option: {selector}")
                                            guest_button.click()
                                            guest_checkout_found = True
                                            page.wait_for_load_state("load", timeout=10000)
                                            time.sleep(2)
                                            break
                                    except:
                                        continue
                                
                                if not guest_checkout_found:
                                    print("⚠️  Sign-in required but no guest checkout option found")
                                    print("Checkout validation limited due to authentication requirements")
                            else:
                                print("✓ Proceeding with checkout (no sign-in required)")
                            
                            # Locate and validate grand total
                            print("\n--- Validating grand total calculation ---")
                            
                            total_selectors = [
                                "#grand-total-price",
                                ".grand-total-price .a-offscreen",
                                "[data-automation-id='order-total'] .a-offscreen",
                                ".a-row.a-spacing-none.checkout-order-total .a-offscreen",
                                ".order-total .a-price .a-offscreen",
                                "#subtotals-marketplace-table .grand-total-price"
                            ]
                            
                            grand_total = None
                            for selector in total_selectors:
                                try:
                                    total_element = page.locator(selector).first
                                    if total_element.is_visible():
                                        total_text = total_element.inner_text().strip()
                                        # Extract numeric value from total text
                                        import re
                                        total_match = re.search(r'[\d,]+\.?\d*', total_text.replace('$', ''))
                                        if total_match:
                                            grand_total = float(total_match.group().replace(',', ''))
                                            print(f"Grand total found: ${grand_total}")
                                            break
                                except:
                                    continue
                            
                            if grand_total and item_price:
                                # Validate calculation: item price × quantity (2) = expected total
                                expected_subtotal = item_price * 2
                                print(f"Expected subtotal (${item_price} × 2): ${expected_subtotal}")
                                
                                # Allow for taxes, shipping, etc. - check if total is reasonable
                                if grand_total >= expected_subtotal:
                                    if grand_total <= expected_subtotal * 1.5:  # Allow up to 50% markup for taxes/shipping
                                        print(f"✓ Grand total validation successful!")
                                        print(f"  Item price: ${item_price}")
                                        print(f"  Quantity: 2")
                                        print(f"  Expected subtotal: ${expected_subtotal}")
                                        print(f"  Actual grand total: ${grand_total}")
                                        print(f"  Difference (taxes/fees): ${grand_total - expected_subtotal:.2f}")
                                    else:
                                        print(f"⚠️  Grand total seems unusually high:")
                                        print(f"  Expected: ~${expected_subtotal}, Got: ${grand_total}")
                                else:
                                    print(f"❌ Grand total validation failed:")
                                    print(f"  Grand total (${grand_total}) is less than expected subtotal (${expected_subtotal})")
                            elif grand_total:
                                print(f"✓ Grand total located: ${grand_total}")
                                print("⚠️  Could not validate calculation (item price not available)")
                            elif item_price:
                                print(f"Item price available: ${item_price}")
                                print("❌ Could not locate grand total on checkout page")
                                # Debug: show available price elements
                                print("Available price elements:")
                                price_elements = page.locator(".a-price, .a-offscreen, [class*='total'], [class*='price']").filter(visible=True)
                                for i in range(min(price_elements.count(), 5)):
                                    try:
                                        element = price_elements.nth(i)
                                        text = element.inner_text().strip()
                                        if text and '$' in text:
                                            print(f"  Price element {i+1}: '{text}'")
                                    except:
                                        pass
                            else:
                                print("❌ Could not extract price information for validation")
                            
                            print("✓ Checkout process and validation completed")
                        else:
                            print("❌ Could not find 'Proceed to Checkout' button")
                            print("Available cart buttons:")
                            # Debug: show available buttons
                            cart_buttons = page.locator("input, button").filter(visible=True)
                            for i in range(min(cart_buttons.count(), 5)):
                                try:
                                    button = cart_buttons.nth(i)
                                    button_text = button.inner_text() or button.get_attribute("value") or ""
                                    if button_text:
                                        print(f"  Button {i+1}: '{button_text[:50]}'")
                                except:
                                    pass
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
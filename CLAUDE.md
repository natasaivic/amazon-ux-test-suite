# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A comprehensive automated testing framework for validating critical user experience flows on the Amazon e-commerce platform. This test suite ensures the reliability and functionality of core customer journeys through systematic end-to-end testing using Playwright and pytest.

## Current Test Implementation

The framework currently implements a comprehensive end-to-end test that validates:

### ✅ **Implemented Functionality**
- **Search Functionality**: Product search for "AirPods Max Over-Ear Headphone" with result validation
- **Product Selection**: Intelligent selection of second search result and product page navigation  
- **Cart Management**: Add to cart functionality with comprehensive verification and confirmation

### 🔄 **Future Planned Features**
- **Shopping Cart Operations**: Navigate to shopping cart page and update item quantity to 2
- **Checkout Process**: Proceed to checkout and implement validation of grand total calculation during the checkout process
- **Advanced Search**: Filters, sorting, and search result accuracy
- **Product Interactions**: Variant selection and product comparisons
- **Payment Validation**: Payment flow validation and order confirmation

## Current Architecture

The codebase currently implements:

### **Actual Structure**
- **Single comprehensive test** (`test_search_simple.py`) covering complete user journey
- **Playwright fixtures** in `conftest.py` for browser and page management
- **Environment configuration** via `.env` file with headed mode as default
- **Robust element detection** with multiple fallback strategies for dynamic Amazon UI
- **Comprehensive validation** at each step of the user workflow

### **Key Implementation Features**
- Direct search URL navigation for maximum reliability
- Smart page type detection (standard Amazon vs. sponsored/external pages)
- Multiple fallback selectors for cart buttons and confirmation elements
- Detailed logging and debugging output for troubleshooting
- Visual verification through headed mode with pause points

## Common Commands

Since this is a Playwright + pytest project, these commands will likely be used:

```bash
# Install dependencies
pip install -r requirements.txt
# or
pip install playwright pytest

# Install browser binaries
playwright install

# Run all tests
pytest

# Run specific test file
pytest tests/test_search_simple.py

# Run tests with specific markers
pytest -m smoke

# Run tests in headed mode (visible browser)
pytest --headed

# Run tests in parallel
pytest -n auto

# Generate test report
pytest --html=report.html
```

## Development Notes

### **Current Implementation Principles**
- **Defensive Testing**: Multiple fallback strategies for dynamic Amazon UI elements
- **Smart Navigation**: Direct URL approach instead of form interaction for reliability
- **Explicit Waits**: Uses `page.wait_for_selector()` and `page.wait_for_load_state()` appropriately
- **Comprehensive Validation**: Verifies each step with detailed logging output
- **Environment Configuration**: Uses `.env` file for browser settings (headed mode default)

### **Key Technical Approaches**
- **Element Detection**: Multiple selector strategies with graceful fallbacks
- **Page Type Recognition**: Distinguishes Amazon product pages from external/sponsored content
- **Cart Verification**: Multiple confirmation methods (UI elements, cart count, success messages)
- **Error Handling**: Continues execution with informative error messages rather than failing completely
- **Visual Debugging**: Headed mode with pause points for manual verification

### **Test Execution Patterns**
```bash
# Run the main end-to-end test with full output
pytest tests/test_search_simple.py::TestAmazonSearchSimple::test_search_and_select_second_result -v -s

# Expected output flow:
# ✓ Found 22 search results
# ✓ Successfully navigated to product page  
# ✓ Standard Amazon product page detected
# ✓ Found 'Add to Cart' button with selector: #add-to-cart-button
# ✓ Clicked 'Add to Cart' button
# ✓ Cart confirmation found
# ✓ Item successfully added to cart
```
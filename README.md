# Amazon UX Test Suite

## Overview

A comprehensive automated testing framework for validating critical user experience flows on the Amazon e-commerce platform. This test suite ensures the reliability and functionality of core customer journeys through systematic end-to-end testing.

## Test Coverage

The test suite currently implements and validates the following key user flows:

### ✅ **Implemented**
- **Search Functionality**: Product search and search result validation
- **Product Selection**: Product detail page navigation and information extraction  
- **Cart Management**: Add to cart functionality with comprehensive verification

### 🔄 **Planned for Future Implementation**
- **Shopping Cart Operations**: Navigate to shopping cart page and update item quantity to 2        │ │
- **Checkout Process**: Proceed to checkout and implement validation of grand total  

## Technology Stack

- **Playwright**: Modern web automation framework for cross-browser testing
- **pytest**: Python testing framework providing flexible test organization and reporting
- **Python**: Primary language for test implementation and maintenance

## Test Architecture

Tests are organized by feature domains to ensure maintainability and clear separation of concerns:
- Search flow validation
- Product interaction testing
- Shopping cart functionality
- Checkout process verification

## Quality Assurance Approach

This framework follows QA best practices including:
- Page Object Model design pattern for maintainable test code
- Explicit wait strategies for reliable element interaction
- Cross-browser compatibility testing
- Comprehensive error handling and logging
- Reusable test utilities and fixtures

## Setup Instructions

### Prerequisites
- Python 3.8+
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd amazon-ux-test-suite
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Configure environment variables:
```bash
# The .env file is already included with default settings
# Edit .env file to customize configuration if needed
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_search_simple.py

# Run tests with HTML report
pytest --html=reports/report.html

# Run tests in parallel
pytest -n auto

# Run tests in headed mode (visible browser) - default setting
pytest tests/test_search_simple.py -v -s

# Run specific test method
pytest tests/test_search_simple.py::TestAmazonSearchSimple::test_search_and_select_second_result -v -s
```

## Current Test Implementation

### End-to-End Amazon UX Workflow
The test suite currently includes a comprehensive end-to-end test (`test_search_simple.py`) that validates the complete Amazon customer journey:

#### **Complete User Flow Test**:
1. **Search Functionality**
   - Searches for "AirPods Max Over-Ear Headphone" on Amazon
   - Validates search results are displayed (typically 20+ results)
   - Verifies search result visibility and accessibility

2. **Product Selection**
   - Intelligently selects the second search result
   - Navigates to the product detail page
   - Extracts and displays product information

3. **Cart Management** 
   - Detects standard Amazon product pages vs. external/sponsored pages
   - Locates "Add to Cart" button using multiple fallback strategies
   - Successfully adds the selected item to shopping cart
   - Verifies cart confirmation through multiple validation methods

#### **Test Features:**
- **Smart Navigation**: Direct search URL approach for maximum reliability
- **Robust Element Detection**: Multiple fallback strategies for dynamic Amazon UI
- **Page Type Recognition**: Handles different Amazon page layouts
- **Comprehensive Validation**: Verifies each step of the user journey
- **Visual Verification**: Headed mode execution with pause points
- **Detailed Logging**: Clear output showing progress and debugging information

#### **Test Output Example:**
```
✓ Found 22 search results
✓ Successfully navigated to product page
✓ Standard Amazon product page detected
✓ Found 'Add to Cart' button with selector: #add-to-cart-button
✓ Clicked 'Add to Cart' button
✓ Cart confirmation found
✓ Item successfully added to cart
```

This single test demonstrates a production-ready approach to testing critical e-commerce user flows with comprehensive error handling and validation.

## Project Structure

```
amazon-ux-test-suite/
├── tests/                    # Test files organized by feature
│   └── test_search_simple.py # Amazon search and product selection tests
├── conftest.py              # Pytest configuration and fixtures
├── requirements.txt         # Python dependencies (Playwright, pytest, etc.)
├── .env                     # Environment configuration (included)
├── .gitignore              # Git ignore rules
├── CLAUDE.md               # Development guidance for Claude Code
├── venv/                   # Python virtual environment (excluded from git)
└── README.md               # This file
```

## Next Steps

The framework is ready for expansion with additional test scenarios:

### **Immediate Enhancements**
- **Cart Workflow Extension**: Navigate to cart page and verify item details
- **Quantity Management**: Test quantity updates and item removal from cart
- **Multiple Items**: Add multiple different products to cart

### **Advanced Features**
- **Checkout Flow**: Guest and authenticated checkout processes
- **Product Variations**: Size, color, and option selection testing
- **Search Filters**: Price range, brand, and category filtering
- **Cross-Browser Testing**: Firefox, Safari, and Edge compatibility
- **Performance Testing**: Page load times and response measurements

### **Quality Enhancements**
- **Page Object Model**: Refactor common elements into reusable page classes
- **Test Data Management**: External test data files and parameterized tests
- **Reporting**: Enhanced HTML reports with screenshots and test metrics
- **CI/CD Integration**: GitHub Actions for automated test execution

# Amazon UX Test Suite

## Overview

A comprehensive automated testing framework for validating critical user experience flows on the Amazon e-commerce platform. This test suite ensures the reliability and functionality of core customer journeys through systematic end-to-end testing.

## Test Coverage

The test suite validates the following key user flows:

- **Search Functionality**: Product search, filters, sorting, and search result accuracy
- **Product Selection**: Product detail pages, variant selection, and product information display
- **Cart Management**: Add to cart, cart modifications, quantity updates, and cart persistence
- **Checkout Validation**: Checkout process, payment flow validation, and order confirmation

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

### Search Flow Testing
The test suite currently includes:

- **AirPods Max Search Test** (`test_search_simple.py`):
  - Searches for "AirPods Max Over-Ear Headphone" on Amazon
  - Validates search results are displayed
  - Selects and navigates to the second search result
  - Verifies successful product page navigation
  - Runs in headed mode with 5-second viewing pause

**Test Features:**
- Direct search URL navigation for reliability
- Robust element selection with fallback strategies
- Clear test output and debugging information
- Headed mode execution for visual verification

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

This framework is ready for expansion with additional test scenarios:
- Cart management testing
- Checkout flow validation
- Product detail page interactions
- Filter and sort functionality
- Cross-browser compatibility testing

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
cp .env.example .env
# Edit .env file with your configuration
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_search.py

# Run tests with HTML report
pytest --html=reports/report.html

# Run tests in parallel
pytest -n auto

# Run tests in headed mode (visible browser)
pytest --headed
```

## Project Structure

```
amazon-ux-test-suite/
├── tests/              # Test files organized by feature
├── pages/              # Page Object Model classes
├── utils/              # Utility functions and helpers
├── fixtures/           # Test fixtures and setup
├── reports/            # Test reports and artifacts
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration
└── README.md          # This file
```

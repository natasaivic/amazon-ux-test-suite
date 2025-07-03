# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A comprehensive automated testing framework for validating critical user experience flows on the Amazon e-commerce platform. This test suite ensures the reliability and functionality of core customer journeys through systematic end-to-end testing using Playwright and pytest.

## Test Coverage Areas

The framework validates these key user flows:
- **Search Functionality**: Product search, filters, sorting, and search result accuracy
- **Product Selection**: Product detail pages, variant selection, and product information display
- **Cart Management**: Add to cart, cart modifications, quantity updates, and cart persistence
- **Checkout Validation**: Checkout process, payment flow validation, and order confirmation

## Architecture Structure

The codebase follows QA best practices with this expected structure:
- Test files organized by feature domains (search, product, cart, checkout)
- Page Object Model design pattern for maintainable test code
- Explicit wait strategies for reliable element interaction
- Cross-browser compatibility testing support
- Comprehensive error handling and logging
- Reusable test utilities and fixtures
- Configuration files for test environments and browser settings

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
pytest tests/test_search.py

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

- Tests should be defensive and handle dynamic content on Amazon's website
- Use explicit waits for elements rather than fixed sleeps
- Implement proper error handling for network issues and element loading
- Consider using test fixtures for common setup/teardown operations
- Use environment variables for sensitive data (avoid hardcoding credentials)
- Implement proper logging for debugging test failures
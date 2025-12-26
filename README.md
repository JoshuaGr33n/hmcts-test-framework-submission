# Test Automation Framework - HMCTS Coding Challenge

A robust, maintainable test automation framework for login functionality testing, built with Python, Pytest, and Selenium WebDriver.

## 🚀 Features

- **Page Object Model (POM)** design pattern for maintainability
- **Comprehensive logging** with timestamped log files
- **Detailed HTML reporting** with pytest-html
- **Allure reporting** support for rich test reports
- **Configuration management** via config.ini
- **Screenshot capture** on test failure
- **Data-driven testing** with pytest parametrization
- **Secure credential handling** via environment variables
- **Cross-browser support** (Chrome, Firefox)
- **Headless execution** capability

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome or Firefox browser

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JoshuaGr33n/hmcts-test-framework-submission.git
   cd hmcts-test-framework-submission
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Edit `config.ini`** to modify:
   - Application URL
   - Browser settings (chrome/firefox, headless mode)
   - Wait timeouts
   - Test data

2. **Set environment variables** for sensitive data (optional):
   ```bash
   export SAUCE_USERNAME="standard_user"
   export SAUCE_PASSWORD="secret_sauce"
   ```

## 🧪 Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test markers
pytest -m smoke
pytest -m negative
pytest -m positive
```

### With HTML Reporting
```bash
# Generate HTML report
pytest --html=reports/test_report.html --self-contained-html

# Open the report (on macOS)
open reports/test_report.html
```

### With Allure Reporting
```bash
# Generate Allure results
pytest --alluredir=./allure-results

# Generate and open Allure report
allure generate ./allure-results -o ./allure-report --clean
allure open ./allure-report
```

### Parallel Execution
```bash
# Run tests in parallel (2 workers)
pytest -n 2
```

## 📁 Project Structure

```
hmcts-test-framework-submission/
├── pages/                    # Page Object Model classes
│   ├── base_page.py         # Base page with common methods
│   └── login_page.py        # Login page specific methods
├── tests/                   # Test suites
│   ├── conftest.py         # Pytest fixtures
│   └── test_login.py       # Login test cases
├── utilities/              # Helper utilities
│   └── config_reader.py   # Configuration management
├── logs/                   # Execution logs (auto-generated)
├── reports/                # Test reports (auto-generated)
├── screenshots/            # Failure screenshots (auto-generated)
├── config.ini             # Configuration file
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🧩 Test Cases Covered

### Positive Tests
- ✅ TC001: Successful login with valid credentials

### Negative Tests
- ✅ TC002: Login with invalid username
- ✅ TC003: Login with invalid password
- ✅ TC004: Login with locked out user
- ✅ TC005: Login with empty credentials
- ✅ TC006: Verify login page elements

## 🏗️ Design Choices

### **1. Technology Stack Selection**
- **Python with Pytest**: Chosen for its simplicity, extensive plugin ecosystem, and superior test discovery compared to unittest. Pytest's fixture system enables clean setup/teardown patterns.
- **Selenium WebDriver**: Industry standard for web automation with robust cross-browser support.
- **Page Object Model (POM)**: Implemented to separate test logic from UI locators, enhancing maintainability and reducing code duplication.

### **2. Architecture Decisions**
- **Modular Design**: Clear separation between pages, tests, utilities, and configuration.
- **Configuration-Driven**: All environment-specific settings in `config.ini`, allowing easy switching between environments without code changes.
- **Fixture-Based Setup**: Pytest fixtures in `conftest.py` provide reusable WebDriver instances and page objects with proper cleanup.

### **3. Reliability Enhancements**
- **Explicit Waits**: Implemented custom wait methods in `BasePage` to handle dynamic content, avoiding flaky tests from hard-coded sleeps.
- **Comprehensive Error Handling**: Try-catch blocks with detailed logging for all critical operations.
- **Automatic Screenshots**: Hook integrated to capture screenshots on test failures for easier debugging.

### **4. Maintainability Features**
- **Centralized Locators**: All element locators defined as constants in page classes.
- **Reusable Base Methods**: Common interactions (click, type, wait) abstracted in `BasePage`.
- **Parameterized Tests**: Using `@pytest.mark.parametrize` for data-driven testing without code duplication.

### **5. Professional DevOps Integration**
- **Logging Framework**: Structured logging with timestamped files and console output for audit trails.
- **Multiple Reporting Options**: HTML reports for quick viewing and Allure for detailed analytics.
- **Environment Variable Support**: Sensitive credentials handled securely via environment variables.

## 🔮 Additional Improvements with More Time

Given additional development time, I would implement the following enhancements:

### **1. Dockerization & CI/CD Integration**
```python
# Dockerfile for consistent test execution
FROM python:3.10-slim
# Add Chrome/Firefox browsers
# Configure headless execution
# Integrate with GitHub Actions for automated testing on PRs
```

### **2. Advanced Reporting & Analytics**
- **Dashboard Integration**: Push results to tools like ElasticSearch/Kibana for trend analysis
- **Slack/Teams Notifications**: Automatic alerts for test failures
- **Historical Comparison**: Track test execution times and failure rates over time

### **3. Enhanced Test Coverage**
- **API Testing Layer**: Add tests for login API endpoints alongside UI tests
- **Visual Regression Testing**: Integrate with Percy or Applitools for UI consistency checks
- **Accessibility Testing**: Incorporate axe-core for automated accessibility compliance

### **4. Performance & Scalability**
- **Parallel Execution Optimization**: Better test distribution across workers
- **Cloud Testing Integration**: Support for BrowserStack, SauceLabs, or AWS Device Farm
- **Test Data Management**: Factory pattern for generating test data dynamically

### **5. Security & Compliance**
- **Security Scanning**: Integrate ZAP or similar for security testing
- **Compliance Reporting**: Generate audit reports for regulatory requirements
- **Secret Management**: Integration with HashiCorp Vault or AWS Secrets Manager

### **6. Developer Experience**
- **Custom CLI Tool**: Command-line interface for common test operations
- **Test Generation**: Scaffolding tools for quickly adding new test cases
- **Debug Mode**: Enhanced debugging with video recording and network traffic capture

### **7. Monitoring & Alerting**
- **Real-time Monitoring**: Live dashboard showing test execution status
- **Performance Baselines**: Establish and monitor performance thresholds
- **Predictive Analysis**: Machine learning to predict flaky tests before they fail

## 📊 Metrics and Reporting

The framework generates:
- **HTML Reports**: `reports/test_report.html`
- **Allure Reports**: `allure-report/` (if Allure is installed)
- **Log Files**: `logs/test_execution_*.log`
- **Screenshots**: `screenshots/` (on test failure)

## 🐛 Troubleshooting

### Common Issues

1. **WebDriver issues**
   ```bash
   # Ensure webdriver-manager can install drivers
   pip install --upgrade webdriver-manager
   ```

2. **Browser not launching**
   - Check browser version compatibility
   - Try running without headless mode first

3. **Import errors**
   ```bash
   # Ensure you're in the project root directory
   # and virtual environment is activated
   ```

### Getting Help
Check the log files in `logs/` directory for detailed error information.

## 📝 Notes

- The framework uses SauceDemo website (`https://www.saucedemo.com/`) for testing
- Credentials are read from environment variables or use defaults
- All sensitive data should be stored in environment variables, not in code
- The framework follows PEP 8 coding standards

## 📄 License

This project is created for HMCTS coding challenge assessment.
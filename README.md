# OpenCart E2E Test Automation Framework

A professional, production-ready end-to-end test automation framework for the OpenCart demo e-commerce site using Python, Selenium WebDriver, and pytest.

## 🚀 Features

- **Page Object Model (POM)** architecture for maintainable test code
- **Data-driven testing** with JSON test data files
- **Cross-browser support** (Chrome, Firefox)
- **Headless mode** for CI/CD pipelines
- **Detailed HTML reports** with pytest-html
- **Screenshot capture** on test failures
- **GitHub Actions CI** pipeline integration
- **Custom pytest markers** for test categorization

## 📁 Project Structure

```
opencart-automation/
├── .github/workflows/      # CI/CD pipeline
├── config/                 # Configuration settings
├── pages/                  # Page Object classes
├── tests/                  # Test cases
├── test_data/              # Test data files
├── utilities/              # Helper functions
├── reports/                # Test reports (generated)
├── screenshots/            # Failure screenshots (generated)
└── requirements.txt        # Dependencies
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/opencart-automation.git
cd opencart-automation
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🧪 Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run smoke tests only:
```bash
pytest tests/ -m smoke -v
```

### Run regression tests:
```bash
pytest tests/ -m regression -v
```

### Run specific test file:
```bash
pytest tests/test_login.py -v
```

### Run in headless mode:
```bash
pytest tests/ --headless
```

### Run with HTML report:
```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

### Run on Firefox:
```bash
pytest tests/ --browser firefox
```

## 📊 Test Categories

| Marker | Description |
|--------|-------------|
| `smoke` | Quick tests for basic functionality |
| `regression` | Full regression test suite |
| `login` | Login-related tests |
| `registration` | Registration-related tests |
| `search` | Product search tests |
| `cart` | Shopping cart tests |

## 🔧 Configuration

Edit `config/config.py` to modify:
- Base URL
- Browser settings
- Timeout values
- Directory paths

## 📝 Test Data

Test data is stored in JSON files under `test_data/`:
- `users.json` - User credentials
- `products.json` - Product search terms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

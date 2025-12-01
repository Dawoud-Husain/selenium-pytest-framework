# BlazeDemo E2E Test Automation Framework

A professional, production-ready end-to-end test automation framework for the BlazeDemo flight booking site using Python, Selenium WebDriver, and pytest.

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
selenium-pytest-framework/
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
git clone https://github.com/Dawoud-Husain/selenium-pytest-framework.git
cd selenium-pytest-framework
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
pytest tests/test_flight_booking.py -v
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
| `flights` | Flight selection tests |
| `purchase` | Purchase/checkout tests |
| `booking` | Complete booking flow tests |

## 🔧 Configuration

Edit `config/config.py` to modify:
- Base URL
- Browser settings
- Timeout values
- Directory paths

## 📝 Test Data

Test data is stored in JSON files under `test_data/`:
- `bookings.json` - Passenger details, payment info, and flight routes

## 🧩 Page Objects

The framework includes page objects for:
- `HomePage` - Select departure/destination cities and search flights
- `FlightsPage` - View and select available flights
- `PurchasePage` - Fill passenger and payment details
- `ConfirmationPage` - View booking confirmation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

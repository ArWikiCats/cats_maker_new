# Cats Maker - Arabic Wikipedia Category Creator

A Python automation tool for creating Arabic Wikipedia categories from their English counterparts. This bot processes English Wikipedia categories and creates equivalent Arabic categories with proper translations, templates, portals, and Wikidata integration.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [Related Documentation](#related-documentation)

## Overview

Cats Maker New is a sophisticated Wikipedia bot designed to automate the creation of Arabic Wikipedia categories based on their English counterparts. The tool:

1. Takes a list of English Wikipedia category names
2. Resolves Arabic translations using Wikidata and ArWikiCats
3. Creates the Arabic category pages with proper structure
4. Adds appropriate templates and portal links
5. Links the new categories to Wikidata
6. Adds the new categories to relevant pages

This project is particularly useful for expanding the Arabic Wikipedia's category structure to match the more comprehensive English Wikipedia.

## Features

### Core Functionality
- **Category Translation**: Automatically resolves Arabic category labels from English categories using Wikidata sitelinks and the ArWikiCats library
- **Category Creation**: Creates new Arabic Wikipedia category pages with proper formatting
- **Template Generation**: Generates navigation templates for categories (centuries, decades, years, millennia)
- **Portal Integration**: Automatically adds relevant portal links to categories based on topic detection
- **Wikidata Integration**: Creates and updates Wikidata sitelinks for newly created categories

### Data Sources
- **Wikidata API**: Retrieves sitelinks, labels, descriptions, and properties
- **Wikipedia API**: Queries page information, categories, and langlinks
- **SQL Database**: Supports Wikimedia Tool Labs SQL databases for efficient queries
- **Quarry Integration**: Fetches category lists from Quarry queries

### Processing Features
- **Batch Processing**: Processes multiple categories in a single run
- **Recursive Processing**: Discovers and processes subcategories
- **Duplicate Detection**: Tracks processed categories to avoid duplicates
- **Error Handling**: Robust error handling with logging
- **Caching**: In-memory caching for API responses

## Architecture

The project follows a layered architecture:

```
┌─────────────────────────────────────────┐
│         Entry Point Layer               │
│         run.py                          │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      Business Logic Layer               │
│      mk_cats/mknew.py                   │
│      - create_categories_from_list()    │
│      - one_cat(), process_catagories()  │
│      - make_ar(), ar_make_lab()         │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      Page Creation Layer                │
│      mk_cats/create_category_page.py    │
│      mk_cats/categorytext.py            │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      Data Processing Layer              │
│      b18_new/, c18_new/                 │
│      - Category processing              │
│      - Link resolution                  │
│      - Member list management           │
└─────────────┬───────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      External Services Layer            │
│      - wiki_api/ (MediaWiki API)        │
│      - wd_bots/ (Wikidata API)          │
│      - api_sql/ (Database)              │
└─────────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────┐
│      Utilities Layer                    │
│      helps/, utils/, temp/              │
└─────────────────────────────────────────┘
```

### Data Flow

```
English Category Name
    ↓
[ar_make_lab] → Arabic Label (from Wikidata/ArWikiCats)
    ↓
[get_ar_list_from_en] → List of Arabic article titles
    ↓
[find_LCN, Get_Sitelinks] → Language links, Qid
    ↓
[find_Page_Cat_without_hidden] → Parent categories (English)
    ↓
[get_listenpageTitle] → Member pages
    ↓
[generate_category_text] → Category page text (with templates)
    ↓
[page.save] → Save to ar.wikipedia
    ↓
[Log_to_wikidata] → Update Wikidata sitelink
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Access to Wikipedia API (for actual operations)
- (Optional) Access to Wikimedia Tool Labs for SQL queries

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MrIbrahem/cats_maker_new.git
   cd cats_maker_new
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.in
   ```

3. **Install optional dependencies (for full functionality):**
   ```bash
   # For Arabic category label resolution
   pip install ArWikiCats
   ```

4. **Configure pywikibot (if not already configured):**
   ```bash
   python -m pywikibot -lang:ar -family:wikipedia
   ```

### Dependencies

- `wikitextparser>=0.55.7` - Wiki text parsing
- `tqdm>=4.67.1` - Progress bars
- `SPARQLWrapper>=2.0.0` - SPARQL queries
- `pymysql` - MySQL database connections
- `jsonlines` - JSONL file handling
- `sqlite_utils` - SQLite utilities
- `pywikibot` - MediaWiki API interaction
- `pytest` - Testing framework
- `pytest-mock` - Test mocking

## Usage

### Basic Usage

```bash
# Process a single category
python run.py -encat:Science

# Process categories from a Quarry query
python run.py -quarry:357357

# Process with debug logging
python run.py DEBUG -encat:Mathematics
```

### Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `encat:<name>` | Process a single English category | `encat:Science` |
| `quarry:<id>` | Fetch categories from Quarry query | `quarry:357357` |
| `-depth:<n>` | Set recursion depth (default: 5) | `-depth:3` |
| `-range:<n>` | Set range limit for processing | `-range:10` |
| `-We_Try` | Enable retry mode | `-We_Try` |
| `-nowetry` | Disable retry mode | `-nowetry` |
| `DEBUG` | Enable debug logging | `DEBUG` |

### Programmatic Usage

```python
from src.mk_cats import create_categories_from_list

# Process a list of categories
categories = [
    "Category:Science",
    "Category:Mathematics",
    "Category:Physics"
]

# Optional callback for processing results
def my_callback(title, **kwargs):
    print(f"Processed: {title}")

create_categories_from_list(categories, callback=my_callback)
```

### Individual Functions

```python
from src.mk_cats import ar_make_lab, process_catagories

# Get Arabic label for an English category
ar_label = ar_make_lab("Category:Science")
print(f"Arabic label: {ar_label}")

# Process a single category with its subcategories
process_catagories("Category:Science", ar_label, num=1, lenth=1)
```

## Configuration

### Environment Variables

The project supports configuration through several mechanisms:

| Variable | Description | Default |
|----------|-------------|---------|
| Log level | Set via command line with `DEBUG` | `INFO` |

### Runtime Configuration

Configuration is managed through `sys.argv` arguments and internal dictionaries:

```python
# In mk_cats/mknew.py
Range = {1: 5}      # Recursion range limit
We_Try = {1: True}  # Retry on failure

# In c18_new/bots/cat_tools_argv.py
use_sqldb = {1: True}  # Use SQL database
```

### Blacklists

The project maintains several blacklists to skip certain categories:

- **English category blacklist**: Categories to skip entirely
- **Template blacklist**: Templates to exclude from processing
- **Name blacklist**: Specific names to avoid

## Project Structure

```
cats_maker_new/
├── run.py                    # Main entry point
├── requirements.in           # Python dependencies
├── pyproject.toml           # Project configuration (Black, isort, ruff)
├── pytest.ini               # Pytest configuration
├── refactoring_plan.md      # Technical refactoring documentation
├── testing_plan.md          # Testing strategy documentation
│
├── src/                     # Source code
│   ├── mk_cats/            # Main category creation logic
│   │   ├── mknew.py        # Core functions (create_categories_from_list)
│   │   ├── categorytext.py # Text generation for category pages
│   │   ├── create_category_page.py  # Page creation logic
│   │   └── utils/          # Utility functions
│   │
│   ├── b18_new/            # Category processing and links
│   │   ├── LCN_new.py      # Language link discovery
│   │   ├── cat_tools.py    # Category utilities
│   │   ├── sql_cat.py      # SQL-based category queries
│   │   └── add_bot.py      # Add categories to pages
│   │
│   ├── c18_new/            # Additional category tools
│   │   ├── bots/           # Bot utilities
│   │   ├── cats_tools/     # Category conversion tools
│   │   └── tools_bots/     # Helper bots
│   │
│   ├── wd_bots/            # Wikidata integration
│   │   ├── wd_api_bot.py   # Wikidata API functions
│   │   ├── to_wd.py        # Log to Wikidata
│   │   └── get_bots.py     # Data retrieval
│   │
│   ├── wiki_api/           # Wikipedia API calls
│   │   ├── himoBOT2.py     # General Wikipedia functions
│   │   └── wd_sparql.py    # SPARQL queries
│   │
│   ├── api_sql/            # Database operations
│   │   ├── wiki_sql.py     # Wiki SQL queries
│   │   └── sql_qu.py       # Query utilities
│   │
│   ├── helps/              # Helper utilities
│   │   ├── log.py          # Logging wrapper
│   │   └── printe_helper.py # Print formatting
│   │
│   ├── temp/               # Template generation
│   │   └── *_temp.py       # Century, decade, year templates
│   │
│   └── utils/              # General utilities
│       └── skip_cats.py    # Category blacklists
│
├── tests/                  # Test suite
│   ├── conftest.py        # Shared test fixtures
│   ├── mk_cats/           # mk_cats tests
│   ├── b18_new/           # b18_new tests
│   ├── wd_bots/           # wd_bots tests
│   ├── wiki_api/          # wiki_api tests
│   └── ...
│
└── .github/
    └── workflows/
        └── pytest.yaml    # CI/CD configuration
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/mk_cats/test_mknew.py

# Run with coverage report
pytest --cov=src --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

### Test Structure

The test suite covers:

- **Unit Tests**: Individual function testing with mocked dependencies
- **Integration Tests**: End-to-end workflow testing
- **Fixture Tests**: Reusable test data and mock configurations

### Test Coverage

Current test coverage includes **1563 tests** covering:

| Module | Tests | Status |
|--------|-------|--------|
| api_sql | 28 | ✅ |
| b18_new | 28 | ✅ |
| c18_new | 18 | ✅ |
| helps | 58 | ✅ |
| mk_cats | 31 | ✅ |
| utils | 14 | ✅ |
| wd_bots | 29 | ✅ |
| wiki_api | 32 | ✅ |
| temp | 1326 | ✅ |

### Writing Tests

Tests follow pytest conventions with comprehensive fixtures:

```python
import pytest
from src.mk_cats.mknew import ar_make_lab

class TestArMakeLab:
    """Tests for ar_make_lab function"""

    def test_returns_label_for_valid_category(self, mocker):
        """Test that valid categories return Arabic labels"""
        mocker.patch('src.mk_cats.mknew.filter_en.filter_cat', return_value=True)
        mocker.patch('src.mk_cats.mknew.resolve_arabic_category_label',
                     return_value='علوم')

        result = ar_make_lab("Category:Science")
        assert result == "علوم"
```

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Install development dependencies: `pip install -r requirements.in`
4. Make your changes
5. Run tests: `pytest`
6. Run linters: `ruff check src/`
7. Submit a pull request

### Code Style

This project uses:
- **Black** for code formatting (line length: 120)
- **isort** for import sorting
- **ruff** for linting

```bash
# Format code
black src/

# Sort imports
isort src/

# Lint code
ruff check src/
```

### Commit Guidelines

- Write clear, descriptive commit messages
- Reference issues when applicable
- Keep commits focused and atomic

## Related Documentation

- **[refactoring_plan.md](refactoring_plan.md)**: Detailed technical documentation about the codebase architecture, execution flow, and planned improvements
- **[testing_plan.md](testing_plan.md)**: Comprehensive testing strategy, test coverage goals, and test examples
- **[Wikidata API](https://www.wikidata.org/wiki/Wikidata:Data_access)**: Wikidata data access documentation
- **[MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page)**: Wikipedia API reference

## License

This project is open source. See repository for license details.

## Acknowledgments

- Arabic Wikipedia community
- Wikidata project
- Pywikibot developers
- ArWikiCats project

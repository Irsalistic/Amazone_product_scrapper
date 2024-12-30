# Amazon Product Scraper

A Python-based web scraper that extracts product information from Amazon search results using Selenium. The script can concurrently scrape multiple product categories and save the results in JSON format.

## Features

- Concurrent scraping of multiple product categories
- Automatic pagination through search results (up to 20 pages per query)
- Random User-Agent rotation to help avoid detection
- Headless browser operation
- Detailed product information extraction including:
  - Product title
  - Rating
  - Total reviews
  - Purchase details
  - Price
  - Product image URL
  - Timestamp information

## Prerequisites

- Python 3.10+
- Chrome browser installed
- Required Python packages (see Requirements section)

## Requirements

```
selenium
webdriver_manager
```

## Installation
2. Install the required packages:
   ```bash
   pip requirements.txt
   ```

## Usage

1. The script comes with predefined search queries for common electronics categories:
   - Headphones
   - Smartphones
   - Laptops
   - Tablets
   - Cameras
   - Earbuds
   - Smartwatches
   - Chargers
   - Speakers
   - Monitors

2. To run the scraper:
   ```bash
   python amazone_scraper.py
   ```

3. The script will create separate JSON files for each search query, named `<search_query>.json`

## Configuration

You can modify the following variables in the script:

- `BASE_URL`: The base Amazon search URL
- `search_queries`: List of product categories to scrape
- `USER_AGENTS`: List of User-Agent strings for rotation

## Output Format

The scraper saves data in JSON format with the following structure:

```json
{
    "title": "Product Title",
    "rating": "4.5",
    "total_reviews": "1,234",
    "purchase_details": "Prime delivery details",
    "price": "$99.99",
    "image_url": "https://...",
    "creation_timestamp": "2024-12-24T10:00:00",
    "update_timestamp": "2024-12-24T10:00:00",
    "scrape_date": "2024-12-24"
}
```


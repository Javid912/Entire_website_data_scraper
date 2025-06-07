# Entire Website Data Scraper & Dashboard

A production-ready, Dockerized web scraping and dashboard solution for any website using Scrapy, Playwright, and Flask. Easily run and manage scrapes, view results, and download data in JSON or CSV format.

## Features
- Scrape the entire website or a single page
- Extracts main text content, emails, and links
- Download results as JSON or CSV
- Lightweight, Dockerized, and easy to deploy

## Quick Start (Docker)

1. **Build the images:**
   ```bash
   docker-compose build
   ```
2. **Run the Flask dashboard:**
   ```bash
   docker-compose up web
   ```
   Visit [http://localhost:5000](http://localhost:5000)

## Development Setup (without Docker)

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install
   ```
2. Run the Flask app:
   ```bash
   python flask_app/app.py
   ```
3. Run the Scrapy spider:
   ```bash
   cd scrapy_project
   scrapy crawl main_spider -a start_url=https://example.com/
   ```

## Environment Variables
Copy `.env.example` to `.env` and adjust as needed.

## Project Structure
- `flask_app/` - Flask dashboard
- `scrapy_project/` - Scrapy spiders and pipelines
- `data/scraped_data/` - Output data (ignored by git)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
MIT 
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///../data/scraped_data/scraper.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCRAPY_SETTINGS_MODULE = 'scrapy_project.settings'
    SCRAPY_EXPORT_PATH = os.getenv('SCRAPY_EXPORT_PATH', '../data/scraped_data/')
    # Add more config as needed 
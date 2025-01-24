# Automotive Market Price Analytics

A comprehensive web application for analyzing and visualizing automotive market prices across different brands and models. This project combines web scraping capabilities with interactive data visualization to provide insights into car pricing trends.

## Project Overview

This application consists of three main components:

1. **Data Collection (scraper_module.py)**
   - Scrapes car model and price data from cars.com
   - Uses Oxylabs proxy for reliable data collection
   - Supports multiple car brands and models
   - Saves raw data in JSON format

2. **Data Processing (main_script.py)**
   - Processes the scraped data from individual JSON files
   - Combines data from all brands into a single comprehensive dataset
   - Handles data cleaning and formatting
   - Generates a consolidated complete.json file

3. **Interactive Dashboard (car_prices_app.py)**
   - Built with Streamlit for an interactive user interface
   - Features multiple visualization types:
     * Price distribution boxplots
     * Average price comparisons
     * Brand-wise price analysis
     * Detailed model information
   - Includes interactive filters for:
     * Brand selection
     * Year range
     * Price range

## Features

- **Multi-brand Analysis**: Compare prices across different automotive brands
- **Interactive Filtering**: Filter data by brand, year, and price range
- **Visual Analytics**: Multiple visualization types for price analysis
- **Detailed Statistics**: View comprehensive price statistics for each brand
- **Responsive Design**: Wide layout for better visualization

## Installation

1. Clone the repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in a .env file:
   - USERNAME (Oxylabs username)
   - PASSWORD (Oxylabs password)

## Usage

1. **Data Collection**:
   ```bash
   python scraper_module.py
   ```

2. **Data Processing**:
   ```bash
   python main_script.py
   ```

3. **Launch Dashboard**:
   ```bash
   streamlit run car_prices_app.py
   ```

## Data Structure

The application uses a hierarchical data structure:
- Individual brand data stored in JSON files
- Consolidated data in complete.json
- Processed data includes:
  * Brand information
  * Model details
  * Year of manufacture
  * Price information

## Technologies Used

- Python
- Streamlit
- Plotly
- BeautifulSoup4
- Pandas
- Requests
- dotenv

## Features

- Real-time data filtering
- Interactive visualizations
- Comprehensive price analytics
- User-friendly interface
- Responsive design

## Note

This project requires valid Oxylabs credentials for data collection. Ensure you have the necessary credentials in your .env file before running the scraper.
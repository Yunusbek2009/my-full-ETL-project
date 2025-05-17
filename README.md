Untitled4.ipynb — Web Scraping, Data Cleaning, and Visualization
Overview
This notebook performs the Extract, Transform, Load (ETL) process on university data scraped from a web page:

Extract:
Uses requests and BeautifulSoup to scrape university names and their descriptions from HTML content, applying precise selectors (span[itemprop='name'] and span[itemprop='description']) to filter relevant information.

Transform:
Cleans and structures the raw HTML data into a well-defined Python dictionary format.
Converts the cleaned data into CSV format, writing it safely to disk for persistence and reproducibility.
Applies basic data cleaning and manipulation to ensure data quality.

Load and Visualize:
Loads the cleaned dataset for analysis.
Generates insightful visualizations using matplotlib and seaborn to explore distributions and relationships in the dataset, providing clear, interpretable graphics to support decision-making.

Key Features
Robust web scraping with error handling potential (expandable).

Transformation from messy HTML to structured CSV format.

Modular code facilitating repeatable ETL workflows.

Data visualization that makes use of Python’s most popular plotting libraries for clear, publication-quality charts.

Dependencies
requests — For HTTP requests.

beautifulsoup4 — For HTML parsing and data extraction.

re — Regular expressions for optional text processing.

csv — CSV file creation and manipulation.

matplotlib and seaborn — For data visualization.

How to Run
Ensure you have all dependencies installed:

bash
Copy
Edit
pip install requests beautifulsoup4 matplotlib seaborn
Run the notebook cells sequentially:

Scrape and extract data from the webpage.

Save the cleaned data to CSV.

Load and visualize the data using plots.

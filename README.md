# CRAWL DATA

This is a Python script for scraping data from Netflix show pages and storing it in a MongoDB database.

## Getting Started

### Prerequisites

Before running this script, you'll need to install the following packages:

- `requests`
- `beautifulsoup4`
- `pymongo`
- `bson`

You can install them via pip:

```
pip install requests beautifulsoup4 pymongo bson
```

### Usage

To use this script, simply run it using Python 3:

```
python crawlData.py
```

The script will scrape data from the Netflix show page at https://www.netflix.com/browse?jbv=81665914 (you can modify this URL to scrape a different show), and store the data in a MongoDB database.

## Acknowledgements

This script was created by [hgthaii].

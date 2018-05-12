# Sheriff

This project aims to parse sheriff sale PDFs and map them.

## Setup Instructions

1. Run `pip install -r requirements.txt`
2. Add the bid/postponed PDFs to the project root. The files must be called `bid.pdf` and `postponed.pdf`

## Running

1. `python run.py`
2. Step 1 will create a file called `addresses.tsv`. Upload this file to Google Fusion Tables for viewing the map.
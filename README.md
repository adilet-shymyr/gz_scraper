# Data Scraper and Processor from goszakup.gov.kz

This project automates scraping procurement data from [goszakup.gov.kz](https://v3bl.goszakup.gov.kz/ru/rep/rep/m001) for a list of Business Identification Numbers (BINs). The script retrieves procurement data, processes it, saves it to Excel files, and combines all the files into a consolidated output.

## Features

- Automates data scraping from the website for multiple BINs and a specified year.
- Filters and processes the scraped data to keep relevant columns.
- Saves individual Excel files for each BIN with the format `BIN_year.xlsx`.
- Combines all individual Excel files into one aggregated Excel file.

## Requirements

To run this project, you need the following:

- **Python 3.11**
- **Google Chrome**
- **ChromeDriver** (automatically managed by `webdriver_manager`)
- The following Python libraries:
  - `selenium`
  - `pandas`
  - `openpyxl`
  - `webdriver_manager`


## Setup
- **Clone the Repository**
```bash
Copy code
git clone https://github.com/adilet-shymyr/gz-scraper.git
cd goszakup-scraper
```

- **Creating the Virtual Environment**
- **Navigate to your project directory and run the following command:**
```bash 
python -m venv venv
```

- Activating the Virtual Environment
After creating the venv, you need to activate it:

- For Windows (Command Prompt):

```bash
venv\Scripts\activate
````
Install the dependencies using the following command:

```bash
pip install -r requirements.txt
```
- **Modify the Configuration**


Update the year variable in the script to the desired year.
Update the bins list in the script to include the BINs you want to scrape.
Set the `data_folder` path to appropriate directories on your system.

## Running the Script
Run the Python script to scrape data for the specified BINs and year:
```bash
python main.py
```
- *The script performs the following steps:*

- Navigates to the specified webpage.

- Inputs each BIN and year, scrapes the data, and processes it.

- Saves the filtered data into separate Excel files, named `BIN_year.xlsx`.

- Combines all the individual files into a single file named `combined_final_file.xlsx`.

## Output Files:
- Individual BIN Excel files will be saved in the `data` directory.
- The final combined Excel file will be saved as `combined_final_file.xlsx` in the root directory.

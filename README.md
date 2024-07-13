# Web Scraping Project: Apartment Rentals in Barcelona

## Overview
This project focuses on extracting valuable information from the Engel & Völkers website about apartments for rent in Barcelona. The goal is to gather and analyze data related to rental properties, presenting the findings in a structured and comprehensible manner using dataframes.

## Objectives
1. Retrieve the list of all available apartments for rent in Barcelona from Engel & Völkers in a dataframe with the following attributes:
    - Title
    - Location
    - Bedrooms
    - Bathrooms
    - Living Area
    - Price
2. Calculate the average living area.
3. Calculate the average price.
4. Calculate the average price per square meter.
5. Calculate the average number of bedrooms.
6. Calculate the average number of bathrooms.
7. Count the number of available offers for rent in Barcelona.
8. Identify the largest living area of an apartment for rent in Barcelona.
9. Identify the highest price of an apartment for rent in Barcelona.
10. Identify the most common location of apartments for rent in Barcelona and the number of offers in that location.
11. Create a dataframe with the calculated results.
12. Calculate the price per sqm for each neighborhood in Barcelona and display the results in a dataframe.

## Requirements
The following Python libraries are required to run the code:
- `bs4`
- `selenium`
- `webdriver_manager`
- `pandas`

You can install these dependencies using the following command:
```sh
pip install bs4 selenium webdriver_manager pandas

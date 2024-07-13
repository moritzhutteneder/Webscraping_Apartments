"""
Created on Thu Dec  7 11:59:09 2023
"""
# ----------------------------------------------------------------------------------------------------------------------------
# General remarks regarding the code:
# 
# Please execute the code in the following order:
# 1. Execute the imports and defined methods
# 2. Execute the code after the defined methods line by line to see the results for each objective, starting with the line 'driver = open_browser(url)'

# Objectives - we defined the following objectives for scraping:
# 1. Retrieve the list of all available apartments for rent in Barcelona from Engel & Völkers in a dataframe with the following attributes:
# 'Title', 'Location', 'Bedrooms', 'Bathrooms', 'Living Area', 'Price'
# 2. Calculate the average living area
# 3. Calculate the average price
# 4. Calculate the average price per square meter
# 5. Calculate the average amount of bedrooms
# 6. Calculate the average amount of bathrooms
# 7. Count the number of available offers for rent in Barcelona
# 8. Identify the biggest living area of an apartment for rent in Barcelona
# 9. Identify the highest price of an apartment for rent in Barcelona
# 10. Identify the most common location of apartments for rent in Barcelona and the number of offers in that location
# 11. Create a dataframe with the calculated results
# 12. Calculate the price per sqm for each neighborhood in Barcelona and display the results in a dataframe
# ----------------------------------------------------------------------------------------------------------------------------

# Imports
import bs4
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# The following method opens the browser and desired website, accepts the cookies, and returns the driver
def open_browser(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(2) # Add a waiting period of 2 seconds
    accept_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))) # Wait until the accept cookies button is clickable
    accept_cookies.click() # Click the accept cookies button
    time.sleep(2) # Add a waiting period of 2 seconds
    search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ev-search-btn"))) # Wait until the search button is clickable
    search_button.click() # Click the search button
    return driver # Return the driver

# The following method filters the website for apartments for rent in Barcelona
def filter_website(driver): 
    dropdown_for_rent_xpath = "//div[@class='ev-dropdown-head-label-filter-bar' and contains(text(), 'Buy')]" # The xpath of the dropdown menu for rent
    dropdown_for_rent = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, dropdown_for_rent_xpath))) # Wait until the dropdown menu for rent is clickable
    dropdown_for_rent.click() # Click the dropdown menu for rent

    dropdown_filter_for_rent_xpath = "//span[@class='ev-dropdown-value' and contains(text(), 'Rent')]" # The xpath of the filter for rent
    filter_for_rent = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, dropdown_filter_for_rent_xpath))) # Wait until the filter for rent is clickable
    filter_for_rent.click() # Click the filter for rent

    dropdown_property_type_xpath = "//div[@class='ev-dropdown-head-label-filter-bar' and contains(text(), 'Property Type')]" # The xpath of the dropdown menu for property type
    dropdown_property_type = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, dropdown_property_type_xpath))) # Wait until the dropdown menu for property type is clickable
    dropdown_property_type.click() # Click the dropdown menu for property type

    dropdown_filter_apartments_xpath = "//span[@class='ev-dropdown-value' and contains(text(), 'Apartment')]" # The xpath of the filter for apartments
    filter_apartments = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, dropdown_filter_apartments_xpath))) # Wait until the filter for apartments is clickable
    filter_apartments.click() # Click the filter for apartments



# The following method scrapes the webpage and returns the scraped data in lists
def scrape_webpage(driver):
    # Create empty lists for the data to be scraped
    titles = []
    locations = []
    bedrooms = []
    bathrooms = []
    living_area = []
    price = []
    # Create a counter to keep track of the number of available elements per offer and add None values to the lists if an element is missing
    counter = 1

    # The following while loop iterates through all pages of the website
    while True:
        offers = bs4.BeautifulSoup(driver.page_source, 'html.parser') # Parse the content to HTML format
        
        # The following for loop iterates through all offers on the current page
        for offer in offers.find_all('div', class_='ev-teaser-content'):
            titles.append(offer.find('div', class_='ev-teaser-title').text.strip()) # Add the title of the offer to the list
            locations.append(offer.find('div', class_='ev-teaser-subtitle').text.strip()) # Add the location of the offer to the list
            price.append(offer.find('div', class_='ev-value').text.strip()) # Add the price of the offer to the list
            for attribute in offer.find_all('div', class_='ev-teaser-attribute'): # Iterate through all attributes of the offer
                icon_title = attribute.find('img')['title'] # Get the title of the icon
                value_span = attribute.find('span', class_='ev-teaser-attribute-value') # Get the value of the attribute
                # The following if clauses check which attribute is currently being processed and adds the value to the corresponding list
                if icon_title == "Bedrooms" or icon_title == "Rooms": # The website uses two different icons for the number of bedrooms/rooms in an offer
                    bedrooms.append(value_span.text.strip()) # Add the number of bedrooms/rooms to the list
                elif icon_title == "Bathrooms": 
                    bathrooms.append(value_span.text.strip()) # Add the number of bathrooms to the list
                elif icon_title == "Square Footage" or icon_title == "Total Surface Area": # The website uses two different icons for the living/surface area in an offer
                    living_area.append(value_span.text.strip()) # Add the living/surface area to the list
            # The following if clauses check whether an item is missing in the list. If so, it adds a None value to the list.
            if len(bedrooms) < counter: 
                bedrooms.append(None) # Add a None value to the list if the number of bedrooms is missing
            if len(bathrooms) < counter:
                bathrooms.append(None) # Add a None value to the list if the number of bathrooms is missing
            if len(living_area) < counter:
                living_area.append(None) # Add a None value to the list if the living area is missing
            counter += 1 # Increase the counter by 1
        try:
            time.sleep(1) # Add a waiting period of 1 second
            driver.execute_script("window.scrollBy(0,3000)") # Scroll down the page
            next_page = driver.find_element(By.CLASS_NAME, "ev-pager-next") # Find the button for the next page
            time.sleep(3) # Add a waiting period of 3 seconds
            next_page.click() # Click the button for the next page
        except NoSuchElementException: # If the button for the next page is not found (last page), break the while loop
            break
        
    return titles, locations, bedrooms, bathrooms, living_area, price

# The following method creates a dataframe from the scraped data
def create_dataframe(titles, locations, bedrooms, bathrooms, living_area, price):
    # Create a dictionary from the lists
    data = {
        'Title': titles,
        'Location': locations,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'Living Area': living_area,
        'Price': price
    }
    # Create a dataframe from the dictionary
    df = pd.DataFrame(data)
    return df

# The following method transforms the data in the dataframe and returns the transformed dataframe
def transform_data(df):
    df_transformed = df.copy() # Create a copy of the dataframe
    # Modify the 'Living Area' column so that all values are in the same unit (sqft) and the values are floats
    for i in range(len(df_transformed['Living Area'])):
        value = df_transformed.at[i, 'Living Area'] # Get the value of the cell
        if value is not None:
            value = value.replace(',', '') # Remove the comma from the string
            if 'sqft' in value:
                value = value.replace(' sqft', '') # Remove the unit
                value = float(value) * 0.09290304  # Convert sqft to sqm
                value = round(value, 2)  # Round the value to two decimals
            elif 'ac' in value:
                value = value.replace(' ac', '') # Remove the unit
                value = float(value) * 4046.86  # Convert acres to sqm
                value = round(value, 2)  # Round the value to two decimals
            df_transformed.at[i, 'Living Area'] = value # Write the new (tranformed) value to the cell
    
    # Remove currency symbol and comma from price column
    df_transformed['Price'] = df_transformed['Price'].str.replace(' EUR', '').str.replace(',', '')

    # Convert price values to integers (only for non-none values)
    for i in range(len(df_transformed['Price'])):
        value = df_transformed.at[i, 'Price']
        if value is not None:
            value = int(value)
            df_transformed.at[i, 'Price'] = value

    # Tranform the values in 'Bedrooms' column to integers (only for non-none values)
    for i in range(len(df_transformed['Bedrooms'])):
        value = df_transformed.at[i, 'Bedrooms']
        if value is not None:
            value = int(value)
            df_transformed.at[i, 'Bedrooms'] = value

    # Tranform the values in 'Bathrooms' column to integers (only for non-none values)
    for i in range(len(df_transformed['Bathrooms'])):
        value = df_transformed.at[i, 'Bathrooms']
        if value is not None:
            value = int(value)
            df_transformed.at[i, 'Bathrooms'] = value

    # Reduce the values in the 'Location' column to the name of the neighborhood (without Spain and Barcelona)
    for i in range(len(df['Location'])):
        value = df_transformed.at[i, 'Location']
        if value is not None:
            value = value.replace('Spain, ', '').replace('Barcelona, ', '').strip()
            df_transformed.at[i, 'Location'] = value

    return df_transformed # Return the transformed dataframe

# The following method calculates the results for the objectives 2-10 and returns them in a dataframe
def calculate_results(df):
    # Calculate the average living area
    average_living_area = round(df['Living Area'].mean(), 2)

    # Calculate the average price
    average_price = round(df['Price'].mean(), 2)

    # Calculate the average price per square meter based on the values in the dataframe
    average_price_per_sqm_df = round(df['Price'].sum() / df['Living Area'].sum(), 2)

    # Calculate the average amount of bedrooms
    average_bedrooms = round(df['Bedrooms'].mean())

    # Calculate the average amount of bathrooms
    average_bathrooms = round(df['Bathrooms'].mean())

    # Identify the most common location of apartments for rent in Barcelona and the number of offers in that location
    most_common_location = transformed_df['Location'].value_counts().idxmax()
    num_offers_in_location = transformed_df['Location'].value_counts().max()

    # Identify the biggest living area of an apartment for rent in Barcelona
    biggest_apartment = df['Living Area'].max()

    # Identify the most expensive price of an apartment for rent in Barcelona
    most_expensive_apartment = df['Price'].max()

    # Count the number of offers for rent in Barcelona
    num_rows = df.shape[0]

    # Create a new dataframe with the calculated results
    results_df = pd.DataFrame({
        'Average Living Area': [str(average_living_area) + ' sqm'],
        'Average Price': [str(average_price) + ' EUR/month'],
        'Average Price per Square Meter': [str(average_price_per_sqm_df) + ' EUR/m2'],
        'Average Number of Bedrooms': [str(average_bedrooms)],
        'Average Number of Bathrooms': [str(average_bathrooms)],
        'Biggest Living Area': [str(biggest_apartment) + ' sqm'],
        'Rent of Most Expensive Apartment': [str(most_expensive_apartment) + ' EUR/month'],
        'Most Common Location': [most_common_location + ' (' + str(num_offers_in_location) + ' offers)'],
        'Number of Available Offers for Rent in Barcelona': [str(num_rows)]
    })

    return results_df

# The following method calculates the price per sqm for each neighborhood in Barcelona and returns the results in a dataframe
def calculate_price_index(df):
    # Calculate the average price per square meter based on the values in the dataframe
    modified_df = df.copy()

    # Create a new column in the dataframe with the price per sqm for each offer
    modified_df['Price per sqm (in EUR)'] = modified_df['Price'] / modified_df['Living Area']

    # Create a new dataframe with the price per sqm for each neighborhood
    price_per_sqm_df = modified_df.groupby('Location')['Price per sqm (in EUR)'].mean().reset_index()

    # Sort the dataframe in descending order based on the average price per square meter
    price_per_sqm_df = price_per_sqm_df.sort_values(by='Price per sqm (in EUR)', ascending=False).reset_index(drop=True)

    # Round the values in the 'Price per sqm (in EUR)' column to two decimal places
    # The following line is commented since it did not work in VS Code; however in Spyder it worked (if you want rounded values and use Spyder just uncomment the line)
    # price_per_sqm_df['Price per sqm (in EUR)'] = price_per_sqm_df['Price per sqm (in EUR)'].round(2)

    return price_per_sqm_df

# ----------------------------------------------------------------------------------------------------------------------------
# 1. Retrieve the list of all available apartments for rent in Barcelona from Engel & Völkers in a dataframe with the following attributes:
# 'Title', 'Location', 'Bedrooms', 'Bathrooms', 'Living Area', 'Price'

# url of the webpage to be scraped
url = "https://www.engelvoelkers.com/en-es/barcelona/"
driver = open_browser(url)
filter_website(driver)
titles, locations, bedrooms, bathrooms, living_area, price = scrape_webpage(driver)
scraped_df = create_dataframe(titles, locations, bedrooms, bathrooms, living_area, price)
print(scraped_df)
driver.quit() # Close the browser

# Transform the data in the dataframe so that it can be used for the calculations
transformed_df = transform_data(scraped_df)
print(transformed_df)

# ----------------------------------------------------------------------------------------------------------------------------
# 2. Calculate the average living area
# 3. Calculate the average price
# 4. Calculate the average price per square meter
# 5. Calculate the average amount of bedrooms
# 6. Calculate the average amount of bathrooms
# 7. Count the number of available offers for rent in Barcelona
# 8. Identify the biggest living area of an apartment for rent in Barcelona
# 9. Identify the highest price of an apartment for rent in Barcelona
# 10. Identify the most common location of apartments for rent in Barcelona and the number of offers in that location
# 11. Create a dataframe with the calculated results
results_df = calculate_results(transformed_df)
print(results_df)

# ----------------------------------------------------------------------------------------------------------------------------
# 12. Calculate the price per sqm for each neighborhood in Barcelona and display the results in a dataframe
price_per_sqm_df = calculate_price_index(transformed_df)
print(price_per_sqm_df)

# ----------------------------------------------------------------------------------------------------------------------------
# Conclusion: All objectives have been achieved. The results are summarized in the dataframes 'results_df' and 'price_per_sqm_df'.

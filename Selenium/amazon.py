from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
global filter
filter = "headphones"
driver = webdriver.Chrome()

def start_driver():
    driver.get("https://www.amazon.in/ref=nav_logo")
    time.sleep(8) # to enter the captcha in case
    
    
    # Enter search term
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(filter)
    print(f"Filter applied: {filter}")

    # Click search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "nav-search-submit-button"))
    )
    search_button.click()
    print("Search button clicked")

def click_next():
    """Click the next button to move to the next page."""
    try:
        next_button = driver.find_element(By.CLASS_NAME, "s-pagination-next")
        next_button.click()
        print("Moving to next page")
        time.sleep(1)
    except:
        print("No more pages")

def extract_numeric_value(text):
    """Extracts the first numeric value (integer or float) from a string."""
    match = re.search(r"\d+(\.\d+)?", text)  # Match 4.1 or 2000
    return float(match.group()) if match else None

# def scrap():
#     print("Scraping started...")
#     product_titles = []
#     product_ratings = []
#     product_prices = []

#     for _ in range(10):  # Scrape first page (modify for more pages)
#         time.sleep(1)  # Wait for the page to load

#         # Extract product titles, rating, prices
#         titles = driver.find_elements(By.XPATH, "//h2[@class='a-size-medium a-spacing-none a-color-base a-text-normal']")
#         ratings = driver.find_elements(By.XPATH, "//a[contains(@class, 'a-popover-trigger') and contains(@aria-label, 'out of 5')]")
#         prices = driver.find_elements(By.XPATH, "//span[@class='a-price']")
#         for i in range(min(len(titles),len(prices),len(ratings))):
#             title = titles[i].text.strip()
#             rating = extract_numeric_value(ratings[i].get_attribute("aria-label")) if i < len(ratings) else None
#             price = prices[i]

#             # if title and rating and price:
#             #     product_titles.append(title)
#             #     product_ratings.append(rating)
#             #     product_prices.append(price)

#             print(f"Title: {title}")
#             print(f"Rating: {rating}")
#             print(f"price : {price.text}")

#         click_next()

#     return titles, ratings, prices

# def scrap():
#     print("Scraping started...")
#     product_titles = []
#     product_ratings = []
#     product_prices = []

#     for _ in range(1):  # Scrape first page (modify for more pages)
#         time.sleep(2)  # Wait for the page to load

#         # Extract product details
#         titles = driver.find_elements(By.XPATH, "//h2[@class='a-size-medium a-spacing-none a-color-base a-text-normal']")
#         ratings = driver.find_elements(By.XPATH, "//a[contains(@class, 'a-popover-trigger') and contains(@aria-label, 'out of 5')]")
#         prices = driver.find_elements(By.XPATH, "//span[@class='a-price']//span[@class='a-offscreen']")
#         print(len(titles), len(prices), len(ratings))
#         # Find the minimum length to avoid index errors
#         # min_length = min(len(titles), len(prices), len(ratings))

#         # for i in range(min_length):
#         #     title = titles[i].text.strip()
#         #     rating = extract_numeric_value(ratings[i].get_attribute("aria-label")) if i < len(ratings) else "N/A"
#         #     price = prices[i].text if i < len(prices) else "N/A"

#         #     product_titles.append(title)
#         #     product_ratings.append(rating)
#         #     product_prices.append(price)

#         #     print(f"Title: {title}")
#         #     print(f"Rating: {rating}")
#         #     print(f"Price: {price}\n")

#         # click_next()

#     return product_titles, product_ratings, product_prices


def scrap():
    print("Scraping started...")
    product_titles = []
    product_ratings = []
    product_prices = []

    for _ in range(10):  # Scrape only the first page (modify for more pages)
        time.sleep(1)  # Wait for the page to load

        # Find all product containers
        product_containers = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

        for product in product_containers:
            try:


                # Extract Title
                title_element = product.find_element(By.XPATH, ".//h2[@class='a-size-medium a-spacing-none a-color-base a-text-normal']")
                title = title_element.text.strip()
            except:
                title = "N/A"

            try:
                # Extract Rating
                rating_element = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']")
                rating = extract_numeric_value(rating_element.get_attribute("innerHTML"))
            except:
                rating = "N/A"

            try:
                # Extract Price (Handle multiple cases)
                price_element = product.find_element(By.XPATH, ".//span[@class='a-price-whole']")
                price_fraction = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']")
                price = f"{price_element.text}.{price_fraction.text}"  # Combine whole + fraction part
            except:
                try:
                    price_element = product.find_element(By.XPATH, ".//span[@class='a-price']")
                    price = price_element.text.strip()
                except:
                    price = "N/A"

            product_titles.append(title)
            product_ratings.append(rating)
            product_prices.append(price)

            print(f"Title: {title}")
            print(f"Rating: {rating}")
            print(f"Price: {price}\n")

        click_next()

    return product_titles, product_ratings, product_prices

import pandas as pd

def csv_write(titles, ratings, prices, filename):
    """Writes product titles, ratings, and prices to a CSV file."""
    
    # Create a dictionary with the data
    data = {
        "Title": titles,
        "Rating": ratings,
        "Price (₹)": prices
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Write to CSV file
    df.to_csv(filename, index=False, encoding="utf-8")
    
    print(f"✅ Data successfully written to {filename}")


# Run the script
start_driver()
time.sleep(1)
titles, ratings, prices = scrap()
csv_write(titles,ratings,prices,filename=f"{filter}.csv")

driver.quit()

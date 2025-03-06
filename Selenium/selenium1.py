from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv('email')
PASSWORD = os.getenv("password")

if not EMAIL or not PASSWORD:
    print("Error: Email or Password not found in .env file!")
    exit()

# Step 1: Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Step 2: Open the Target Webpage
driver.get("https://accounts.google.com/signin")
print("Test case started")

try:
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_field.send_keys(EMAIL)
    print("Entered email")

    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    next_button.click()
    print("Clicked Next")

    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Passwd")))
    password_field.send_keys(PASSWORD)
    print("Entered password")

    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    next_button.click()
    print("Clicked Next after entering password")

    WebDriverWait(driver, 10).until(EC.title_contains("Google"))
    print("Login Successful! Current Page:", driver.title)

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
    print("Test case finished")

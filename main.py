from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver
driver = webdriver.Chrome()

# Login to LinkedIn
driver.get("https://www.linkedin.com/login")
time.sleep(3)

# Fill in your credentials
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
username.send_keys("your@gmail.com") ## Enter linkedin username/gmail
password.send_keys("pass@123") ## Enter Linkedin password
password.send_keys(Keys.RETURN)

time.sleep(5)  # Wait for the login to complete

# Navigate to the Companies Search URL
driver.get("https://www.linkedin.com/search/results/companies/?sid=.lk")
time.sleep(3)

# Scrape Pages
for page in range(1, 11):  # Loop through the first 10 pages
    time.sleep(3)  # Allow page to load fully
    html = driver.page_source
    with open(f"page_{page}.html", "w", encoding="utf-8") as file:
        file.write(html)
    print(f"Saved page {page}")

    try:
        # Auto-scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for content to load after scrolling
        
        # Explicit wait for the next button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Next')]"))
        )
        ActionChains(driver).move_to_element(next_button).click().perform()  # Move to button and click
    except Exception as e:
        print(f"Error on page {page}: {e}")
        break

# Close the browser
driver.quit()

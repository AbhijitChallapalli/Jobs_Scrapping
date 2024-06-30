import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import os
from dotenv import load_dotenv

load_dotenv()
username = os.environ.get("LINKEDIN_USER")
password = os.environ.get("LINKEDIN_PASS")

def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(email)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

def scrape_jobs(driver):
    job_list = []
    job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container")

    for card in job_cards:
        try:
            job_title = card.find_element(By.CSS_SELECTOR, "strong").text
            company_name = card.find_element(By.CLASS_NAME, "job-card-container__primary-description").text
            location = retry_find_text(card, By.CLASS_NAME, "job-card-container__metadata-wrapper")
            job_list.append({"title": job_title, "company": company_name, "location": location})
        except StaleElementReferenceException:
            continue  # Skip this card if any of its elements have gone stale

    return job_list

def retry_find_text(element, by, value):
    attempts = 0
    while attempts < 3:
        try:
            return element.find_element(by, value).text
        except StaleElementReferenceException:
            time.sleep(1)  # Wait a bit for the DOM to stabilize
            attempts += 1
    return ""

def save_jobs_to_csv(jobs):
    keys = jobs[0].keys()
    with open('jobs.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(jobs)

chrome_options = Options()
chrome_options.binary_location = '/opt/google/chrome/google-chrome'
service = Service('/home/abhijit/Jobs_Scrapping/chromedriver-linux64/chromedriver-linux64/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    linkedin_login(driver, username, password)
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(20)

    # Set search parameters
    search_box = driver.find_element(By.CLASS_NAME, "jobs-search-box__text-input")
    search_box.send_keys("Data Engineer" + Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results__list-item")))
    time.sleep(3)

    # Click the 'Date posted' dropdown to open it
    date_posted_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='searchFilter_timePostedRange']"))
    )
    date_posted_dropdown.click()

    # Wait for the 'Past 24 hours' option to become visible and click it
    # Attempt to click the label for better interaction
    past_24_hours_label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='timePostedRange-r86400']"))
    )
    past_24_hours_label.click()

    # Click the 'Show results' button to apply the filter
    apply_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Apply current filter to show results']"))
    )
    apply_button.click()

    # Wait for filtered results to load
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "job-card-container")))
    
    # Scrape the job posts
    jobs = scrape_jobs(driver)
    save_jobs_to_csv(jobs)

finally:
    input("Press Enter to close the browser...")
    driver.quit()

print("Automation script executed successfully.")




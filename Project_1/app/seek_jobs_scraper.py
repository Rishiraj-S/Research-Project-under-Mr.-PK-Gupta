import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def scrape_seek_jobs(output_file="data/jobs_data.csv"):
    # Configure Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Seek job search URL
    seek_url = "https://www.seek.com.au/"

    # Locations and Companies
    location = "Australia"
    companies = ["Tata Consultancy Services", "Infosys", "Tech Mahindra", "HCLTech", "Wipro", "LTIMindtree", "Cognizant"]

    # Data storage
    job_data = []

    driver.get(seek_url)
    time.sleep(3)

    for company in companies:
        print(f"Searching for {company} jobs in {location}...")
        
        # Find the search box and enter query
        try:
            search_box = driver.find_element(By.NAME, "keywords")
            search_box.send_keys(Keys.CONTROL + "a")  # Select all text
            search_box.send_keys(Keys.DELETE)  # Clear text
            search_box.send_keys(f"{company}")
            search_box.send_keys(Keys.RETURN)
            time.sleep(5)
        except Exception as e:
            print("Error interacting with Seek search box:", e)
            continue
        
        # Extract Job Listings
        while True:
            job_cards = driver.find_elements(By.CSS_SELECTOR, "article[data-automation='normalJob']")
            print(f"Found {len(job_cards)} job cards for {company} in {location}.")
            
            for job_card in job_cards:
                try:
                    title = job_card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").text
                    company_name = job_card.find_element(By.CSS_SELECTOR, "a[data-automation='jobCompany']").text
                    # location_text = job_card.find_element(By.CSS_SELECTOR, "[data-automation='jobLocation']").text
                    content = job_card.find_element(By.CSS_SELECTOR, "[data-automation='jobShortDescription']").text if job_card.find_elements(By.CSS_SELECTOR, "[data-automation='jobShortDescription']") else "N/A"
                    apply_link = job_card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").get_attribute("href")
                    
                    job_data.append({
                        "Job Title": title,
                        "Company Name": company_name,
                        "Location": location,
                        "Content": content,
                        "Link": apply_link
                    })
                except Exception as e:
                    print(f"Error extracting job details: {e}")
            
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a[data-automation='pageNext']")
                if "disabled" in next_button.get_attribute("class"):
                    print(f"No more job listings for {company} in {location}.")
                    break
                next_button.click()
                time.sleep(5)
            except:
                print(f"No more job listings for {company} in {location}.")
                break

    # Close driver
    driver.quit()

    # Load existing data if CSV file exists
    if os.path.exists(output_file):
        existing_df = pd.read_csv(output_file)
        existing_titles = set(existing_df["Job Title"].tolist())
    else:
        existing_df = pd.DataFrame()
        existing_titles = set()
    
    # Filter new jobs
    new_jobs = [job for job in job_data if job["Job Title"] not in existing_titles]
    
    # Save updated data
    if new_jobs:
        new_df = pd.DataFrame(new_jobs)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(output_file, index=False)
        print(f"Job search completed. Data saved to {output_file}")
    else:
        print("No new job listings found. CSV file remains unchanged.")

if __name__ == "__main__":
    scrape_seek_jobs()
    

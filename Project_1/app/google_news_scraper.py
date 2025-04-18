import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    """
    Scrapes the given URL and extracts text content from all anchor tags.
    Implements user-agent rotation and request delays to avoid being blocked.
    
    Parameters:
        url (str): The URL to scrape.
    
    Returns:
        str: Extracted text content from anchor tags or an empty string if scraping fails.
    """
    
    USER_AGENTS = [  # List of different user agents for rotation
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    # Delay settings in seconds to avoid being flagged as a bot
    REQUEST_DELAY = 2  # Delay between requests
    UA_DELAY = 1  # Delay between switching user agents
    
    success = False
    
    for user_agent in USER_AGENTS:
        headers = {"User-Agent": user_agent}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Parse HTML content
                soup = BeautifulSoup(response.text, "html.parser")
                link_texts = [link.get_text(strip=True) for link in soup.find_all("a", href=True)]
                page_content = " ".join(link_texts)
                success = True
                break  # Stop trying other user agents if successful
            else:
                print(f"Failed with UA '{user_agent}': {url} (Status Code: {response.status_code})")
        except Exception as e:
            print(f"Error with UA '{user_agent}' for URL {url}: {e}")
        
        time.sleep(UA_DELAY)  # Wait before trying the next user agent
    
    if not success:
        page_content = ""
    
    time.sleep(REQUEST_DELAY)  # Final delay before returning the result
    
    return page_content

def scrape_google_news(companies, locations, keywords, pages):
    """
    Scrapes Google News for Generative AI-related articles for given companies and locations.
    Uses Selenium to navigate through Google News and extract relevant article information.
    
    Parameters:
        companies (list): List of company names to search for.
        locations (list): List of locations to include in the search query.
        pages (int): Number of pages to scrape per search query.
    
    Returns:
        pd.DataFrame: DataFrame containing extracted news headlines, sources, descriptions, and links.
    """
    
    # Configure Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximize browser window
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Reduce detection as a bot
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    news_data = []  # List to store scraped news data
    
    for keyword in keywords:
        for location in locations:
            for company in companies:
                print(f"Searching for {company} news in {location}...")
                search_query = f"{company} + Generative AI + {keyword} + {location}"  # Construct search query
                driver.get("https://www.google.com/")
                time.sleep(random.uniform(3, 8))
        
                # Locate Google search box and enter query
                search_box = driver.find_element(By.NAME, "q")
                search_box.send_keys(search_query)
                search_box.send_keys(Keys.RETURN)
                time.sleep(random.uniform(3, 8))
        
                try:
                    # Click on the 'News' tab
                    news_tab = driver.find_element(By.LINK_TEXT, "News")
                    news_tab.click()
                    time.sleep(random.uniform(3, 8))
                except Exception as e:
                    print(f"Could not find the News tab for {company}: {e}")
                    continue
        
                page = 1
                while page <= pages:
                    articles = driver.find_elements(By.XPATH, '//div[@class="SoaBEf"]')
                    print(f"Found {len(articles)} news articles on page {page}.")
        
                    for article in articles:
                        try:
                            # Extract headline
                            headline_element = article.find_element(By.XPATH, './/div[contains(@class, "n0jPhd")]')
                            headline = headline_element.text if headline_element else "N/A"
        
                            # Extract article link
                            link_element = article.find_element(By.XPATH, './/a')
                            link = link_element.get_attribute('href') if link_element else "N/A"
        
                            # Extract source name
                            source_element = article.find_element(By.XPATH, './/div[contains(@class, "MgUUmf")]')
                            source = source_element.text if source_element else "N/A"

                            # Scrape article content from the URL
                            content = scrape_url(link)
        
                            # Store extracted data
                            news_data.append({
                                "Company": company,
                                "Location": location,
                                "Headline": headline,
                                "Source": source,
                                "Content": content,
                                "Link": link
                            })
                        except Exception as e:
                            print(f"Error extracting news details for {company} in {location}: {e}")
        
                    try:
                        # Navigate to the next page
                        next_button = driver.find_element(By.LINK_TEXT, "Next")
                        next_button.click()
                        time.sleep(random.uniform(3, 8))
                        page += 1
                    except:
                        print(f"No more pages available for {company} in {location}.")
                        break
    
    driver.quit()  # Close the browser
    
    # Convert collected data into a DataFrame and save as CSV
    df = pd.DataFrame(news_data)
    df.to_csv("data/google_news.csv", index=False)
    
    return df

if __name__=='__main__':
    companies = ['Tata Consultancy Services', 'Infosys', 'Wipro', 'LTIMindtree', 'HCLTech', 'Tech Mahindra', 'Dell']
    locations = ["India", "Australia"]
    keywords = ['initiatives', 'investment', 'strategy']
    pages = 10

    df = scrape_google_news(companies, locations, keywords, pages)

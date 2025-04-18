import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import os
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
import warnings
import urllib3

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Configure user-agent rotation
ua = UserAgent()

def get_domain_name(url):
    """Extract domain name from URL"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        return domain.split(':')[0]  # Remove port if present
    except:
        return url.split('/')[2] if len(url.split('/')) > 2 else url

def setup_selenium():
    """Initialize Selenium with proper configurations"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set page load strategy
    chrome_options.page_load_strategy = 'eager'
    
    # Configure service
    service = Service(
        ChromeDriverManager().install(),
        port=0  # Auto-select port
    )
    
    # Initialize driver with timeout settings
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    return driver

def fetch_page_static(url):
    """Fetch webpage with retries and random user-agent"""
    headers = {'User-Agent': ua.random}
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            allow_redirects=True,
            verify=False  # Bypass SSL verification
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"🚨 Static fetch failed for {url}: {str(e)}")
        return None

def extract_content_static(html, url):
    """Extract content using BeautifulSoup"""
    if not html:
        return None, None
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Company name extraction
        company_name = (
            soup.find('meta', property='og:site_name') or 
            soup.find('meta', attrs={'name': 'application-name'})
        )
        company_name = company_name.get('content') if company_name else None
        if not company_name:
            company_name = get_domain_name(url).split('.')[0].capitalize()
        
        # Content extraction
        content_selectors = [
            {'name': 'main'},
            {'tag': 'article'},
            {'class': 'main-content'},
            {'id': 'content'},
            {'role': 'main'}
        ]
        
        for selector in content_selectors:
            element = soup.find(**selector)
            if element:
                return company_name, ' '.join(element.stripped_strings)[:100000]
        
        return company_name, ' '.join(soup.body.stripped_strings)[:100000] if soup.body else None
    except Exception as e:
        print(f"⚠️ Static parsing failed for {url}: {str(e)}")
        return None, None

def extract_content_dynamic(driver, url):
    """Extract content using Selenium for JS-heavy sites"""
    try:
        # Set timeouts
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        
        # Navigate with retry
        try:
            driver.get(url)
        except TimeoutException:
            print(f"⚠️ Page load timeout for {url}, retrying...")
            driver.execute_script("window.stop();")
            time.sleep(2)
            driver.get(url)
        
        # Wait for JavaScript
        time.sleep(3)
        
        # Extract company name
        company_name = driver.execute_script("""
            return document.title?.split('|')[0]?.split('-')[0]?.trim() || 
                   document.querySelector('meta[property=\"og:site_name\"]')?.content ||
                   window.location.hostname?.split('.')[0]?.capitalize();
        """)
        
        # Extract content with fallbacks
        content = driver.execute_script("""
            return document.body?.innerText || 
                   document.querySelector('main')?.innerText || 
                   document.querySelector('article')?.innerText ||
                   document.documentElement?.innerText;
        """)
        
        return company_name, content[:100000] if content else None
    except Exception as e:
        print(f"⚠️ Dynamic extraction failed for {url}: {str(e)}")
        return None, None

def process_urls(file_path, delay=2, max_retries=3):
    """Process URLs from file with proper path handling"""
    # Fix path formatting
    try:
        file_path = os.path.normpath(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"❌ File error: {str(e)}")
        return pd.DataFrame()
    
    results = []
    selenium_driver = None
    
    for i, url in enumerate(urls, 1):
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        
        print(f"🌐 Processing ({i}/{len(urls)}): {url}")
        
        # Skip problematic URLs
        if any(domain in url for domain in ['drive.google.com', 'youtube.com']):
            print("⏩ Skipping unsupported URL")
            continue
            
        # Try static first
        company_name, content = None, None
        html = fetch_page_static(url)
        if html:
            company_name, content = extract_content_static(html, url)
        
        # Fallback to Selenium if static failed
        if not content:
            for attempt in range(max_retries):
                try:
                    if selenium_driver is None:
                        selenium_driver = setup_selenium()
                    company_name, content = extract_content_dynamic(selenium_driver, url)
                    if content:
                        break
                except Exception as e:
                    print(f"⚠️ Attempt {attempt + 1} failed: {str(e)}")
                    if selenium_driver:
                        selenium_driver.quit()
                        selenium_driver = None
                    time.sleep(5)
        
        if content:
            results.append({
                'domain_name': get_domain_name(url),
                'company_name': company_name,
                'url': url,
                'content': content
            })
        
        time.sleep(delay)
    
    if selenium_driver:
        selenium_driver.quit()
    
    df = pd.DataFrame(results)
    grouped_df = df.groupby(['domain_name', 'company_name']).agg({
    'url': list,
    'content': lambda x: "\n\n".join(x) # Separate the grouped content by 2 newline characters
    }).reset_index()

    return grouped_df

if __name__ == "__main__":
    # Get absolute paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    indian_path = os.path.join(base_dir, 'data', 'indian_startups.txt')
    australian_path = os.path.join(base_dir, 'data', 'australian_startups.txt')
    dell_path = os.path.join(base_dir, 'data', 'dell.txt')
    
    print("🚀 Processing Indian startups...")
    df_ind = process_urls(indian_path)
    
    print("\n🚀 Processing Australian startups...")
    df_aus = process_urls(australian_path)

    print("🚀 Processing Dell...")
    df_dell = process_urls(dell_path)
    
    # Save results separately
    if not df_ind.empty:
        indian_output = os.path.join(base_dir, 'data', 'indian_startups.csv')
        df_ind.to_csv(indian_output, index=False)
        print(f"\n✅ Saved {len(df_ind)} Indian records to {indian_output}")
    
    if not df_aus.empty:
        australian_output = os.path.join(base_dir, 'data', 'australian_startups.csv')
        df_aus.to_csv(australian_output, index=False)
        print(f"✅ Saved {len(df_aus)} Australian records to {australian_output}")
    
    if df_ind.empty and df_aus.empty:
        print("❌ No data collected from either file")
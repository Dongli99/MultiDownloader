import os
import re
import time
import wget
from bs4 import BeautifulSoup
from selenium import webdriver

def download_files(url, pattern, download_dir):
    # Create the download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)

    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()  # Change to the appropriate WebDriver

    # Navigate to the target URL
    driver.get(url)

    # Wait for the page to load (you might need to adjust the time)
    time.sleep(5)

    # Get the page source after JavaScript execution
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find links matching the pattern using BeautifulSoup
    links = soup.find_all('a', href=re.compile(pattern))
    
    # If links are not found, try using Selenium to find links
    if len(links) == 0:
        links = driver.find_elements_by_xpath("//a[contains(@href, '.zip')]")
        if len(links) == 0:
            print('link not found')
            driver.quit()
            return

    # Download each file
    for link in links:
        file_url = link.get('href')
        file_name = os.path.basename(file_url)
        file_path = os.path.join(download_dir, file_name)
        print(f"Downloading {file_name}...")
        wget.download(file_url, out=file_path)
        print(f"{file_name} downloaded!")

    driver.quit()

if __name__ == "__main__":
    target_url = "https://www.example.com/index.html"  # Replace with the webpage URL
    file_pattern = r'\.zip$'  # Regular expression to match .zip files
    save_directory = "D:\downloads"  # Local directory to save downloaded files

    download_files(target_url, file_pattern, save_directory)

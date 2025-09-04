import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
from termcolor import colored
from urllib.parse import urljoin

def print_header(config):
    print(colored("\n---- Let's Scrap these images ----\n", attrs=["bold"]))
    print(colored(f"config : {config}\n", "yellow", attrs=["bold"]))


def hub(config):
    print_header(config)
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    # Added a timeout to prevent the script from blocking indefinitely
    driver.set_page_load_timeout(20)

    # --- Recursion Configuration ---
    if config['recursive'] is True:
        max_depth = config['level']
    else:
        max_depth = 0

    # List of allowed image extensions
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    # urls_to_visit: our "to-do list"
    # Each element is a pair: (url, current_depth)
    urls_to_visit = [(config['url'], 0)]
    
    # visited_urls: to avoid processing the same page twice
    visited_urls = []
    
    # --- Main crawling loop ---
    while urls_to_visit:
        # Get the first URL and its depth from the list
        current_url, current_depth = urls_to_visit.pop(0)

        # Check if we should skip this URL
        if current_url in visited_urls or current_depth > max_depth:
            continue

        print(colored(f"\n[Depth {current_depth}] Processing: {current_url}", "cyan", attrs=["bold"]))
        visited_urls.append(current_url)

        try:
            # Navigate to the current URL
            driver.get(current_url)
            
            # Simple wait to let JS load
            time.sleep(2)

            # Try to close the cookie pop-up if there is one
            try:
                accept_button = driver.find_element(By.ID, "didomi-notice-agree-button")
                if accept_button:
                    accept_button.click()
                    time.sleep(1) # Wait for the pop-up to disappear
            except:
                pass # No button, continue

            # --- Image search logic ---
            print("Site is open. Searching for images...")
            imgs = driver.find_elements(By.TAG_NAME, 'img')
            imgs_urls = []
            for img in imgs:
                # Try the 'src' attribute, and if it's empty, try 'data-src'.
                # This is to handle "lazy loading" where the image URL is hidden.
                src = img.get_attribute('src') or img.get_attribute('data-src')

                # If a URL (src) is found, process it.
                if src:
                    # If the URL is relative, convert it to an absolute URL.
                    if not src.startswith(('http', 'https')):
                        src = urljoin(current_url, src)
                    
                    # Avoid adding duplicates and ensure the URL is valid
                    if src not in imgs_urls and src.startswith(('http', 'https')):
                        imgs_urls.append(src)
            
            # --- Download logic ---
            output_folder = config['path']
            for i, img_url in enumerate(imgs_urls):
                try:
                    print(f"  -> Downloading: {img_url}")
                    response = requests.get(img_url)
                    
                    file_ext = os.path.splitext(img_url.split('?')[0])[1]
                    if not file_ext in allowed_extensions:
                        file_ext = '.jpg'

                    file_name = os.path.join(output_folder, f"image_{len(visited_urls)}_{i}{file_ext}")
                    with open(file_name, 'wb') as f:
                        f.write(response.content)
                    print(colored(f"     Saved as: {file_name}", "green"))

                except Exception as e:
                    print(colored(f"     Error while downloading {img_url}: {e}", "red"))

            # --- Recursion logic: find new links ---
            if current_depth < max_depth:
                print(colored("  -> Searching for new links...", "yellow"))
                links = driver.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    href = link.get_attribute('href')
                    # Keep only valid links belonging to the same site
                    if href and href.startswith(config['url']):
                        
                        # Ignore anchors (#) to avoid visiting the same page multiple times
                        clean_href = href.split('#')[0]

                        if clean_href not in visited_urls:
                            # Also check that the URL is not already in the list to visit
                            # to avoid duplicates in the queue.
                            is_already_in_queue = any(clean_href == url_in_queue[0].split('#')[0] for url_in_queue in urls_to_visit)
                            if not is_already_in_queue:
                                urls_to_visit.append((href, current_depth + 1))

        except Exception as e:
            print(colored(f"Error while processing page {current_url}: {e}", "red"))

    # Ensures the browser and driver are properly closed at the end
    print(colored("\nCrawling finished.", attrs=["bold"]))
    driver.quit()

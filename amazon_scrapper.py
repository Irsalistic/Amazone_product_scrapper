from datetime import datetime
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import concurrent.futures

BASE_URL = "https://www.amazon.com/s"
search_queries = ["headphones", "smartphones", "laptops", "tablets", "cameras",
                  "earbuds", "smartwatches", "chargers", "speakers", "monitors"]



user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.4515.131 Safari/537.36"
# setting up selenium webdriver
def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# function use to scrape products for a given query
def scrape_products(search_query):
    print(f"Scraping products for query: {search_query}")
    driver = create_driver()
    driver.get(f"{BASE_URL}?k={search_query}")

    # Wait for the product list container to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
    )

    results = []
    scrape_date = datetime.now().strftime("%Y-%m-%d")
    for page in range(1, 21):
        print(f"Scraping page {page} for query: {search_query}...")

        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.s-main-slot > div[data-component-type='s-search-result']"))
        )

        products = driver.find_elements(By.CSS_SELECTOR,
                                        "div.s-main-slot > div[data-component-type='s-search-result']")

        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, "h2 > span").text.strip()
            except Exception:
                title = None

            try:
                aria_label = product.find_element(By.CSS_SELECTOR, "a[aria-label]").get_attribute("aria-label")
                rating = aria_label.split(' ')[0]
            except Exception:
                rating = None

            try:
                total_reviews = product.find_element(By.CSS_SELECTOR,
                                                     "div[data-csa-c-type='alf-af-component'] span.a-size-base.s-underline-text").text.strip()
            except Exception:
                total_reviews = None

            try:
                purchase_details = product.find_element(By.CSS_SELECTOR,
                                                        "div.a-section.a-spacing-none.a-spacing-top-micro > div.a-row.a-size-base > span").text.strip()
            except Exception:
                purchase_details = None

            try:
                price_whole = product.find_element(By.CSS_SELECTOR,
                                                   "div > div > span > div > div > div > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div:nth-child(3) > div.puisg-col.puisg-col-4-of-12.puisg-col-4-of-16.puisg-col-4-of-20.puisg-col-4-of-24 > div > div.a-section.a-spacing-none.a-spacing-top-micro.puis-price-instructions-style > div > div:nth-child(1) > a > span > span:nth-child(2) > span.a-price-whole").text.strip()

                price_fraction = product.find_element(By.CSS_SELECTOR,
                                                      "div > div > div > div > span > div > div > div > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div:nth-child(3) > div.puisg-col.puisg-col-4-of-12.puisg-col-4-of-16.puisg-col-4-of-20.puisg-col-4-of-24 > div > div.a-section.a-spacing-none.a-spacing-top-micro.puis-price-instructions-style > div > div:nth-child(1) > a > span > span:nth-child(2) > span.a-price-fraction").text.strip()

                price = f"${price_whole}.{price_fraction}"


            except Exception:

                try:

                    price = product.find_element(By.CSS_SELECTOR,

                                                 "div > div > span > div > div > div > div.puisg-col.puisg-col-4-of-12.puisg-col-8-of-16.puisg-col-12-of-20.puisg-col-12-of-24.puis-list-col-right > div > div > div:nth-child(3) > div.puisg-col.puisg-col-4-of-12.puisg-col-4-of-16.puisg-col-4-of-20.puisg-col-4-of-24 > div > div:nth-child(3) > div > span.a-color-base").text.strip()

                    # price = f"{price} USD"

                except Exception:

                    price = None

            try:
                image_url = product.find_element(By.CSS_SELECTOR,
                                                 "div.a-section.aok-relative.s-image-fixed-height img.s-image").get_attribute(
                    "src")
            except Exception:
                image_url = None

            if title:
                results.append({
                    "title": title,
                    "rating": rating,
                    "total_reviews": total_reviews,
                    "purchase_details": purchase_details,
                    "price": price,
                    "image_url": image_url,
                    "creation_timestamp": datetime.now().isoformat(),
                    "update_timestamp": datetime.now().isoformat(),
                    "scrape_date": scrape_date,
                })

        if page < 20:
            try:
                next_button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.a-list-item a.s-pagination-next"))
                )
                next_button.click()
                WebDriverWait(driver, 15).until(
                    EC.staleness_of(products[0])
                )
                time.sleep(2)
            except Exception as e:
                print(f"Error navigating to the next page: {e}")
                break

    driver.quit()

    # Save results for the query in a JSON file
    file_name = f"{search_query.replace(' ', '_')}.json"
    with open(file_name, "w") as file:
        json.dump(results, file, indent=4)
    print(f"Results for '{search_query}' saved to {file_name}.")
    return results


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Run the scraping for each query in parallel
        executor.map(scrape_products, search_queries)

    print("Scraping completed for all queries.")


if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time

options = Options()
options.add_argument("--start-fullscreen")
# options.add_argument("--headless")  # Optional

service = Service()
driver = webdriver.Chrome(service=service, options=options)

# STEP 1: Open the textbook explore page
driver.get('https://www.betterworldbooks.com/explore/textbooks')
time.sleep(3)

# STEP 2: Close popup if it appears
try:
    driver.find_element(By.XPATH, '//*[@id="headerApp"]/div[2]/div/div/div[2]/div/div[2]/button').click()
except:
    print("No popup appeared.")
time.sleep(2)

# STEP 3: Collect main category links
category_links = []
for div_index in [2, 3]:
    index = 1
    while True:
        try:
            xpath = f'//*[@id="headerApp"]/div[2]/div/div/div[2]/div/div[2]/div/div[{div_index}]/ul/li[{index}]/a'
            element = driver.find_element(By.XPATH, xpath)
            href = element.get_attribute('href')
            if href:
                category_links.append(href)
            index += 1
        except:
            break

# STEP 4: Collect inner category links
inner_category_links = []
for link in category_links:
    driver.get(link)
    time.sleep(3)
    for i in range(1, 10):
        try:
            anchors = driver.find_elements(By.XPATH, f'//*[@id="exploreApp"]/div/div[{i}]//a')
            for a in anchors:
                href = a.get_attribute('href')
                if href and href.startswith('http'):
                    inner_category_links.append(href)
        except:
            continue
        time.sleep(0.5)

# STEP 5: Extract product links from inner category pages
product_links = []

for inner_link in inner_category_links:
    driver.get(inner_link)
    time.sleep(3)
    try:
        products = driver.find_elements(By.XPATH, '//div[contains(@class,"SearchResultsBookItem")]//a[@href]')
        for p in products:
            href = p.get_attribute('href')
            if href and '/product/detail/' in href:
                product_links.append(href)
    except:
        continue

# STEP 6: Visit each product page and collect data
def safe_text(xpath):
    try:
        return driver.find_element(By.XPATH, xpath).text.strip()
    except:
        return ""

def safe_attr(xpath, attr):
    try:
        return driver.find_element(By.XPATH, xpath).get_attribute(attr)
    except:
        return ""

scraped_books = []

for link in product_links[:20]:  # Limit for testing
    driver.get(link)
    time.sleep(4)

    image_src = safe_attr('//*[@id="detailApp"]/div[1]/div[1]/div[1]/img', 'src')
    title = safe_text('//*[@id="detailApp"]/div[1]/div[1]/div[2]/h1')
    rating = safe_text('//*[@id="detailApp"]/div[1]/div[1]/div[2]/h5[1]/span')
    author = safe_text('//*[@id="detailApp"]/div[1]/div[1]/div[2]/div[1]/a')
    cover_type = safe_text('//*[@id="detailApp"]/div[1]/div[1]/div[2]/h5[2]/span')
    condition = safe_text('//*[@id="detailApp"]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/strong')
    price = safe_text('//*[@id="detailApp"]/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/span')
    language = safe_text('//*[@id="details"]/div/div/div[2]/span')

    json_data = {
        "url": link,
        "image": image_src,
        "title": title,
        "rating": rating,
        "author": author,
        "cover_type": cover_type,
        "condition": condition,
        "price": price,
        "language": language
    }

    scraped_books.append(json_data)
    print(f"✅ Scraped: {title}")

# STEP 7: Save all data
with open('books_batch.json', 'w', encoding='utf-8') as f:
    json.dump(scraped_books, f, indent=2, ensure_ascii=False)

driver.quit()
print(f"\n✅ Done. Saved {len(scraped_books)} books to books_batch.json")

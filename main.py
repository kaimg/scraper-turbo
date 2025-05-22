import requests
import time
import re
from bs4 import BeautifulSoup # type: ignore
from lxml import html # type: ignore
from lxml.etree import tostring


INDEX_FILE = "templates/index.html"
CAR_INFO_FILE = "templates/car_info.html"
RESULT_FILE = "templates/result.html"
TEST_FILE = "templates/test.html"
CAR_LIST_FILE = "templates/car_list.txt"
BASE_URL = "https://turbo.az/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/ ",
}

def main_bs4():
    url = f"{BASE_URL}/autos"
    print("Fetching with BeautifulSoup...")
    start = time.time()
    response = requests.get(url, headers=HEADERS)
    #print(response.status_code)
    #print(response.text)
    soup = BeautifulSoup(response.text, "lxml")
    #print(soup.prettify())
    all = soup.find_all('div', 'products-i vipped')
    #print(all)
    
    end = time.time()
    print(f"BeautifulSoup time: {end - start:.4f} seconds")
    print(f"Found items: {len(all)}")
    
    with open(INDEX_FILE, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(str(item) for item in all))

def main_lxml(max_pages: int = 5):
    html_blocks = []
    ids = set()
    start = time.time()
    for page in range(1, max_pages + 1):
        if page > 1: pagination_url = f"?page={page}"
        else: pagination_url = ""

        url = f"{BASE_URL}/autos{pagination_url}"
        print(f"({page}/{max_pages}) Fetching with lxml...")
        
        
        response = requests.get(url, headers=HEADERS)
        #print(response.status_code)
        #print(response.text)
        tree = html.fromstring(response.text)
        elements = tree.cssselect('div.products-i.vipped')


        for el in elements:
            html_blocks.append(tostring(el, pretty_print=True, encoding='unicode'))
            
            # Extract bookmark <a> and get ID from href
            bookmark_links = el.cssselect('a[href*="/bookmarks"]')
            for a in bookmark_links:
                href = a.get("href", "")
                match = re.search(r'/autos/(\d+)-', href)
                if match:
                    ids.add(match.group(1))
    #print(elements[0].tostring())
    #ele = [el.text_content() for el in elements]
    end = time.time()
    print(f"lxml time: {end - start:.4f} seconds")
    print(f"Found items: {len(ids)}")
    print(f"Extracted IDs: {ids}")
    with open(TEST_FILE, "w", encoding="utf-8") as file:
        file.write('\n\n'.join(html_blocks))
    with open(CAR_LIST_FILE, "w", encoding="utf-8") as file:
        file.write('\n'.join(ids))
    
def get_car_list():
    with open(CAR_LIST_FILE, "r", encoding="utf-8") as file:
        car_ids = file.read().splitlines()
    return car_ids

def get_specific_car_info():
    car_ids = get_car_list()
    print(car_ids)
    for car_id in car_ids:
        car_url = f"{BASE_URL}/autos/{car_id}"
        response = requests.get(car_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        #print(soup.prettify())
        #with open(CAR_INFO_FILE, "w", encoding="utf-8") as file:
        #    file.write(soup.prettify())

def get_car_info_from_file():
    with open(CAR_INFO_FILE, "r", encoding="utf-8") as file:
        car_info = file.read()
    
    tree = html.fromstring(car_info)
    #print(tree.cssselect('div.products-i__price'))
    print(tree.cssselect('div.product-price')[0].text_content().strip())
    #print(tree.cssselect('div.products-i__name'))
    print(tree.cssselect('div.products-i__name')[0].text_content().strip())
    #print(tree.cssselect('div.products-i__attributes'))
    print(tree.cssselect('div.products-i__attributes')[0].text_content().strip())
    #print(tree.cssselect('div.products-i__datetime'))
    print(tree.cssselect('div.products-i__datetime')[0].text_content().strip())
    return car_info

if __name__ == "__main__":
    #main_bs4()
    #main_lxml(100)
    #get_specific_car_info()
    get_car_info_from_file()
import requests
import time
from bs4 import BeautifulSoup # type: ignore
from lxml import html # type: ignore
import cssselect # type: ignore

INDEX_FILE = "templates/index.html"
CAR_INFO_FILE = "templates/car_info.html"
RESULT_FILE = "templates/result.html"
TEST_FILE = "templates/test.html"
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

def main_lxml():
    url = f"{BASE_URL}/autos"
    print("Fetching with lxml...")
    start = time.time()
    
    response = requests.get(url, headers=HEADERS)
    #print(response.status_code)
    #print(response.text)
    tree = html.fromstring(response.text)
    elements = tree.cssselect('div.products-i.vipped')
    ele = list()
    for el in elements:
        print(el.text_content())
        ele.append(el.text_content())
    end = time.time()
    print(f"lxml time: {end - start:.4f} seconds")
    print(f"Found items: {len(elements)}")
    with open(TEST_FILE, "w", encoding="utf-8") as file:
        file.write(str(ele))
    
def get_specific_car_info(car_id: str):
    car_url = f"{BASE_URL}/autos/{car_id}"
    response = requests.get(car_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())
    with open(CAR_INFO_FILE, "w", encoding="utf-8") as file:
        file.write(soup.prettify())

if __name__ == "__main__":
    main_bs4()
    main_lxml()
    #get_specific_car_info("9453404")

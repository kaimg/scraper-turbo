import requests
import time
import re
import json
from http import HTTPStatus 
from bs4 import BeautifulSoup # type: ignore
from lxml import html # type: ignore
from lxml.etree import tostring
from config import BASE_URL, HEADERS, INDEX_FILE, RESULT_FILE, TEST_FILE, CAR_LIST_FILE, CAR_RESULTS_FILE, CAR_INFO_FILE

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
    #print(car_ids)
    for car_id in car_ids:
        car_url = f"{BASE_URL}/autos/{car_id}"
        response = requests.get(car_url, headers=HEADERS)
        if response.status_code == HTTPStatus.OK:
            tree = html.fromstring(response.text)
            #print(soup.prettify())
            with open(f"{CAR_INFO_FILE}_{car_id}.html", "w", encoding="utf-8") as file:
                file.write(tostring(tree, pretty_print=True, encoding='unicode'))
                print(f"Saved car info for {car_id}")
        else:
            print(f"Failed to fetch car info for {car_id}")

def get_car_info_from_file(car_id: str) -> dict:
    print(f"Getting car info for {car_id}")
    with open(f"{CAR_INFO_FILE}_{car_id}.html", "r", encoding="utf-8") as file:
        print(f"Reading car info for {CAR_INFO_FILE}_{car_id}.html")
        car_info = file.read()
    price_pattern = re.compile(r'([\d\s]+?)\s+([A-Z]{3}|\$|AZN)')

    tree = html.fromstring(car_info)
    print(f"Car info: {tree}")
    properties = tree.cssselect("div.product-properties__i")
    print(f"Properties: {properties}")
    price_elem = tree.cssselect("div.product-price")
    print(f"Price elem: {price_elem}")
    if price_elem:
        price_text = price_elem[0].text_content().strip()
        match = price_pattern.search(price_text)

        if match:
            car_data = {
                "Qiymət": match.group(1).strip(),
                "Valyuta": match.group(2)
            }
        else:
            car_data = {
                "Qiymət": price_text,
                "Valyuta": ""
            }
    else:
        car_data = {
            "Qiymət": "",
            "Valyuta": ""
        }

    properties = tree.cssselect("div.product-properties__i")

    for prop in properties:
        label_elem = prop.cssselect("label.product-properties__i-name")
        value_elem = prop.cssselect("span.product-properties__i-value")

        if label_elem and value_elem:
            label = label_elem[0].text_content().strip()
            value = value_elem[0].text_content().strip()
            car_data[label] = value

    return car_data
    #print(tree.cssselect('div.products-i__price'))
    #print(tree.cssselect('div.product-properties__i')[0].text_content().strip())
    #print(tree.cssselect('label.product-properties__i-name')[0].text_content().strip())
    #print(tree.cssselect('span.product-properties__i-value')[0].text_content().strip())
    #print("\n\n")
    ##print(tree.cssselect('div.products-i__name'))
    #print(tree.cssselect('div.products-i__name')[0].text_content().strip())
    ##print(tree.cssselect('div.products-i__attributes'))
    #print(tree.cssselect('div.products-i__attributes')[0].text_content().strip())
    ##print(tree.cssselect('div.products-i__datetime'))
    #print(tree.cssselect('div.products-i__datetime')[0].text_content().strip())
    #return car_info

def print_car_info(car_info: dict):
    cars = list()
    car_json = json.dumps(car_info, ensure_ascii=False, indent=4)
    print(car_json)
    cars.append(car_json)
    return cars

def write_car_info_to_file(car_info):
    with open(CAR_RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(cars, file, ensure_ascii=False, indent=4)
    print("Successfully wrote car data to JSON file.")


if __name__ == "__main__":
    #main_bs4()
    #main_lxml(100)
    #get_specific_car_info()
    #cars = []
    #for car_id in get_car_list():
    #    if car_id == "9452124":
    #        print("stopped")
    #        break
    #    car_info = get_car_info_from_file(car_id)
    #    car_info["index"] = car_id
    #    #car_json = json.dumps(car_info, ensure_ascii=False, indent=4)
    #    #print(car_json)
    #    cars.append(car_info)
    #
    #write_car_info_to_file(cars)
    print(f"CAR_RESULTS_FILE: {CAR_RESULTS_FILE}")
    #print(f"Cars: {cars}")
    #print(result)
    
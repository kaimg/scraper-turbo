import os

if not os.path.exists("templates"):
    os.makedirs("templates")

INDEX_FILE = "templates/index.html"
CAR_INFO_FILE = "templates/cars/car_info"
RESULT_FILE = "templates/result.html"
TEST_FILE = "templates/car_cleaned.csv"
CAR_LIST_FILE = "templates/car_list.txt"
CAR_CSV_FILE = "templates/car_cleaned.csv"
CAR_RESULTS_FILE = "templates/car_results.json"
BASE_URL = "https://turbo.az/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/ ",
}
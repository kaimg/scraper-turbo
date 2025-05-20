import requests
from bs4 import BeautifulSoup # type: ignore


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = "https://turbo.az/autos"
    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    
    all = soup.find_all('div', 'products-i vipped')
    print(all)
    with open("result.html", "w", encoding="utf-8") as file:
        file.write("\n".join(str(item) for item in all))

def get_specific_car_info(car_id: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    base_car_url = f"https://turbo.az/autos/{car_id}"
    response = requests.get(base_car_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())
    with open("car_info.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

if __name__ == "__main__":
    main()
    get_specific_car_info("9453404")

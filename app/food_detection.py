import requests
from dotenv import dotenv_values


# TODO: API 권한 문제
def detect_with_food_ai(image_url, api_key, api_url):
    print(api_key)
    request_params = {
        "image_url": image_url,
        "num_tag": 10,
        "api_key": api_key,
        "longitude": 127,
        "latitude": 37
    }
    resp = requests.post(api_url, json=request_params)
    print(resp.json())


if __name__ == "__main__":
    cfg = dotenv_values(".env")
    image_url = "https://naeng-bu-test.s3.ap-northeast-2.amazonaws.com/banana.jpeg"
    api_key = cfg["API_KEY"]
    api_url = cfg["API_URL"]

    detect_with_food_ai(image_url, api_key, api_url)

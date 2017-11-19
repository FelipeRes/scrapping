import requests
import time

def download(url, num_retries=10):
    print('Dowloading:', url)
    page = None

    try:
        response = requests.get(url)
        print(response.status_code)
        page = response.text
        if response.status_code >= 400:
            print('Download error:', response.text)
            time.sleep(30)
            print("Tenta de novo: " +str(num_retries))
            if num_retries != 0:
                return download(url, num_retries -1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e)
    return page

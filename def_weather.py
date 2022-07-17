from bs4 import BeautifulSoup
import requests
from voice_assistant import speak

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def weather(city):
    try:
        res = requests.get(
            f'https://www.google.com/search?q=weather+{city}&oq=weather+{city}&aqs=chrome.0.69i59.5434j1j9&sourceid=chrome&ie=UTF-8',
            headers=headers)
        print("Searching...\n")
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('#wob_loc')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()

        return location,info,weather

    except IndexError:
        speak ('Cant find such a city')


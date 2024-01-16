import requests
import os
from dotenv import load_dotenv

url = "https://semadb.p.rapidapi.com/collections"

load_dotenv()

RAPID_API_KEY = os.getenv('RAPID_API_KEY')
RAPID_API_HOST = os.getenv('RAPID_API_HOST')

print(RAPID_API_KEY)
print(RAPID_API_HOST)
headers = {
    "X-RapidAPI-Key": f"{RAPID_API_KEY}",
    "X-RapidAPI-Host": f"{RAPID_API_HOST}"
}

response = requests.get(url, headers=headers)

print(response.json())
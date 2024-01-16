import requests

url = "https://semadb.p.rapidapi.com/collections"

print("${RAPID_API_KEY}")
headers = {
    "X-RapidAPI-Key": "${RAPID_API_KEY}",
    "X-RapidAPI-Host": "${RAPID_API_HOST}"
}

response = requests.get(url, headers=headers)

print(response.json())
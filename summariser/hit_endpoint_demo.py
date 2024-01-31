import requests
import json

# URL of the Flask endpoint
url = "http://127.0.0.1:5000/summariser"

# Data to be sent in the request body
data = {"text": "hello world! this is a test."}

# Convert data to JSON format
json_data = json.dumps(data)

# Set headers
headers = {"Content-Type": "application/json"}

# Make the POST request
response = requests.post(url, data=json_data, headers=headers)

# Check the response
if response.status_code == 200:
    summary = response.json()["summary"]
    embedding = response.json()["embedding"]
    print(f"Summary: {summary}")
    print(f"Embedding: {embedding}")
else:
    print(f"Error: {response.status_code}, {response.json()}")

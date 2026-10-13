import requests

CLIENT_ID = "1000.LWPLVIXDQAP5U0VEHZV60GZXAWWHKI"
CLIENT_SECRET = "6f5f9cf51f59199dbc983d056e7573db0e4d3b928b"

# After OAuth setup, put your refresh token here
AUTHORIZATION_CODE = "1000.e308b86d71d61f198611c6af69550538.b8796d737296e9e13bcfd54ef6cdc22f"

url = "https://accounts.zoho.eu/oauth/v2/token"

params = {
    "code": AUTHORIZATION_CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "authorization_code",
}

response = requests.post(url, params=params)

print("Status:", response.status_code)
print("Response:", response.json())
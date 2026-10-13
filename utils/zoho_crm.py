import requests
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

CLIENT_ID = "1000.LWPLVIXDQAP5U0VEHZV60GZXAWWHKI"
CLIENT_SECRET = "6f5f9cf51f59199dbc983d056e7573db0e4d3b928b"

# After OAuth setup, put your refresh token here
REFRESH_TOKEN = "1000.6bef0ef55da33f4e37cabb59d7a9fe09.0bbe94100e38bee96d066f12022edd01"

# India Zoho DC
ACCOUNTS_URL = "https://accounts.zoho.eu"
API_DOMAIN = "https://www.zohoapis.eu"

API_VERSION = "v8"


# ============================================================
# AUTHENTICATION
# ============================================================

def get_access_token():

    url = f"{ACCOUNTS_URL}/oauth/v2/token"

    data = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        raise Exception(
            f"Zoho authentication failed: "
            f"{response.status_code} - {response.text}"
        )

    result = response.json()

    if "access_token" not in result:
        raise Exception(f"Zoho token generation failed: {result}")

    print("OAuth successful")
    print("API domain:", result.get("api_domain"))
    print("Token type:", result.get("token_type"))
    print("Expires in:", result.get("expires_in"))

    return result["access_token"], result["api_domain"]

# def get_access_token():

#     url = f"{ACCOUNTS_URL}/oauth/v2/token"

#     data = {
#         "refresh_token": REFRESH_TOKEN,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "grant_type": "refresh_token",
#     }

#     response = requests.post(url, data=data)

#     print("Zoho OAuth status:", response.status_code)
#     print("Zoho OAuth response:", response.json())

#     if response.status_code != 200:
#         raise Exception(
#             f"Zoho authentication failed: "
#             f"{response.status_code} - {response.text}"
#         )

#     result = response.json()

#     if "access_token" not in result:
#         raise Exception(
#             f"Zoho token generation failed: {result}"
#         )

#     return result["access_token"], result.get("api_domain")

def zoho_get(endpoint, params=None):

    access_token, api_domain = get_access_token()

    if not api_domain:
        api_domain = API_DOMAIN

    url = f"{api_domain}/crm/{API_VERSION}/{endpoint}"

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(
            f"Zoho API error: "
            f"{response.status_code} - {response.text}"
        )

    return response.json()

# def get_access_token():

#     url = f"{ACCOUNTS_URL}/oauth/v2/token"

#     params = {
#         "refresh_token": REFRESH_TOKEN,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "grant_type": "refresh_token"
#     }

#     response = requests.post(url, params=params)

#     if response.status_code != 200:
#         raise Exception(
#             f"Zoho authentication failed: "
#             f"{response.status_code} - {response.text}"
#         )

#     data = response.json()
    

#     print("ZOHO TOKEN RESPONSE:")
#     print(data)

#     if "access_token" not in data:
#         raise Exception(f"Zoho token generation failed: {data}")

#     return data["access_token"], data.get("api_domain", API_DOMAIN)



# ============================================================
# GENERIC API REQUEST
# ============================================================


# ============================================================
# SALES / DEALS
# ============================================================

def get_deals():

    fields = [
        "id",
        "Deal_Name",
        "Account_Name",
        "Stage",
        "Pipeline",
        "Amount",
        "Probability",
        "Closing_Date",
        "Type",
        "Lead_Source",
        "Owner",
        "Created_Time",
        "Modified_Time"
    ]

    params = {
        "fields": ",".join(fields),
        "per_page": 200
    }

    response = zoho_get("Deals", params)

    records = response.get("data", [])

    return pd.json_normalize(records)


# ============================================================
# ACCOUNTS
# ============================================================

def get_accounts():

    fields = [
        "id",
        "Account_Name",
        "Industry",
        "Annual_Revenue",
        "Owner",
        "Created_Time",
        "Modified_Time"
    ]

    params = {
        "fields": ",".join(fields),
        "per_page": 200
    }

    response = zoho_get("Accounts", params)

    records = response.get("data", [])

    return pd.json_normalize(records)


# ============================================================
# CONTACTS
# ============================================================

def get_contacts():

    fields = [
        "id",
        "Full_Name",
        "Email",
        "Phone",
        "Account_Name",
        "Owner",
        "Created_Time"
    ]

    params = {
        "fields": ",".join(fields),
        "per_page": 200
    }

    response = zoho_get("Contacts", params)

    records = response.get("data", [])

    return pd.json_normalize(records)

def get_sales_pipeline():
    """
    Fetch Deals from Zoho CRM for the Sales / Pre-Sales pipeline.
    """

    fields = [
        "id",
        "Deal_Name",
        "Account_Name",
        "Stage",
        "Pipeline",
        "Amount",
        "Probability",
        "Closing_Date",
        "Type",
        "Lead_Source",
        "Owner",
        "Created_Time",
        "Modified_Time",
    ]

    params = {
        "fields": ",".join(fields),
        "per_page": 200,
    }

    response = zoho_get("Deals", params)

    records = response.get("data", [])

    if not records:
        return pd.DataFrame()

    df = pd.json_normalize(records)

    # Flatten Zoho lookup fields
    if "Account_Name.name" in df.columns:
        df["Account_Name"] = df["Account_Name.name"]

    if "Owner.name" in df.columns:
        df["Owner"] = df["Owner.name"]

    return df

def get_sales_summary():

    df = get_sales_pipeline()

    if df.empty:
        return {
            "opportunities": 0,
            "pipeline_value": 0,
            "weighted_pipeline": 0,
        }

    df["Amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    ).fillna(0)

    df["Probability"] = pd.to_numeric(
        df["Probability"],
        errors="coerce"
    ).fillna(0)

    return {
        "opportunities": len(df),
        "pipeline_value": df["Amount"].sum(),
        "weighted_pipeline": (
            df["Amount"] * df["Probability"] / 100
        ).sum(),
    }
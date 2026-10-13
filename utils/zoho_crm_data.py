import requests
import pandas as pd
import time

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

_access_token = None
_token_expiry = 0
_api_domain = None

# def get_access_token():

#     url = f"{ACCOUNTS_URL}/oauth/v2/token"

#     data = {
#         "refresh_token": REFRESH_TOKEN,
#         "client_id": CLIENT_ID,
#         "client_secret": CLIENT_SECRET,
#         "grant_type": "refresh_token",
#     }

#     response = requests.post(url, data=data)

#     if response.status_code != 200:
#         raise Exception(
#             f"Zoho authentication failed: "
#             f"{response.status_code} - {response.text}"
#         )

#     result = response.json()

#     if "access_token" not in result:
#         raise Exception(f"Zoho token generation failed: {result}")

#     print("OAuth successful")
#     print("API domain:", result.get("api_domain"))
#     print("Token type:", result.get("token_type"))
#     print("Expires in:", result.get("expires_in"))

#     return result["access_token"], result["api_domain"]

def get_access_token():

    global _access_token
    global _token_expiry
    global _api_domain

    # Reuse token while it is still valid
    if (
        _access_token is not None
        and time.time() < _token_expiry
    ):
        return _access_token, _api_domain

    url = f"{ACCOUNTS_URL}/oauth/v2/token"

    data = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
    }

    response = requests.post(
        url,
        data=data,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"Zoho authentication failed: "
            f"{response.status_code} - {response.text}"
        )

    result = response.json()

    if "access_token" not in result:
        raise Exception(
            f"Zoho token generation failed: {result}"
        )

    _access_token = result["access_token"]

    _api_domain = result.get(
        "api_domain",
        API_DOMAIN
    )

    # Refresh 2 minutes before expiry
    expires_in = result.get("expires_in", 3600)

    _token_expiry = (
        time.time()
        + expires_in
        - 120
    )

    return _access_token, _api_domain


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


# ============================================================
# DATabricks LEADS
# ============================================================

def get_databricks_leads():

    fields = [
        "id",
        "Full_Name",
        "Company",
        "Email",
        "Phone",
        "Solution Title",
        "Lead_Status",
        "Lead_Source",
        "Owner",
        "Created_Time",
        "Modified_Time",
        "Converted_Account",
        "Converted_Deal",
    ]

    params = {
        "fields": ",".join(fields),
        "per_page": 200,
    }

    response = zoho_get("Leads", params)

    records = response.get("data", [])

    if not records:
        return pd.DataFrame()

    df = pd.json_normalize(records)

    # Flatten lookup fields
    for column in [
        "Owner.name",
        "Converted_Account.name",
        "Converted_Deal.name",
    ]:
        if column in df.columns:
            base_column = column.replace(".name", "")
            df[base_column] = df[column]

    return df


# ============================================================
# DATABRICKS DEALS
# ============================================================

def get_databricks_deals():

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
        "Partner Solution",
        "Practice",
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

    # Flatten lookup fields
    if "Account_Name.name" in df.columns:
        df["Account_Name"] = df["Account_Name.name"]

    if "Owner.name" in df.columns:
        df["Owner"] = df["Owner.name"]

    return df


# ============================================================
# FILTER DATabricks LEADS - Solution Title having - Databricks
# ============================================================

def filter_databricks_leads(df): #--test -

    # if df.empty or "Solution Title" not in df.columns:
    #     return pd.DataFrame()

    return df 
    #    df[
    #     df["Solution Title"]
    #     .fillna("")
    #     .astype(str)
    #     .str.contains(
    #         "Databricks",
    #         case=False,
    #         na=False
    #     )
    # ].copy()


# ============================================================
# FILTER DATABRICKS DEALS - Partner Solution + Practice
# ============================================================

def filter_databricks_deals(df):

    if df.empty or "Practice" not in df.columns:
        return pd.DataFrame()

    practice = (
        df["Practice"]
        .fillna("")
        .astype(str)
    )

    mask = (
        practice.str.contains(
            "Data & AI",
            case=False,
            na=False
        )
        |
        # "Partner Solution".str.contains(
        #             "Databricks",
        #             case=False,
        #             na=False
        #         )
                
        # |
        practice.str.contains(
            "Databricks",
            case=False,
            na=False
        )
    )

    return df[mask].copy()


# ============================================================
# DATABRICKS SALES DATA
# ============================================================

def get_databricks_sales():

    leads = get_databricks_leads()
    deals = get_databricks_deals()

    leads = filter_databricks_leads(leads)
    deals = filter_databricks_deals(deals)

    return {
        "leads": leads,
        "deals": deals,
    }


# ============================================================
# ACCOUNTS
# ============================================================

def get_accounts():

    fields = [
        "id",
        "Account_Name",
        "Account Origin",
        "Industry",
        "Annual_Revenue",
        "Phone",
        "Website",
        "Billing_City",
        "Billing_State",
        "Billing_Country",
        "Owner",
        "Created_Time",
        "Modified_Time",
    ]

    params = {
        "fields": ",".join(fields),
        "per_page": 200,
    }

    response = zoho_get("Accounts", params)

    records = response.get("data", [])

    if not records:
        return pd.DataFrame()

    df = pd.json_normalize(records)

    if "Owner.name" in df.columns:
        df["Owner"] = df["Owner.name"]

    return df


# ============================================================
# ACCOUNTS ASSOCIATED WITH DATABRICKS LEADS + DEALS
# ============================================================

def get_databricks_accounts():

    accounts = get_accounts()

    if accounts.empty:
        return pd.DataFrame()

    leads = get_databricks_leads()
    deals = get_databricks_deals()

    leads = filter_databricks_leads(leads)
    deals = filter_databricks_deals(deals)

    account_ids = set()

    # --------------------------------------------------------
    # Accounts from Deals
    # --------------------------------------------------------

    if not deals.empty and "Account_Name.id" in deals.columns:

        deal_account_ids = (
            deals["Account_Name.id"]
            .dropna()
            .astype(str)
            .tolist()
        )

        account_ids.update(deal_account_ids)

    # --------------------------------------------------------
    # Accounts from converted Leads
    # --------------------------------------------------------

    if not leads.empty and "Converted_Account.id" in leads.columns:

        lead_account_ids = (
            leads["Converted_Account.id"]
            .dropna()
            .astype(str)
            .tolist()
        )

        account_ids.update(lead_account_ids)

    if not account_ids:
        return pd.DataFrame()

    accounts["id"] = accounts["id"].astype(str)

    return accounts[
        accounts["id"].isin(account_ids)
    ].copy()


# ============================================================
# SALES SUMMARY
# ============================================================

def get_sales_summary():

    sales = get_databricks_sales()

    leads = sales["leads"]
    deals = sales["deals"]

    pipeline_value = 0
    weighted_pipeline = 0

    if not deals.empty:

        deals["Amount"] = pd.to_numeric(
            deals["Amount"],
            errors="coerce"
        ).fillna(0)

        deals["Probability"] = pd.to_numeric(
            deals["Probability"],
            errors="coerce"
        ).fillna(0)

        pipeline_value = deals["Amount"].sum()

        weighted_pipeline = (
            deals["Amount"]
            * deals["Probability"]
            / 100
        ).sum()

    return {
        "leads": len(leads),
        "deals": len(deals),
        "pipeline_value": pipeline_value,
        "weighted_pipeline": weighted_pipeline,
    }

#------GET SOLUTIONS containing 'Databricks' and add to deals and leads if not found in orig datafram---#

def get_solutions():

    fields = [
        "id",
        "Solution Title",
        "Description",
        "Status",
        "Created_Time",
        "Modified_Time",
    ]

    params = {
        "fields": ",".join(fields),
        "per_page": 200,
    }

    response = zoho_get("Solutions", params)

    records = response.get("data", [])

    if not records:
        return pd.DataFrame()

    return pd.json_normalize(records)


#---join solutions to others to get full picture
def get_databricks_sales_with_solutions():

    sales = get_databricks_sales()

    leads = sales["leads"]
    deals = sales["deals"]

    solutions = get_solutions()

    # Add solution-derived leads/deals if they aren't already present
    # TODO: map the actual Solution → Lead/Deal fields once confirmed

    return {
        "leads": leads,
        "deals": deals,
        "solutions": solutions,
    }
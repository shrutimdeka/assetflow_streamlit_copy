import requests
import pandas as pd
import time
import streamlit as st

from utils.config import (
    ZOHO_CLIENT_ID,
    ZOHO_CLIENT_SECRET,
    ZOHO_REFRESH_TOKEN,
    ZOHO_API_DOMAIN,
    ZOHO_ACCOUNTS_URL,
    validate_config,
)

# ============================================================
# CONFIGURATION
# ============================================================

CLIENT_ID = ZOHO_CLIENT_ID
CLIENT_SECRET = ZOHO_CLIENT_SECRET

# After OAuth setup, put your refresh token here
REFRESH_TOKEN = ZOHO_REFRESH_TOKEN

# India Zoho DC
ACCOUNTS_URL = ZOHO_ACCOUNTS_URL
API_DOMAIN = ZOHO_API_DOMAIN

API_VERSION = "v8"


# ============================================================
# AUTHENTICATION
# ============================================================

_access_token = None
_token_expiry = 0
_api_domain = None

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
        timeout=3500
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

#-------------------------------- tables----------------------------------------#
@st.cache_data(ttl=3500)
def get_databricks_leads():

    fields = [
        "id",
        "Full_Name",
        "Company",
        "Email",
        "Phone",
        "Solution",
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

    # Flatten useful lookup fields
    if "Owner.name" in df.columns:
        df["Owner"] = df["Owner.name"]

    if "Converted_Account.name" in df.columns:
        df["Converted_Account"] = df["Converted_Account.name"]

    if "Converted_Deal.name" in df.columns:
        df["Converted_Deal"] = df["Converted_Deal.name"]

    # ORIGINAL FILTER:
    # Solution contains Databricks
    if "Solution" in df.columns:
        df = df[
            df["Solution"]
            .fillna("")
            .astype(str)
            .str.contains(
                "Databricks",
                case=False,
                na=False
            )
        ].copy()

    return df

@st.cache_data(ttl=3500)
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

    # Flatten useful lookup fields
    if "Account_Name.name" in df.columns:
        df["Account_Name"] = df["Account_Name.name"]

    if "Owner.name" in df.columns:
        df["Owner"] = df["Owner.name"]

    # ORIGINAL FILTER:
    # Practice contains Data & AI OR Databricks
    if "Practice" in df.columns:

        practice = (
            df["Practice"]
            .fillna("")
            .astype(str)
        )

        df = df[
            practice.str.contains(
                "Data & AI",
                case=False,
                na=False
            )
            |
            practice.str.contains(
                "Databricks",
                case=False,
                na=False
            )
        ].copy()

    return df

@st.cache_data(ttl=3500)
def get_databricks_solutions():

    fields = [
        "id",
        "Solution_Title",
        "Description",
        "Status",
        "Created_Time",
        "Modified_Time",
    ]

    params = {
        "fields": ",".join(fields),
        "per_page": 200,
    }

    response = zoho_get(
        "Solutions",
        params
    )

    records = response.get("data", [])

    if not records:
        return pd.DataFrame()

    df = pd.json_normalize(records)

    if "Solution_Title" in df.columns:

        df = df[
            df["Solution_Title"]
            .fillna("")
            .astype(str)
            .str.contains(
                "Databricks",
                case=False,
                na=False
            )
        ].copy()

    return df

#-----Get solutions list---------------#
# ============================================================
# GET FULL SOLUTION RECORD
# ============================================================
@st.cache_data(ttl=3500)
def get_solution(solution_number): #--number based on where Databricks is mentioned as solution

    response = zoho_get(
        f"Solutions/{solution_number}"
    )

    return response

# ============================================================
# GET LEADS + DEALS FROM DATABRICKS SOLUTIONS
# ============================================================

@st.cache_data(ttl=3500)
def get_solution_associations():

    solutions = get_databricks_solutions()

    all_leads = []
    all_deals = []

    if solutions.empty:
        return (
            pd.DataFrame(),
            pd.DataFrame()
        )

    for _, solution in solutions.iterrows():

        # Use Solution Number from the filtered dataframe
        solution_number = solution["id"]

        solution_title = solution["Solution_Title"]

        # ----------------------------------------------------
        # Get the complete Solution record
        # ----------------------------------------------------

        solution_data = get_solution(
            solution_number
        )

        # ----------------------------------------------------
        # Inspect the returned lists
        # ----------------------------------------------------

        # Temporary debugging
        print(
            f"\nSolution: {solution_title}"
        )

        print(
            "Solution response keys:",
            solution_data.keys()
        )

        # ----------------------------------------------------
        # Leads
        # ----------------------------------------------------

        associated_leads = solution_data.get(
            "Associated_Leads",
            []
        )

        if associated_leads:

            leads_df = pd.json_normalize(
                associated_leads
            )

            leads_df["id"] = (
                solution_number
            )

            leads_df["Solution_Title"] = (
                solution_title
            )

            all_leads.append(
                leads_df
            )

        # ----------------------------------------------------
        # Deals
        # ----------------------------------------------------

        associated_deals = solution_data.get(
            "Associated_Deals",
            []
        )

        if associated_deals:

            deals_df = pd.json_normalize(
                associated_deals
            )

            deals_df["id"] = (
                solution_number
            )

            deals_df["Solution_Title"] = (
                solution_title
            )

            all_deals.append(
                deals_df
            )

    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------

    leads_df = (
        pd.concat(
            all_leads,
            ignore_index=True
        )
        if all_leads
        else pd.DataFrame()
    )

    deals_df = (
        pd.concat(
            all_deals,
            ignore_index=True
        )
        if all_deals
        else pd.DataFrame()
    )

    return leads_df, deals_df

@st.cache_data(ttl=3500)
def get_solution_comparison():

    # Original filtered tables
    original_leads = get_databricks_leads()
    original_deals = get_databricks_deals()

    # Records associated with Databricks Solutions
    solution_leads, solution_deals = (
        get_solution_associations()
    )

    # -----------------------------------------
    # Leads found through Solutions but missing
    # from original Leads table
    # -----------------------------------------

    if (
        not solution_leads.empty
        and not original_leads.empty
    ):

        original_lead_ids = set(
            original_leads["id"]
            .astype(str)
        )

        missing_leads = solution_leads[
            ~solution_leads["id"]
            .astype(str)
            .isin(original_lead_ids)
        ].copy()

    elif not solution_leads.empty:

        missing_leads = solution_leads.copy()

    else:

        missing_leads = pd.DataFrame()

    # -----------------------------------------
    # Deals found through Solutions but missing
    # from original Deals table
    # -----------------------------------------

    if (
        not solution_deals.empty
        and not original_deals.empty
    ):

        original_deal_ids = set(
            original_deals["id"]
            .astype(str)
        )

        missing_deals = solution_deals[
            ~solution_deals["id"]
            .astype(str)
            .isin(original_deal_ids)
        ].copy()

    elif not solution_deals.empty:

        missing_deals = solution_deals.copy()

    else:

        missing_deals = pd.DataFrame()

    return {
        "missing_leads": missing_leads,
        "missing_deals": missing_deals,
    }


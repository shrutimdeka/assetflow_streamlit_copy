import pandas as pd

def assets():
    return pd.DataFrame(
        [
        [
            "Value Chain Command Centre App",
            "Accelerator App",
            "Value Chain Command Center is a foundational Connected Intelligence solution designed to operationalize enterprise command and control across the value chain. It connects unified data and analytics, process intelligence, and embedded AI into a single operating layer that sits above domain Control Towers.",
            "Streamlit",
            "images/streamlit icon.png",
            "Accelerator",
            "https://commandcenterapp-4304158276012576.16.azure.databricksapps.com/"
        ],
        [
            "Operations Control Tower App",
            "Accelerator App",
            "Operations Tower application is the lightweight Command Center for only Operations. This is an accelerator for businesses that want to focus on Operations Control Tower.",
            "Streamlit",
            "images/streamlit icon.png",
            "Accelerator",
            "https://operationtower-4304158276012576.16.azure.databricksapps.com"
        ],
        [
            "Early Warning AI Monitoring Solution",
            "Demo Asset",
            "Predictive & prescriptive AI solution for shopfloor machines. It combines Alarm code manual and Litmus sensor data to provide prescriptive diagnosis before event (alarm) occurs.",
            "AI/BI",
            "images/aibi icon.png",
            "Demo Asset",
            "https://dbc-57514f5c-cfc4.cloud.databricks.com/dashboardsv3/01f138d670fa1358a7ca6060f4a0214c/published?o=7474655163446050"
        ],
        [
            "Supply Chain Inventory Planning Copilot",
            "Demo Asset",
            "A Genie-based supply chain inventory planning copilot which answers complex questions regarding inventory, distribution, work order and fulfilling SLAs and root cause analyses.",
            "Genie Agent",
            "images/genie icon.png",
            "Demo Asset",
            "https://dbc-57514f5c-cfc4.cloud.databricks.com/genie/rooms/01f16a4c29711a7894eccb66d4bf8ebd?o=7474655163446050"
        ],
        [
            "Value Chain Command Center Dashboard",
            "Accelerator Dashboard",
            "Value chain Command Center in the AI/BI dashboard version - for those who want the solution in native Databricks Dashboard format.",
            "AI/BI",
            "images/aibi icon.png",
            "Accelerator",
            "https://adb-4304158276012576.16.azuredatabricks.net/dashboardsv3/01f14ad81673105292c300bed704d4ff/published?o=4304158276012576"
        ],
        [
            "ML Model Monitoring Dashboard",
            "Accelerator Dashboard",
            "It is a demo and accelerator asset to showcase ML model monitoring for both LLM-based and classical ML-based solutions. This can be customised as needed. Currently used on the Command Center.",
            "AI/BI",
            "images/aibi icon.png",
            "Accelerator",
            "https://adb-4304158276012576.16.azuredatabricks.net/dashboardsv3/01f173984d4d12f69828fd6826f30f9d/published?o=4304158276012576"
        ],
        [
            "PLM Insights Dashboard",
            "Demo Asset",
            "Product lifecycle management insights dashboard used to discover objects in Oracle PLM, aiding in migration planning and execution.",
            "AI/BI",
            "images/aibi icon.png",
            "Demo Asset",
            "https://adb-4304158276012576.16.azuredatabricks.net/dashboardsv3/01f14205315d1009a54c203e9d1bc9ad/published?o=4304158276012576"
        ],
        [
            "LinkedIn Marketing Blogs",
            "Blog",
            "LinkedIn use cases and blog tracker for more asset discovery and knowledge base.",
            "Document",
            "images/excel icon.png",
           "Blog",
            "https://inspirenext.sharepoint.com/:x:/r/sites/DataAIPractice/_layouts/15/Doc.aspx?sourcedoc=%7B2A865545-8C74-4485-93DE-54F92A631F96%7D&file=LinkedIn%20Use%20Cases%20%26%20Blog%20Tracker.xlsx=&action=default&mobileredirect=true"
        ],
    ]
    , columns=[
        "Name",
        "Category",
        "Description",
        "Technology",
        "Images",
        "Type",
        "URL"
    ])
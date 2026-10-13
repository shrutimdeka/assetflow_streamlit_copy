# AssetFlow — Streamlit starter

A lightweight, modular Streamlit implementation inspired by the supplied AssetFlow wireframe.

## Current priority

- HOME landing page
- Executive Dashboard
- **Sales Pipeline / Pre-Sales**
- Project Tracking placeholder
- **Asset Repository**
- Backend Sync placeholder

## Run locally

```bash
cd assetflow_streamlit
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Structure

```text
assetflow_streamlit/
├── app.py
├── requirements.txt
├── README.md
├── pages/
│   ├── 1_Executive_Dashboard.py
│   ├── 2_Sales_Pipeline.py
│   ├── 3_Project_Tracking.py
│   ├── 4_Asset_Repository.py
│   └── 5_Backend_Sync.py
└── utils/
    ├── data.py
    └── styles.py
```

## Where to connect real data

`utils/data.py` contains the demo data. Replace those functions with:
- Databricks SQL queries
- Unity Catalog tables
- REST/API calls
- CSV/Excel ingestion

The UI pages do not need to change.

## Important

The sidebar navigation is Streamlit's native multipage navigation. Each section is a separate Python page, so new functionality can be added independently.

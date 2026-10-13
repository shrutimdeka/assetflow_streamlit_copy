import streamlit as st

def apply_global_styles():
    st.markdown(
        """
        <style>
        /* ---------- App ---------- */
        .stApp {
            background: #f7f9fc;
        }

        [data-testid="stHeader"] {
            background: #f7f9fc;
        }

        .block-container {
            padding-top: 1.7rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #dce3ed;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 4px 14px 4px;
        }

        .brand-mark, .home-mark {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            border-radius: 7px;
            background: #1455d9;
            color: white;
            font-weight: 700;
        }

        .brand-name {
            color: #152238;
            font-size: 1.05rem;
            font-weight: 700;
        }

        .brand-subtitle {
            color: #7b8798;
            font-size: 0.68rem;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        .sidebar-hint {
            color: #8b96a7;
            font-size: .72rem;
            line-height: 1.4;
            padding: 4px 5px;
        }

        /* ---------- Typography ---------- */
        h1, h2, h3 {
            color: #182437 !important;
            letter-spacing: -.02em;
        }

        .eyebrow {
            color: #7a8798;
            text-transform: uppercase;
            letter-spacing: .11em;
            font-size: .68rem;
            font-weight: 700;
            margin-bottom: .2rem;
        }

        .page-title {
            font-size: 1.75rem;
            font-weight: 700;
            margin: 0 0 .2rem 0;
        }

        .page-description {
            color: #778396;
            font-size: .88rem;
            margin-bottom: 1.25rem;
        }

        /* ---------- Cards ---------- */
        
        .metric-card {
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e4c7e8;
            background: linear-gradient(135deg, #f8e9f7, #eee7fb);
            box-sizing: border-box;
            min-height: 105px;
        }

        .metric-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #76577f;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .metric-value {
            margin-top: 8px;
            font-size: 2rem;
            font-weight: 700;
            color: #54245f;
        }

        .metric-delta {
            color: #16a36a;
            font-size: .72rem;
            margin-top: 7px;
        }

        .panel {
            background: #fff;
            border: 1px solid #e0e6ee;
            border-radius: 8px;
            padding: 17px;
        }

        .panel-title {
            color: #263449;
            font-size: .76rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            font-weight: 700;
            margin-bottom: 12px;
        }

        /* ============================================================
   ASSET REPOSITORY
   ============================================================ */

/* Main asset widget */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    border: 1px solid #dde3ec !important;
    background: #ffffff !important;
    overflow: hidden !important;
}

/* Keep the inside of the card white */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: #ffffff !important;
}


/* ---------- Asset Header ---------- */

.asset-header {
    padding-top: 8px;
}

.asset-type {
    color: #7650a3;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.asset-name {
    color: #263449;
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.35;
}


/* ---------- Description ---------- */

.asset-description {
    color: #687587;
    font-size: 0.82rem;
    line-height: 1.55;

    min-height: 52px;
    margin-top: 14px;
    margin-bottom: 12px;

    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}


/* ---------- Technology ---------- */

.asset-technology {
    color: #8b96a7;
    font-size: 0.7rem;
    font-weight: 500;

    min-height: 22px;
    padding-top: 9px;

    border-top: 1px solid #edf0f4;
    margin-bottom: 12px;
}


/* ---------- Asset Icon ---------- */

/* Prevent Streamlit from adding unnecessary spacing */
div[data-testid="stImage"] {
    margin-bottom: 0;
}

/* Make asset images sit neatly in their column */
div[data-testid="stImage"] img {
    border-radius: 12px;
}
        
        #--new
        /* ---------- Asset Repository ---------- */

/* Outer asset widget */
.asset-widget {
    height: 365px;
    min-height: 365px;
    max-height: 365px;

    display: flex;
    flex-direction: column;

    border: 1px solid #d9dee7;
    border-radius: 10px;
    background: #ffffff;

    overflow: hidden;
    box-sizing: border-box;
}

/* Image area */
.asset-thumb {
    height: 80px;
    min-height: 800px;
    max-height: 120px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #f8fafc;
    border-bottom: 1px solid #e2e7ef;

    overflow: hidden;
    box-sizing: border-box;
}

.asset-thumb img {
    width: 100%;
    height: 80px;
    object-fit: contain;
    display: block;
}

/* Information area */
.asset-card {
    height: 180px;
    min-height: 180px;
    max-height: 205px;

    padding: 16px;

    box-sizing: border-box;
    background: #ffffff;

    overflow: hidden;
}

/* Asset type */
.asset-type {
    height: 18px;
    min-height: 18px;

    color: #1455d9;
    font-size: .61rem;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-weight: 700;

    overflow: hidden;
}

/* Asset name */
.asset-name {
    height: 44px;
    min-height: 44px;

    color: #243248;
    font-size: .9rem;
    font-weight: 700;

    margin-top: 5px;

    line-height: 1.35;

    overflow: hidden;

    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

/* Description */
.asset-description {
    height: 48px;
    min-height: 48px;

    color: #667386;
    font-size: .75rem;
    line-height: 1.45;

    margin-top: 8px;

    overflow: hidden;

    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

/* Technology */
.asset-technology {
    height: 25px;
    min-height: 25px;

    margin-top: 10px;

    color: #8b96a7;
    font-size: .65rem;

    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}


/* ---------- Streamlit image ---------- */

div[data-testid="stImage"] {
    height: 120px !important;
    min-height: 120px !important;
    max-height: 120px !important;

    margin: 0 !important;
    padding: 0 !important;

    overflow: hidden;
}

div[data-testid="stImage"] img {
    width: 100% !important;
    height: 120px !important;
    min-height: 120px !important;
    max-height: 120px !important;

    object-fit: contain;

    display: block;

    border: 0 !important;
}


/* ---------- View button ---------- */

div[data-testid="stLinkButton"] {
    height: 40px !important;
    min-height: 40px !important;
    max-height: 40px !important;

    margin: 0 !important;
    padding: 0 !important;

    width: 100% !important;
}

div[data-testid="stLinkButton"] a {
    width: 100% !important;
    height: 40px !important;

    min-height: 40px !important;

    display: flex !important;
    align-items: center;
    justify-content: center;

    box-sizing: border-box;

    border: 0 !important;
    border-top: 1px solid #d9dee7 !important;

    border-radius: 0 0 10px 10px !important;

    font-size: .75rem;
    font-weight: 600;
}
        #---
    
        # .asset-card {
        #     height: 300px;
        #     padding: 18px;
        #     border: 1px solid #cfd6e2;
        #     border-radius: 12px;
        #     box-sizing: border-box;
        #     overflow: hidden;
        #     background: white;
        # }

        # .asset-thumb {
        #     height: 80px;
        #     border-radius: 5px;
        #     background: linear-gradient(135deg, #eef3fa, #dfe7f3);
        #     display: flex;
        #     align-items: center;
        #     justify-content: center;
        #     color: #54709b;
        #     font-size: 1.5rem;
        #     margin-bottom: 12px;
        # }

        # .asset-type {
        #     color: #1455d9;
        #     font-size: .61rem;
        #     text-transform: uppercase;
        #     letter-spacing: .08em;
        #     font-weight: 700;
        # }

        # .asset-name {
        #     color: #243248;
        #     font-size: .9rem;
        #     font-weight: 700;
        #     margin-top: 4px;
        # }

        # .asset-description {
        #     height: 90px;
        #     overflow: hidden;
        #     display: -webkit-box;
        #     -webkit-line-clamp: 2;
        #     -webkit-box-orient: vertical;
        # }

        .status-pill {
            display: inline-block;
            border-radius: 10px;
            padding: 3px 8px;
            font-size: .62rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .status-green { background:#e4f7ed; color:#118353; }
        .status-yellow { background:#fff4d6; color:#a26a00; }
        .status-blue { background:#e8efff; color:#315db8; }
        .status-grey { background:#eef1f5; color:#68758a; }

        /* ---------- Home ---------- */
        .home-wrap {
            min-height: 72vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .home-mark {
            width: 54px;
            height: 54px;
            font-size: 1.25rem;
            margin-bottom: 16px;
        }

        .home-wrap h1 {
            font-size: 2.4rem;
            margin-bottom: 8px;
        }

        .home-tagline {
            max-width: 650px;
            color: #778396;
            line-height: 1.7;
        }

        .home-note {
            margin-top: 18px;
            color: #9aa4b3;
            font-size: .78rem;
        }

        /* Streamlit widgets */
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #e0e6ee;
            border-radius: 8px;
            padding: 10px 14px;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #e0e6ee;
            border-radius: 8px;
            overflow: hidden;
        }

        .stButton button {
            border-radius: 5px;
            font-size: .78rem;
        }

        @media (max-width: 900px) {
            .block-container { padding-left: 1rem; padding-right: 1rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

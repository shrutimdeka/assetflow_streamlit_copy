import streamlit as st
from utils.styles import apply_global_styles

apply_global_styles()

from utils.zoho_crm_data_dup import (
    get_databricks_leads,
    get_databricks_deals,
    get_solution_associations,
)

with st.sidebar:

    # existing logo/navigation code
    ...

    st.divider()

    if st.button(
        "↻ Refresh CRM Data",
        use_container_width=True
    ):
        get_databricks_leads.clear()
        get_databricks_deals.clear()
        get_solution_associations.clear()

        st.rerun()
# ============================================================
# HOME PAGE STYLES
# ============================================================

st.markdown(
    """
    <style>

    /* Style the bordered container used as the home banner */
    /* ---------- Home Banner Box ---------- */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
    border: 1px solid #e6d8f0 !important;
    overflow: hidden !important;

    background: linear-gradient(
        135deg,
        #faf7fd 0%,
        #f4edfa 48%,
        #fff5f6 100%
    ) !important;
}

/* Apply the background to the inner Streamlit container too */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: linear-gradient(
        135deg,
        #faf7fd 0%,
        #f4edfa 48%,
        #fff5f6 100%
    ) !important;
}

    /* Banner text */
    .home-eyebrow {
        color: #70428f;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .home-title {
        color: #3f235d;
        font-size: 2.4rem;
        font-weight: 700;
        line-height: 1.2;
        margin-top: 8px;
    }

    .home-description {
        color: #6f6678;
        font-size: 1rem;
        line-height: 1.7;
    }

    .home-note {
        color: #9a8595;
        font-size: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGO
# ============================================================

_, logo_col, _ = st.columns([1, 2, 1])

with logo_col:
    st.image(
        "utils/images/new_logo.png",
        use_container_width=True
    )


st.write("")


# ============================================================
# HOME BANNER
# ============================================================

with st.container(border=True):

    st.markdown(
        '<p class="home-eyebrow">DATA & AI PRACTICE</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="home-title">Your Internal Accelerator Hub</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="home-description">
        Explore pre-sales opportunities, track the sales pipeline,
        discover reusable accelerators and access Data & AI assets
        from one central workspace.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="home-note">InspireXT • Accelerate. Reuse. Deliver.</p>',
        unsafe_allow_html=True
    )
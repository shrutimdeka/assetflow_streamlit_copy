import streamlit as st
from utils.styles import apply_global_styles
from utils.data import assets
from utils.images import *
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

apply_global_styles()

st.markdown('<div class="eyebrow">Repository</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Asset Repository</div>', unsafe_allow_html=True)
st.markdown('<div class="page-description">Find, reuse and share accelerators, pre-sale demo and technical blogs.</div>', unsafe_allow_html=True)

df = assets()

# Count assets by category
accelerators = len(
    df[(df["Category"] == "Accelerator App") | (df["Category"] == "Accelerator Dashboard") ]
)

demo_assets = len(
    df[df["Category"] == "Demo Asset"]
)

technical_blogs = len(
    df[df["Category"] == "Blog"]
)

c1, c2, c3 = st.columns(3)

for col, label, value in zip(
    [c1, c2, c3],
    [
        "Accelerators",
        "Demo Assets",
        "Documents",
    ],
    [
        accelerators,
        demo_assets,
        technical_blogs,
    ],
):

    with col:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    search = st.text_input("Search repository", placeholder="Search by asset name, capability or technology")
with f2:
    category = st.selectbox("Category", ["All"] + sorted(df["Category"].unique()))

# ============================================================
# TECHNOLOGY OPTIONS BASED ON SELECTED CATEGORY
# ============================================================

if category == "All":

    # Show all technologies when all categories are selected
    technology_options = sorted(
        df["Technology"]
        .dropna()
        .astype(str)
        .unique()
    )

else:

    # Show only technologies available for the selected category
    technology_options = sorted(
        df.loc[
            df["Category"] == category,
            "Technology"
        ]
        .dropna()
        .astype(str)
        .unique()
    )


with f3:
    technology = st.selectbox(
        "Technology",
        ["All"] + technology_options
    )



filtered = df.copy()
if search:
    filtered = filtered[
        filtered["Name"].str.contains(search, case=False) |
        filtered["Description"].str.contains(search, case=False)
    ]
if category != "All":
    filtered = filtered[filtered["Category"] == category]
if technology != "All":
    filtered = filtered[filtered["Technology"] == technology]

st.write("")


cols = st.columns(3)

for i, (_, row) in enumerate(filtered.iterrows()):

    with cols[i % 3]:

        # ============================================================
        # ONE COMPLETE ASSET WIDGET
        # ============================================================
        with st.container(border=True):

            # --------------------------------------------------------
            # HEADER: ICON + TYPE + TITLE
            # --------------------------------------------------------
            icon_col, content_col = st.columns([0.65, 2.35])

            with icon_col:

                if row["Images"]:
                    image_path = BASE_DIR / "utils" / row["Images"]

                    if image_path.exists():
                        st.image(
                            str(image_path),
                            width=115
                        )

            with content_col:

                st.markdown(
                    f"""
                    <div class="asset-header">
                        <div class="asset-type">{row['Type']}</div>
                        <div class="asset-name">{row['Name']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # --------------------------------------------------------
            # DESCRIPTION
            # --------------------------------------------------------
            st.markdown(
                f"""
                <div class="asset-description">
                    {row['Description']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # --------------------------------------------------------
            # TECHNOLOGY
            # --------------------------------------------------------
            st.markdown(
                f"""
                <div class="asset-technology">
                    {row['Technology']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # --------------------------------------------------------
            # VIEW BUTTON
            # --------------------------------------------------------
            st.link_button(
                "View",
                row["URL"],
                use_container_width=True,
            )

st.write("")


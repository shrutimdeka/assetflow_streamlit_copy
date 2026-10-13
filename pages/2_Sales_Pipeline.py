import streamlit as st
import pandas as pd

from utils.styles import apply_global_styles

from utils.zoho_crm_data_dup import (
    get_databricks_leads,
    get_databricks_deals,
    get_solution_associations,
)


apply_global_styles()


# ============================================================
# HELPERS
# ============================================================

def first_existing_column(df, candidates):
    """Return the first matching column from a list of candidates."""
    for col in candidates:
        if col in df.columns:
            return col
    return None


def clean_date_column(df, column):
    """Convert a date column safely to datetime."""
    if column and column in df.columns:
        df = df.copy()
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )
    return df


def money_range(df, column):
    """Return safe min/max for Amount slider."""
    values = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if values.empty:
        return 0.0, 1000000.0

    minimum = float(values.min())
    maximum = float(values.max())

    if minimum == maximum:
        maximum = minimum + 1

    return minimum, maximum


def add_solution_column(deals_df, solution_deals_df):
    """
    Add Solution information to the main deals dataframe.

    First tries to match deals using Zoho record ID.
    Falls back to account matching if a deal ID is unavailable.
    """

    if deals_df is None or deals_df.empty:
        return deals_df

    deals_df = deals_df.copy()

    # Ensure Solution column always exists
    if "Solution" not in deals_df.columns:
        deals_df["Solution"] = pd.NA

    if solution_deals_df is None or solution_deals_df.empty:
        return deals_df

    solution_deals_df = solution_deals_df.copy()

    solution_title_col = first_existing_column(
        solution_deals_df,
        [
            "Solution",
            "Solution_Title",
            "Solution Title",
            "Solution_Title.name",
        ]
    )

    if not solution_title_col:
        return deals_df

    # --------------------------------------------------------
    # MATCH BY DEAL ID — preferred approach
    # --------------------------------------------------------

    deal_id_col = first_existing_column(
        deals_df,
        [
            "id",
            "ID",
            "Deal_ID",
            "Deal ID",
        ]
    )

    solution_deal_id_col = first_existing_column(
        solution_deals_df,
        [
            "id",
            "ID",
            "Deal_ID",
            "Deal ID",
        ]
    )

    if deal_id_col and solution_deal_id_col:

        solution_map = (
            solution_deals_df[
                [solution_deal_id_col, solution_title_col]
            ]
            .dropna(subset=[solution_deal_id_col])
            .copy()
        )

        solution_map.columns = [
            "_deal_id",
            "_solution"
        ]

        solution_map["_deal_id"] = (
            solution_map["_deal_id"]
            .astype(str)
            .str.strip()
        )

        # If the same deal belongs to multiple solutions,
        # display all solution names rather than dropping one.
        solution_map = (
            solution_map
            .groupby("_deal_id")["_solution"]
            .agg(
                lambda x: ", ".join(
                    sorted(
                        set(
                            x.dropna()
                            .astype(str)
                            .str.strip()
                        )
                    )
                )
            )
            .reset_index()
        )

        deals_df["_deal_id"] = (
            deals_df[deal_id_col]
            .astype(str)
            .str.strip()
        )

        deals_df = deals_df.merge(
            solution_map,
            on="_deal_id",
            how="left"
        )

        deals_df["Solution"] = (
            deals_df["Solution"]
            .fillna(deals_df["_solution"])
        )

        deals_df.drop(
            columns=["_deal_id", "_solution"],
            errors="ignore",
            inplace=True
        )

        return deals_df

    # --------------------------------------------------------
    # FALLBACK: MATCH BY ACCOUNT
    # --------------------------------------------------------

    deal_account_col = first_existing_column(
        deals_df,
        [
            "Account_Name",
            "Account_Name.name",
            "Account",
        ]
    )

    solution_account_col = first_existing_column(
        solution_deals_df,
        [
            "Account_Name",
            "Account_Name.name",
            "Account",
        ]
    )

    if not deal_account_col or not solution_account_col:
        return deals_df

    solution_map = (
        solution_deals_df[
            [solution_account_col, solution_title_col]
        ]
        .dropna(subset=[solution_account_col])
        .copy()
    )

    solution_map.columns = [
        "_account",
        "_solution"
    ]

    solution_map["_account"] = (
        solution_map["_account"]
        .astype(str)
        .str.strip()
    )

    solution_map = (
        solution_map
        .groupby("_account")["_solution"]
        .agg(
            lambda x: ", ".join(
                sorted(
                    set(
                        x.dropna()
                        .astype(str)
                        .str.strip()
                    )
                )
            )
        )
        .reset_index()
    )

    deals_df["_account"] = (
        deals_df[deal_account_col]
        .astype(str)
        .str.strip()
    )

    deals_df = deals_df.merge(
        solution_map,
        on="_account",
        how="left"
    )

    deals_df["Solution"] = (
        deals_df["Solution"]
        .fillna(deals_df["_solution"])
    )

    deals_df.drop(
        columns=["_account", "_solution"],
        errors="ignore",
        inplace=True
    )

    return deals_df


def combine_deals(direct_deals_df, solution_deals_df):
    """
    Combine direct Deals data with Solution Related Deals.

    Deduplicates using Zoho deal ID where available.
    Falls back to Deal Name if no ID exists.
    """

    if direct_deals_df is None:
        direct_deals_df = pd.DataFrame()

    if solution_deals_df is None:
        solution_deals_df = pd.DataFrame()

    direct_deals_df = direct_deals_df.copy()
    solution_deals_df = solution_deals_df.copy()

    # Keep track of where each record came from
    if not direct_deals_df.empty:
        direct_deals_df["_Record_Source"] = "Deals Module"

    if not solution_deals_df.empty:
        solution_deals_df["_Record_Source"] = "Solutions Related Deals"

    # If only one source exists
    if direct_deals_df.empty:
        return solution_deals_df

    if solution_deals_df.empty:
        return direct_deals_df

    # Combine all columns from both datasets
    combined_df = pd.concat(
        [direct_deals_df, solution_deals_df],
        ignore_index=True,
        sort=False
    )

    # --------------------------------------------------------
    # DEDUPLICATE BY ZOHO RECORD ID
    # --------------------------------------------------------

    deal_id_col = first_existing_column(
        combined_df,
        [
            "id",
            "ID",
            "Deal_ID",
            "Deal ID",
        ]
    )

    if deal_id_col:

        # Keep the Deals module record first when duplicates exist
        combined_df["_source_priority"] = (
            combined_df["_Record_Source"]
            .eq("Deals Module")
            .astype(int)
        )

        combined_df = (
            combined_df
            .sort_values("_source_priority", ascending=False)
            .drop_duplicates(
                subset=[deal_id_col],
                keep="first"
            )
            .drop(columns=["_source_priority"])
        )

    else:

        # ----------------------------------------------------
        # FALLBACK: DEDUPLICATE BY DEAL NAME
        # ----------------------------------------------------

        deal_name_col = first_existing_column(
            combined_df,
            [
                "Deal_Name",
                "Deal Name",
                "Name",
            ]
        )

        if deal_name_col:

            combined_df["_source_priority"] = (
                combined_df["_Record_Source"]
                .eq("Deals Module")
                .astype(int)
            )

            combined_df = (
                combined_df
                .sort_values("_source_priority", ascending=False)
                .drop_duplicates(
                    subset=[deal_name_col],
                    keep="first"
                )
                .drop(columns=["_source_priority"])
            )

    return combined_df.reset_index(drop=True)


# ============================================================
# LOAD DATA
# ============================================================

leads_df = get_databricks_leads()

direct_deals_df = get_databricks_deals()

# get_solution_associations() returns:
# 1. solution-related leads
# 2. solution-related deals
solution_leads_df, solution_deals_df = get_solution_associations()


# ------------------------------------------------------------
# HANDLE EMPTY DATAFRAMES
# ------------------------------------------------------------

if leads_df is None:
    leads_df = pd.DataFrame()

if direct_deals_df is None:
    direct_deals_df = pd.DataFrame()

if solution_leads_df is None:
    solution_leads_df = pd.DataFrame()

if solution_deals_df is None:
    solution_deals_df = pd.DataFrame()


# ------------------------------------------------------------
# ADD SOLUTION INFORMATION TO BOTH DEAL DATASETS
# ------------------------------------------------------------

direct_deals_df = add_solution_column(
    direct_deals_df,
    solution_deals_df
)

solution_deals_df = add_solution_column(
    solution_deals_df,
    solution_deals_df
)


# ------------------------------------------------------------
# COMBINE ORIGINAL DEALS + SOLUTION RELATED DEALS
# ------------------------------------------------------------

deals_df = combine_deals(
    direct_deals_df,
    solution_deals_df
)


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    '<div class="eyebrow">Sales Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-title">Sales Pipeline</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-description">'
    'Track Databricks opportunities from lead through deal conversion.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TABS
# ============================================================

tab_leads, tab_deals = st.tabs(
    ["Leads", "Deals"]
)


# ============================================================
# TAB 1 — LEADS
# ============================================================

with tab_leads:

    if leads_df.empty:

        st.info("No leads found.")

    else:

        source_col = first_existing_column(
            leads_df,
            [
                "Lead_Source",
                "Lead Source",
                "Source",
            ]
        )

        owner_col = first_existing_column(
            leads_df,
            [
                "Owner",
                "Owner.name",
                "Lead_Owner",
            ]
        )

        created_col = first_existing_column(
            leads_df,
            [
                "Created_Time",
                "Created Date",
                "Created_Time.date",
            ]
        )

        # Convert timestamp/string to datetime
        leads_df = clean_date_column(
            leads_df,
            created_col
        )


        # ----------------------------------------------------
        # LEADS BY SOURCE KPIs
        # ----------------------------------------------------

        st.markdown(
            '<div class="panel-title">Leads by Source</div>',
            unsafe_allow_html=True
        )

        if source_col:

            source_counts = (
                leads_df[source_col]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
            )

            source_cols = st.columns(
                min(len(source_counts), 4)
            )

            for i, (source, count) in enumerate(
                source_counts.items()
            ):

                with source_cols[i % len(source_cols)]:

                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">
                                {source}
                            </div>
                            <div class="metric-value">
                                {count}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


        # ----------------------------------------------------
        # LEADS BY OWNER KPIs
        # ----------------------------------------------------

        st.write("")
        st.write("")

        st.markdown(
            '<div class="panel-title">Leads by Owner</div>',
            unsafe_allow_html=True
        )

        if owner_col:

            owner_counts = (
                leads_df[owner_col]
                .fillna("Unassigned")
                .astype(str)
                .value_counts()
            )

            owner_cols = st.columns(
                min(len(owner_counts), 4)
            )

            for i, (owner, count) in enumerate(
                owner_counts.items()
            ):

                with owner_cols[i % len(owner_cols)]:

                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">
                                {owner}
                            </div>
                            <div class="metric-value">
                                {count}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


        # ====================================================
        # LEAD TABLE
        # ====================================================

        st.write("")
        st.write("")
        st.divider()

        st.markdown(
            '<div class="panel-title">Lead Details</div>',
            unsafe_allow_html=True
        )


        # ====================================================
        # FILTERS — LEADS
        # ====================================================

        f1, f2 = st.columns(2)

        with f1:

            # FILTER: Lead Owner
            if owner_col:

                selected_owner = st.selectbox(
                    "Owner",
                    ["All"]
                    + sorted(
                        leads_df[owner_col]
                        .dropna()
                        .astype(str)
                        .unique()
                    ),
                    key="lead_owner_filter"
                )

            else:
                selected_owner = "All"


        with f2:

            # FILTER: Lead Created Date
            if created_col:

                valid_dates = (
                    leads_df[created_col]
                    .dropna()
                )

                if not valid_dates.empty:

                    date_range = st.date_input(
                        "Created Date",
                        value=(
                            valid_dates.min().date(),
                            valid_dates.max().date()
                        ),
                        key="lead_date_filter"
                    )

                else:
                    date_range = None

            else:
                date_range = None


        filtered_leads = leads_df.copy()


        # ====================================================
        # APPLY LEAD FILTERS
        # ====================================================

        # FILTER: Owner
        if selected_owner != "All" and owner_col:

            filtered_leads = filtered_leads[
                filtered_leads[owner_col]
                .astype(str)
                .eq(selected_owner)
            ]


        # FILTER: Created Date
        if (
            created_col
            and date_range
            and len(date_range) == 2
        ):

            start_date, end_date = date_range

            filtered_leads = filtered_leads[
                filtered_leads[created_col]
                .dt.date
                .between(
                    start_date,
                    end_date
                )
            ]


        st.dataframe(
            filtered_leads,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TAB 2 — DEALS
# ============================================================

with tab_deals:

    if deals_df.empty:

        st.info("No deals found.")

    else:

        # ----------------------------------------------------
        # IDENTIFY COLUMNS
        # ----------------------------------------------------

        stage_col = first_existing_column(
            deals_df,
            [
                "Stage",
                "Deal_Status",
                "Deal Status",
                "Status",
            ]
        )

        source_col = first_existing_column(
            deals_df,
            [
                "Lead_Source",
                "Deal_Source",
                "Deal Source",
                "Source",
            ]
        )

        closing_col = first_existing_column(
            deals_df,
            [
                "Closing_Date",
                "Closing Date",
                "Close_Date",
            ]
        )

        amount_col = first_existing_column(
            deals_df,
            [
                "Amount",
                "Deal_Amount",
            ]
        )


        # ----------------------------------------------------
        # CLEAN DEAL DATE
        # ----------------------------------------------------

        deals_df = clean_date_column(
            deals_df,
            closing_col
        )


        # ====================================================
        # DEALS BY SOURCE KPIs
        # Same styling as Leads tab
        # ====================================================

        st.markdown(
            '<div class="panel-title">Deals by Source</div>',
            unsafe_allow_html=True
        )

        if source_col:

            deal_source_counts = (
                deals_df[source_col]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
            )

            source_cols = st.columns(
                min(len(deal_source_counts), 4)
            )

            for i, (source, count) in enumerate(
                deal_source_counts.items()
            ):

                with source_cols[i % len(source_cols)]:

                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">
                                {source}
                            </div>
                            <div class="metric-value">
                                {count}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            st.info(
                "No Source column was found in the deals data."
            )


        st.write("")
        st.write("")


        # ====================================================
        # DEAL PIPELINE KPIs
        # ====================================================

        st.markdown(
            '<div class="panel-title">Deal Pipeline</div>',
            unsafe_allow_html=True
        )

        if not stage_col:

            st.warning(
                "No deal status/stage column was found."
            )

        else:

            # ------------------------------------------------
            # DEAL STATUS COUNTS
            # ------------------------------------------------

            stage_counts = (
                deals_df[stage_col]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
            )

            stage_names = list(stage_counts.index)

         #----deals pipeline START----------------

            stage_cols = st.columns(
                min(len(stage_names), 5)
            )

            for i, stage in enumerate(stage_names):

                count = stage_counts[stage]

                with stage_cols[i % len(stage_cols)]:

                    if st.button(
                        f"{stage}\n{count}",
                        key=f"deal_stage_{stage}",
                        use_container_width=True
                    ):

                        st.session_state[
                            "selected_deal_stage"
                        ] = stage

          #---deals pipeline widgets END--------------

            selected_stage = st.session_state.get(
                "selected_deal_stage",
                stage_names[0] if stage_names else None
            )


            # =================================================
            # SELECTED DEALS
            # =================================================

            if selected_stage:

                st.write("")

                selected_deals = deals_df[
                    deals_df[stage_col]
                    .fillna("Unknown")
                    .astype(str)
                    .eq(selected_stage)
                ].copy()


                st.markdown(
                    f"""
                    <div class="panel-title">
                        {selected_stage} — {len(selected_deals)} Deals
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # =============================================
                # DEAL FILTERS
                # =============================================

                f1, f2 = st.columns(2)


                with f1:

                    # FILTER: Closing Date
                    if closing_col:

                        valid_dates = (
                            deals_df[closing_col]
                            .dropna()
                        )

                        if not valid_dates.empty:

                            closing_range = st.date_input(
                                "Closing Date",
                                value=(
                                    valid_dates.min().date(),
                                    valid_dates.max().date()
                                ),
                                key="deal_closing_date"
                            )

                        else:
                            closing_range = None

                    else:
                        closing_range = None


                with f2:

                    # FILTER: Amount
                    if amount_col:

                        deals_df[amount_col] = pd.to_numeric(
                            deals_df[amount_col],
                            errors="coerce"
                        )

                        amount_min, amount_max = money_range(
                            deals_df,
                            amount_col
                        )

                        amount_range = st.slider(
                            "Amount",
                            min_value=float(amount_min),
                            max_value=float(amount_max),
                            value=(
                                float(amount_min),
                                float(amount_max)
                            ),
                            key="deal_amount_filter"
                        )

                    else:
                        amount_range = None


                # =============================================
                # APPLY DEAL FILTERS
                # =============================================

                filtered_deals = selected_deals.copy()


                # FILTER: Closing Date
                if (
                    closing_col
                    and closing_range
                    and len(closing_range) == 2
                ):

                    start_date, end_date = closing_range

                    filtered_deals = filtered_deals[
                        filtered_deals[closing_col]
                        .dt.date
                        .between(
                            start_date,
                            end_date
                        )
                    ]


                # FILTER: Amount
                if amount_col and amount_range:

                    filtered_deals = filtered_deals[
                        filtered_deals[amount_col]
                        .between(
                            amount_range[0],
                            amount_range[1]
                        )
                    ]


                # =============================================
                # DEAL TABLE
                # =============================================

                st.dataframe(
                    filtered_deals,
                    use_container_width=True,
                    hide_index=True
                )


        # ====================================================
        # SOLUTION RELATED DEALS — VALIDATION TABLE
        # ====================================================

        st.write("")
        st.write("")
        st.divider()

        st.markdown(
            '<div class="panel-title">'
            'Solution Related Deals'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="page-description">
                Deals fetched through related records under
                Databricks Solutions. This table helps validate
                records contributed by the Solutions module.
            </div>
            """,
            unsafe_allow_html=True
        )

        if solution_deals_df.empty:

            st.info(
                "No related deals were returned from Solutions."
            )

        else:

            st.dataframe(
                solution_deals_df,
                use_container_width=True,
                hide_index=True
            )
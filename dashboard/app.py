from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Retention Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("Customer Engagement & Product Utilization Analytics")
st.caption(
    "Retention Strategy Dashboard | European Bank Dataset | "
    "Year: 2025 | Descriptive Analytics"
)


# --------------------------------------------------
# 2. DATA LOADING AND VALIDATION
# --------------------------------------------------

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "European_Bank.csv"
)

REQUIRED_COLUMNS = [
    "Year",
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited",
]

BINARY_COLUMNS = ["HasCrCard", "IsActiveMember", "Exited"]

NUMERIC_COLUMNS = [
    "Year",
    "CreditScore",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited",
]

ENGAGEMENT_ORDER = [
    "Active Engaged",
    "Active but Low-Product",
    "Inactive High-Balance",
    "Inactive Disengaged",
]


def validate_data(data: pd.DataFrame) -> None:
    """Raise a clear error when the input dataset fails essential checks."""

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    missing_counts = data[REQUIRED_COLUMNS].isna().sum()
    columns_with_missing = missing_counts[missing_counts > 0]
    if not columns_with_missing.empty:
        details = columns_with_missing.to_dict()
        raise ValueError(f"Missing values detected: {details}")

    non_numeric = [
        column
        for column in NUMERIC_COLUMNS
        if not pd.api.types.is_numeric_dtype(data[column])
    ]
    if non_numeric:
        raise ValueError(f"Expected numeric columns: {non_numeric}")

    if not np.isfinite(data[NUMERIC_COLUMNS].to_numpy(dtype=float)).all():
        raise ValueError("Non-finite numeric values (inf or -inf) were detected.")

    for column in BINARY_COLUMNS:
        observed = set(data[column].unique())
        if not observed.issubset({0, 1}):
            raise ValueError(
                f"{column} must contain only binary values 0 and 1. "
                f"Found: {sorted(observed)}"
            )

    if not data["NumOfProducts"].between(1, 4).all():
        raise ValueError("NumOfProducts contains values outside the expected 1–4 range.")

    if not data["Tenure"].between(0, 10).all():
        raise ValueError("Tenure contains values outside the expected 0–10 range.")

    if (data["Balance"] < 0).any():
        raise ValueError("Balance contains negative values.")

    if (data["EstimatedSalary"] < 0).any():
        raise ValueError("EstimatedSalary contains negative values.")

    if (data["Age"] <= 0).any():
        raise ValueError("Age must contain positive values.")

    if data.empty:
        raise ValueError("The dataset contains no customer records.")


@st.cache_data
def load_and_prepare_data(path: str) -> tuple[pd.DataFrame, float]:
    """Load, validate and prepare the dataset using full-dataset thresholds."""

    data = pd.read_csv(path)
    validate_data(data)

    # Remove direct identifiers before any dashboard analysis or display.
    safe_df = data.drop(
        columns=["CustomerId", "Surname"],
        errors="ignore",
    ).copy()

    # Calculate the threshold once using the full dataset, before filters.
    median_balance = float(safe_df["Balance"].median())

    safe_df["Engagement_Segment"] = np.select(
        [
            (safe_df["IsActiveMember"] == 1)
            & (safe_df["NumOfProducts"] > 1),

            (safe_df["IsActiveMember"] == 1)
            & (safe_df["NumOfProducts"] == 1),

            (safe_df["IsActiveMember"] == 0)
            & (safe_df["Balance"] > median_balance),

            (safe_df["IsActiveMember"] == 0)
            & (safe_df["Balance"] <= median_balance),
        ],
        [
            "Active Engaged",
            "Active but Low-Product",
            "Inactive High-Balance",
            "Inactive Disengaged",
        ],
        default="Unclassified",
    )

    if (safe_df["Engagement_Segment"] == "Unclassified").any():
        raise ValueError("Some customers could not be assigned an engagement segment.")

    # Custom descriptive Relationship Strength Index (0–100).
    # Four equally weighted components, each normalized to 0–1.
    safe_df["RSI"] = (
        safe_df["IsActiveMember"]
        + safe_df["HasCrCard"]
        + (safe_df["NumOfProducts"].clip(upper=2) / 2.0)
        + (safe_df["Tenure"] / 10.0)
    ) / 4.0 * 100.0

    safe_df["Churn_Status"] = np.where(
        safe_df["Exited"] == 1,
        "Exited (1)",
        "Retained (0)",
    )

    return safe_df, median_balance


def safe_rate(numerator: int, denominator: int) -> float | None:
    """Return a percentage, or None when its denominator is zero."""

    if denominator == 0:
        return None
    return numerator / denominator * 100.0


def format_percentage(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.2f}%"


def format_number(value: float | None) -> str:
    return "N/A" if value is None or pd.isna(value) else f"{value:,.2f}"


def render_dynamic_takeaways(
    title: str,
    bullets: list[str],
    suggestions: list[str],
) -> None:
    """Render filter-aware descriptive observations and cautious suggestions."""

    st.subheader(title)
    st.markdown("\n".join(f"- {item}" for item in bullets))

    if suggestions:
        st.markdown("**Suggested Focus Areas (Descriptive / Hypothesis-Driven):**")
        st.markdown("\n".join(f"- {item}" for item in suggestions))


try:
    df, median_balance = load_and_prepare_data(str(DATA_PATH))
except Exception as error:
    st.error(f"Could not load or validate the dataset: {error}")
    st.stop()


# --------------------------------------------------
# 3. SIDEBAR FILTERS AND MODULE NAVIGATION
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

engagement_options = [
    segment
    for segment in ENGAGEMENT_ORDER
    if segment in set(df["Engagement_Segment"].unique())
]

selected_engagement = st.sidebar.multiselect(
    "Engagement Segment",
    options=engagement_options,
    default=engagement_options,
)

product_options = sorted(int(value) for value in df["NumOfProducts"].unique())

selected_products = st.sidebar.multiselect(
    "Number of Products",
    options=product_options,
    default=product_options,
)

balance_min = float(df["Balance"].min())
balance_max = float(df["Balance"].max())

balance_range = st.sidebar.slider(
    "Account Balance Range",
    min_value=balance_min,
    max_value=balance_max,
    value=(balance_min, balance_max),
    format="%.0f",
)

salary_min = float(df["EstimatedSalary"].min())
salary_max = float(df["EstimatedSalary"].max())

salary_range = st.sidebar.slider(
    "Estimated Salary Range",
    min_value=salary_min,
    max_value=salary_max,
    value=(salary_min, salary_max),
    format="%.0f",
)

st.sidebar.divider()

module = st.sidebar.radio(
    "Analytical Module",
    [
        "Engagement & Churn Overview",
        "Product Utilization",
        "High-Value Disengaged Detector",
        "Retention Strength Analysis",
    ],
)

st.sidebar.divider()
st.sidebar.caption(
    "Metrics and charts respond to the active filters. "
    f"Engagement segments use the full-dataset median balance "
    f"({median_balance:,.2f})."
)

filtered_df = df[
    df["Engagement_Segment"].isin(selected_engagement)
    & df["NumOfProducts"].isin(selected_products)
    & df["Balance"].between(*balance_range)
    & df["EstimatedSalary"].between(*salary_range)
].copy()

if filtered_df.empty:
    st.warning(
        "No customers match the selected filter combination. "
        "Adjust the sidebar filters to view the analysis."
    )
    st.stop()


# --------------------------------------------------
# 4. FILTERED POPULATION METRICS
# --------------------------------------------------

total_customers = len(filtered_df)
exited_count = int(filtered_df["Exited"].sum())
retained_count = total_customers - exited_count

churn_rate = safe_rate(exited_count, total_customers)
retention_rate = safe_rate(retained_count, total_customers)

active_df = filtered_df[filtered_df["IsActiveMember"] == 1]
active_retained_count = int((active_df["Exited"] == 0).sum())
engagement_retention_ratio = safe_rate(
    active_retained_count,
    len(active_df),
)

retained_df = filtered_df[filtered_df["Exited"] == 0]
product_depth_index = (
    float(retained_df["NumOfProducts"].mean())
    if not retained_df.empty
    else None
)

high_balance_df = filtered_df[filtered_df["Balance"] > median_balance]
inactive_high_balance_count = int(
    (high_balance_df["IsActiveMember"] == 0).sum()
)
high_balance_disengagement_rate = safe_rate(
    inactive_high_balance_count,
    len(high_balance_df),
)

cardholders_df = filtered_df[filtered_df["HasCrCard"] == 1]
retained_cardholders_count = int((cardholders_df["Exited"] == 0).sum())
credit_card_stickiness_score = safe_rate(
    retained_cardholders_count,
    len(cardholders_df),
)

relationship_strength_index = float(filtered_df["RSI"].mean())
average_products = float(filtered_df["NumOfProducts"].mean())


# --------------------------------------------------
# 5. OVERVIEW
# --------------------------------------------------

st.subheader("Retention Overview")

overview_cols = st.columns(4)

overview_cols[0].metric(
    "Total Customers",
    f"{total_customers:,}",
)
overview_cols[1].metric(
    "Retention Rate",
    format_percentage(retention_rate),
)
overview_cols[2].metric(
    "Churn Rate",
    format_percentage(churn_rate),
)
overview_cols[3].metric(
    "Average Product Count",
    f"{average_products:.2f}",
)

st.caption(
    f"Showing {total_customers:,} filtered customers out of {len(df):,} total records. "
    "Figures describe associations in cross-sectional 2025 data."
)

st.subheader("Required Retention KPIs")

kpi_cols = st.columns(5)

kpi_cols[0].metric(
    "Engagement Retention Ratio",
    format_percentage(engagement_retention_ratio),
    help="Retained active customers divided by all active customers in the filtered population.",
)
kpi_cols[1].metric(
    "Product Depth Index",
    format_number(product_depth_index),
    help="Average number of products held by retained customers in the filtered population.",
)
kpi_cols[2].metric(
    "High-Balance Disengagement Rate",
    format_percentage(high_balance_disengagement_rate),
    help="Inactive customers above the full-dataset median balance divided by all customers above that threshold.",
)
kpi_cols[3].metric(
    "Credit Card Stickiness Score",
    format_percentage(credit_card_stickiness_score),
    help="Retained credit-card holders divided by all credit-card holders in the filtered population.",
)
kpi_cols[4].metric(
    "Relationship Strength Index",
    f"{relationship_strength_index:.2f}",
    help="Mean of the custom 0–100 descriptive RSI across the filtered population.",
)

st.caption(
    "KPI denominators are calculated within the filtered population, except that "
    "the high-balance threshold remains fixed at the full-dataset median. "
    "N/A means the relevant denominator or retained-customer group is empty."
)

st.divider()


# --------------------------------------------------
# 6. ANALYTICAL MODULES
# --------------------------------------------------

if module == "Engagement & Churn Overview":

    st.header("Engagement & Churn Overview")

    engagement_summary = (
        filtered_df.groupby("Engagement_Segment", as_index=False)
        .agg(
            Customers=("Exited", "size"),
            Exited=("Exited", "sum"),
            Churn_Rate_Pct=(
                "Exited",
                lambda values: round(float(values.mean() * 100.0), 2),
            ),
        )
    )

    engagement_summary["Engagement_Segment"] = pd.Categorical(
        engagement_summary["Engagement_Segment"],
        categories=ENGAGEMENT_ORDER,
        ordered=True,
    )
    engagement_summary = engagement_summary.sort_values("Engagement_Segment")

    left, right = st.columns(2)

    with left:
        fig_dist = px.bar(
            engagement_summary,
            x="Engagement_Segment",
            y="Customers",
            color="Engagement_Segment",
            title="Customer Distribution by Engagement Segment",
            labels={
                "Engagement_Segment": "Engagement Segment",
                "Customers": "Number of Customers",
            },
            category_orders={"Engagement_Segment": ENGAGEMENT_ORDER},
        )
        fig_dist.update_layout(showlegend=False)
        st.plotly_chart(fig_dist, width="stretch")

    with right:
        fig_churn = px.bar(
            engagement_summary,
            x="Engagement_Segment",
            y="Churn_Rate_Pct",
            color="Engagement_Segment",
            title="Churn Rate by Engagement Segment",
            labels={
                "Engagement_Segment": "Engagement Segment",
                "Churn_Rate_Pct": "Churn Rate (%)",
            },
            category_orders={"Engagement_Segment": ENGAGEMENT_ORDER},
        )
        fig_churn.update_layout(showlegend=False)
        st.plotly_chart(fig_churn, width="stretch")

    st.subheader("Engagement Segment Summary")
    st.dataframe(
        engagement_summary,
        hide_index=True,
        width="stretch",
    )

    highest_row = engagement_summary.loc[
        engagement_summary["Churn_Rate_Pct"].idxmax()
    ]
    lowest_row = engagement_summary.loc[
        engagement_summary["Churn_Rate_Pct"].idxmin()
    ]

    engagement_bullets = [
        f"Overall churn in the current selection is {churn_rate:.2f}% "
        f"({exited_count:,} exited customers out of {total_customers:,}).",
        f"Highest observed segment churn is "
        f"'{highest_row['Engagement_Segment']}' at "
        f"{highest_row['Churn_Rate_Pct']:.2f}% "
        f"(n = {int(highest_row['Customers']):,}).",
        f"Lowest observed segment churn is "
        f"'{lowest_row['Engagement_Segment']}' at "
        f"{lowest_row['Churn_Rate_Pct']:.2f}% "
        f"(n = {int(lowest_row['Customers']):,}).",
    ]

    if (
        total_customers < 200
        or int(highest_row["Customers"]) < 100
        or int(lowest_row["Customers"]) < 100
    ):
        engagement_bullets.append(
            "Sample-size caution: At least one segment has a relatively small "
            "filtered count. Interpret its churn rate cautiously."
        )

    engagement_suggestions = [
        "Prioritize engagement check-ins for inactive customers before introducing new cross-sell offers.",
        "Review service friction and onboarding touchpoints for active single-product customers.",
    ]

    render_dynamic_takeaways(
        "Filtered Summary & Suggestions",
        engagement_bullets,
        engagement_suggestions,
    )


elif module == "Product Utilization":

    st.header("Product Utilization Analysis")

    product_summary = (
        filtered_df.groupby("NumOfProducts", as_index=False)
        .agg(
            Customers=("Exited", "size"),
            Exited=("Exited", "sum"),
            Churn_Rate_Pct=(
                "Exited",
                lambda values: round(float(values.mean() * 100.0), 2),
            ),
        )
        .sort_values("NumOfProducts")
    )

    product_labels = [
        str(value)
        for value in sorted(product_summary["NumOfProducts"].unique())
    ]
    product_summary["Product_Count_Label"] = (
        product_summary["NumOfProducts"].astype(str)
    )

    left, right = st.columns(2)

    with left:
        fig_count = px.bar(
            product_summary,
            x="Product_Count_Label",
            y="Customers",
            title="Customer Distribution by Product Count",
            labels={
                "Product_Count_Label": "Number of Products",
                "Customers": "Number of Customers",
            },
            text="Customers",
            category_orders={"Product_Count_Label": product_labels},
        )
        st.plotly_chart(fig_count, width="stretch")

    with right:
        fig_churn = px.bar(
            product_summary,
            x="Product_Count_Label",
            y="Churn_Rate_Pct",
            title="Churn Rate by Product Count",
            labels={
                "Product_Count_Label": "Number of Products",
                "Churn_Rate_Pct": "Churn Rate (%)",
            },
            text_auto=".1f",
            category_orders={"Product_Count_Label": product_labels},
        )
        st.plotly_chart(fig_churn, width="stretch")

    st.subheader("Product Utilization Summary")
    st.dataframe(
        product_summary[
            ["NumOfProducts", "Customers", "Exited", "Churn_Rate_Pct"]
        ],
        hide_index=True,
        width="stretch",
    )

    lowest_product = product_summary.loc[
        product_summary["Churn_Rate_Pct"].idxmin()
    ]
    highest_product = product_summary.loc[
        product_summary["Churn_Rate_Pct"].idxmax()
    ]

    product_bullets = [
        f"Average product count in the selected population is "
        f"{average_products:.2f} across {total_customers:,} customers.",
        f"Lowest observed churn occurs among customers with "
        f"{int(lowest_product['NumOfProducts'])} product(s): "
        f"{lowest_product['Churn_Rate_Pct']:.2f}% "
        f"(n = {int(lowest_product['Customers']):,}).",
        f"Highest observed churn occurs among customers with "
        f"{int(highest_product['NumOfProducts'])} product(s): "
        f"{highest_product['Churn_Rate_Pct']:.2f}% "
        f"(n = {int(highest_product['Customers']):,}).",
        "The dataset records product counts, not product names or specific bundle combinations.",
    ]

    if any(value >= 3 for value in product_summary["NumOfProducts"]):
        product_bullets.append(
            "Small-group caution: Customers with three or four products represent "
            "a small share of the full dataset. Avoid over-generalizing their churn rates."
        )

    product_suggestions = [
        "Evaluate multi-product adoption around core account usage rather than pushing high product counts indiscriminately.",
        "Investigate whether elevated churn among high-product-count customers coincides with pricing, fees or account complexity.",
    ]

    render_dynamic_takeaways(
        "Filtered Summary & Suggestions",
        product_bullets,
        product_suggestions,
    )


elif module == "High-Value Disengaged Detector":

    st.header("High-Value Disengaged Customer Detector")

    st.write(
        "Identifies retained customers who are inactive "
        "(`IsActiveMember == 0`) and hold balances above the full-dataset median."
    )

    high_value_disengaged = filtered_df[
        (filtered_df["IsActiveMember"] == 0)
        & (filtered_df["Balance"] > median_balance)
        & (filtered_df["Exited"] == 0)
    ].copy()

    high_value_cols = st.columns(3)

    high_value_cols[0].metric(
        "Actionable Retained Customers",
        f"{len(high_value_disengaged):,}",
    )
    high_value_cols[1].metric(
        "Average Account Balance",
        format_number(
            float(high_value_disengaged["Balance"].mean())
            if not high_value_disengaged.empty
            else None
        ),
    )
    high_value_cols[2].metric(
        "Full-Dataset Median Balance",
        f"{median_balance:,.2f}",
    )

    st.subheader("Actionable Customer Profile")

    if not high_value_disengaged.empty:

        profile_values = [
            (
                "Average Age",
                float(high_value_disengaged["Age"].mean()),
            ),
            (
                "Average Tenure (Years)",
                float(high_value_disengaged["Tenure"].mean()),
            ),
            (
                "Average Balance",
                float(high_value_disengaged["Balance"].mean()),
            ),
            (
                "Average Estimated Salary",
                float(high_value_disengaged["EstimatedSalary"].mean()),
            ),
            (
                "Average Product Count",
                float(high_value_disengaged["NumOfProducts"].mean()),
            ),
        ]

        profile = pd.DataFrame(
            {
                "Metric": [item[0] for item in profile_values],
                "Value": [f"{item[1]:,.2f}" for item in profile_values],
            }
        )

        st.dataframe(
            profile,
            hide_index=True,
            width="stretch",
        )

        average_balance_hv = float(high_value_disengaged["Balance"].mean())
        average_products_hv = float(
            high_value_disengaged["NumOfProducts"].mean()
        )

        high_value_bullets = [
            f"{len(high_value_disengaged):,} retained customers in the current "
            f"filter match the inactive high-balance profile.",
            f"The group has an average balance of {average_balance_hv:,.2f} "
            f"and an average product count of {average_products_hv:.2f}.",
            "Balance is a proxy for potential financial value, not verified bank profitability or customer lifetime value.",
            "Inactivity is a proxy for disengagement; transaction recency and frequency are not available in this dataset.",
        ]

        high_value_suggestions = [
            "Run targeted check-in outreach to identify dormant-account friction or underused features.",
            "Prioritize outreach using balance and activity together, before proposing additional products.",
        ]

        render_dynamic_takeaways(
            "Filtered Summary & Suggestions",
            high_value_bullets,
            high_value_suggestions,
        )

    else:
        st.info(
            "No retained inactive high-balance customers match the active filter criteria."
        )


elif module == "Retention Strength Analysis":

    st.header("Retention Strength Analysis")

    retained_customers = filtered_df[filtered_df["Exited"] == 0]
    exited_customers = filtered_df[filtered_df["Exited"] == 1]

    rsi_cols = st.columns(3)

    rsi_cols[0].metric(
        "Average RSI",
        f"{filtered_df['RSI'].mean():.2f}",
    )
    rsi_cols[1].metric(
        "Retained Customer RSI",
        format_number(
            float(retained_customers["RSI"].mean())
            if not retained_customers.empty
            else None
        ),
    )
    rsi_cols[2].metric(
        "Exited Customer RSI",
        format_number(
            float(exited_customers["RSI"].mean())
            if not exited_customers.empty
            else None
        ),
    )

    left, right = st.columns(2)

    with left:
        fig_hist = px.histogram(
            filtered_df,
            x="RSI",
            color="Churn_Status",
            nbins=20,
            barmode="overlay",
            title="Relationship Strength Index Distribution",
            labels={
                "RSI": "Relationship Strength Index (0–100)",
                "Churn_Status": "Customer Status",
            },
            category_orders={
                "Churn_Status": ["Retained (0)", "Exited (1)"]
            },
        )
        st.plotly_chart(fig_hist, width="stretch")

    with right:
        fig_box = px.box(
            filtered_df,
            x="Churn_Status",
            y="RSI",
            color="Churn_Status",
            title="Relationship Strength by Customer Status",
            labels={
                "Churn_Status": "Customer Status",
                "RSI": "Relationship Strength Index (0–100)",
            },
            category_orders={
                "Churn_Status": ["Retained (0)", "Exited (1)"]
            },
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, width="stretch")

    st.subheader("RSI Component Definitions")

    rsi_components = pd.DataFrame(
        {
            "Component": [
                "Account Activity",
                "Credit Card Ownership",
                "Product Depth",
                "Relationship Duration",
            ],
            "Weight": ["25%", "25%", "25%", "25%"],
            "Calculation": [
                "IsActiveMember (0 or 1)",
                "HasCrCard (0 or 1)",
                "min(NumOfProducts, 2) / 2",
                "Tenure / 10",
            ],
        }
    )

    st.dataframe(
        rsi_components,
        hide_index=True,
        width="stretch",
    )

    rsi_bullets = [
        f"Mean RSI across the selected {total_customers:,} customers is "
        f"{filtered_df['RSI'].mean():.2f}.",
    ]

    if not retained_customers.empty and not exited_customers.empty:
        retained_rsi = float(retained_customers["RSI"].mean())
        exited_rsi = float(exited_customers["RSI"].mean())

        rsi_bullets.append(
            f"Retained customers average {retained_rsi:.2f} "
            f"(n = {len(retained_customers):,}) versus "
            f"{exited_rsi:.2f} among exited customers "
            f"(n = {len(exited_customers):,})."
        )
    elif retained_customers.empty:
        rsi_bullets.append(
            "No retained customers (Exited == 0) are present in this filter."
        )
    else:
        rsi_bullets.append(
            "No exited customers (Exited == 1) are present in this filter."
        )

    rsi_bullets.append(
        "RSI uses equal 25% descriptive weights. It is not a calibrated "
        "probability or a predictive churn model."
    )

    rsi_suggestions = [
        "Inspect the individual RSI components rather than treating a mid-range score alone as a churn trigger.",
        "Validate component weights against observed outcomes before using the index for operational decisions.",
    ]

    render_dynamic_takeaways(
        "Filtered Summary & Suggestions",
        rsi_bullets,
        rsi_suggestions,
    )


# --------------------------------------------------
# 7. FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "Customer Engagement & Product Utilization Analytics | "
    "Unified Mentor Project | Cross-Sectional Dataset Year: 2025 | "
    "Independent descriptive analysis (not an official European Central Bank publication)."
)

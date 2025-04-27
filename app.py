# bank_stacx_app.py
"""
Bank Stacx 2.0 – Streamlit dashboard for peer‑to‑peer bank analytics

Sections
--------
1. Key Financials – tabular peer comparison of raw financial statement line‑items
2. Key Metrics   – computed ratios with chart v s. sector average
3. CCAR Stress‑Test – capital‑adequacy metrics with chart v s. sector average

How to run
----------
1. Install requirements: `pip install streamlit pandas numpy plotly`
2. Place the Excel file `Line items (1).xlsx` in the same folder as this script.
3. Run `streamlit run bank_stacx_app.py`
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

DATA_FILE = Path(__file__).with_name("Line items (1).xlsx")

# ---------- Helpers ---------------------------------------------------------

def load_data(path: Path) -> pd.DataFrame:
    """Load excel – assumes first sheet contains wide‑format bank data."""
    return pd.read_excel(path)

def get_peer_group(df: pd.DataFrame, bank: str) -> pd.DataFrame:
    """Return dataframe filtered to selected bank's peer group (all banks for now)."""
    return df  # placeholder – could refine by size/region tier later

# ---------- UI ----------------------------------------------------------------
st.set_page_config(page_title="Bank Stacx 2.0", layout="wide")
st.title("🏦 Bank Stacx 2.0 – Peer‑to‑Peer Bank Analytics")

# Load raw excel once and cache
@st.cache_data
def cached_data():
    return load_data(DATA_FILE)

df_raw = cached_data()

banks = df_raw["Bank"].unique().tolist()
selected_bank = st.sidebar.selectbox("Select a Bank", banks)
peer_df = get_peer_group(df_raw, selected_bank)
selected_bank_df = peer_df[peer_df["Bank"] == selected_bank].iloc[0]

# ---------- Key Financials ----------------------------------------------------
with st.expander("Key Financials", expanded=True):
    st.subheader("Key Financials – Peer Comparison")
    fin_cols = [
        "PAT", "Depreciation", "Total Liabilities (excluding equity)",
        "Cash & cash equivalents", "Total Assets", "Current Assets", "Current Liabilities",
        "Accounts Receivables", "Marketable Securities", "Core Deposits", "Total Deposits",
        "Loans", "Non performing assets", "Tier-1 Capital", "Tier-2 capital", "Risk weighted assets",
    ]
    fin_df = peer_df[["Bank"] + fin_cols].set_index("Bank")
    st.dataframe(fin_df.style.format("{:,}"))

# ---------- Key Metrics -------------------------------------------------------
with st.expander("Key Metrics", expanded=True):
    st.subheader("Key Metrics – Ratio Analysis vs Market Avg")

    # Pre‑compute ratios
    ratio_df = peer_df.copy()
    ratio_df["core deposits to total deposits"] = ratio_df["Core Deposits"] / ratio_df["Total Deposits"]
    ratio_df["NPAs to total loans"] = ratio_df["Non performing assets"] / ratio_df["Loans"]
    ratio_df["liquidity ratio"] = ratio_df["Cash & cash equivalents"] / ratio_df["Total Assets"]
    ratio_df["capital adequacy ratio"] = (
        (ratio_df["Tier-1 Capital"] + ratio_df["Tier-2 capital"]) / ratio_df["Risk weighted assets"]
    )
    ratio_df["Solvency Ratio"] = ratio_df["Total Liabilities (excluding equity)"] / ratio_df["Total Assets"]
    ratio_df["loans to deposit ratio"] = ratio_df["Loans"] / ratio_df["Total Deposits"]

    ratio_options = [
        "core deposits to total deposits",
        "NPAs to total loans",
        "liquidity ratio",
        "capital adequacy ratio",
        "Solvency Ratio",
        "loans to deposit ratio",
    ]
    chosen_ratio = st.selectbox("Select Ratio", ratio_options)

    market_avg = ratio_df[chosen_ratio].mean()
    st.metric("Market Average", f"{market_avg: .2%}")

    fig = px.bar(
        ratio_df,
        x="Bank",
        y=chosen_ratio,
        title=f"{chosen_ratio.title()} – Bank vs Market",
        labels={chosen_ratio: "Ratio", "Bank": ""},
    )
    fig.add_hline(y=market_avg, line_dash="dot", annotation_text="Market Avg", annotation_position="outside top")
    st.plotly_chart(fig, use_container_width=True)

# ---------- CCAR Stress‑Test Analysis ----------------------------------------
with st.expander("CCAR Stress‑Test Analysis", expanded=True):
    st.subheader("CCAR Metrics vs Market Avg")

    ccar_cols = {
        "Common Equity Tier 1 Capital": "CET1_ratio",
        "Tier 1 Capital Ratio": "Tier1_ratio",
        "Total Capital": "Total_capital_ratio",
        "Leverage Ratio": "Leverage_ratio",
        "Supplementary Tier 1": "Supp_Tier1_ratio",
    }

    # Assume these ratio columns exist or are computable in the dataset
    for display, col in ccar_cols.items():
        if col not in peer_df.columns:
            peer_df[col] = np.nan  # placeholder if missing

    metric = st.selectbox("Select CCAR Metric", list(ccar_cols.keys()))
    metric_col = ccar_cols[metric]
    market_avg_ccar = peer_df[metric_col].mean(skipna=True)
    st.metric("Market Average", f"{market_avg_ccar: .2%}")

    fig2 = px.bar(
        peer_df,
        x="Bank",
        y=metric_col,
        title=f"{metric} – Bank vs Market",
        labels={metric_col: "Ratio", "Bank": ""},
    )
    fig2.add_hline(y=market_avg_ccar, line_dash="dot", annotation_text="Market Avg", annotation_position="outside top")
    st.plotly_chart(fig2, use_container_width=True)

# ---------- Summary -----------------------------------------------------------

st.markdown("---")
st.markdown(
    f"### Summary for **{selected_bank}**\n"
    f"- Coupon Rate: **{selected_bank_df['Coupon Rate (%)']:.2f}%**  \n"
    f"- Last Market Price (Flat): **{selected_bank_df['Flat Price']:.2f}**  \n"
    f"- Yield to Maturity: **{selected_bank_df['Yield to Maturity (YTC%)']:.2f}%**  \n"
    f"- Modified Duration: **{selected_bank_df['Modified Duration']:.3f} yr**  \n"
    f"- Capital Adequacy Ratio: **{selected_bank_df.get('capital adequacy ratio', np.nan):.2%}**"
)

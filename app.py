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

# bank_stacx_app.py  ── v2
"""
Bank Stacx 2.0 – Streamlit dashboard for peer‑to‑peer bank analytics
-------------------------------------------------------------------
This rev adds **robust file‑handling** so you don’t see the
`FileNotFoundError` again:
* If `Line items (1).xlsx` is present in the app folder, we load it.
* Otherwise we show a **file‑uploader** widget so you can drag‑and‑drop
  the file at run‑time.
* After upload, the file is cached in `st.session_state` so the page
  reloads never re‑ask for it.

To run locally:
```bash
pip install streamlit pandas numpy plotly openpyxl
streamlit run bank_stacx_app.py
```

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Bank Stacx 2.0", layout="wide")

DATA_FILE = Path("Line items (1).xlsx")

# ---------------------------
# Data loader with fallback
# ---------------------------
@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=0)

if "df_raw" not in st.session_state:
    if DATA_FILE.exists():
        st.session_state.df_raw = load_data(DATA_FILE)
    else:
        st.info("📄 Upload your **Line items (1).xlsx)** file to begin.")
        upload = st.file_uploader("Upload Excel", type=["xlsx", "xls"], key="u1")
        if upload:
            DATA_FILE.write_bytes(upload.getbuffer())  # persist to disk
            st.session_state.df_raw = load_data(DATA_FILE)
            st.success("File loaded – reload page if anything looks odd.")
            st.experimental_rerun()

# If still no data, stop here
if "df_raw" not in st.session_state:
    st.stop()

df_raw = st.session_state.df_raw

# ---------------------------
# Helpers
# ---------------------------
BANK_COL = "Bank"  # adjust if your column header differs

@st.cache_data(show_spinner=False)
def list_banks(df: pd.DataFrame):
    return sorted(df[BANK_COL].dropna().unique())

banks = list_banks(df_raw)
selected_bank = st.sidebar.selectbox("Select Bank", banks)
peer_count = st.sidebar.number_input("Peers (top N by assets)", 1, len(banks)-1, 3)

# Build peer set – simplistic: pick next N banks in list
sel_idx = banks.index(selected_bank)
peer_banks = banks[max(0, sel_idx - peer_count): sel_idx] + \
             banks[sel_idx + 1: sel_idx + 1 + peer_count]

peer_df = df_raw[df_raw[BANK_COL].isin([selected_bank] + peer_banks)].copy()

st.title("🏦 Bank Stacx 2.0 – Peer Comparison Dashboard")

# ---------------------------
# Key Financials Tab
# ---------------------------
fin_cols = [
    "PAT", "Depreciation", "Total Liabilities (excluding equity)",
    "Cash & cash equivalents", "Total Assets", "Current Assets",
    "Current Liabilities", "Accounts Receivables", "Marketable Securities",
    "Core Deposits", "Total Deposits", "Loans", "Non performing assets",
    "Tier-1 Capital", "Tier-2 capital", "Risk weighted assets",
]

with st.expander("📊 Key Financials (peer table)"):
    st.dataframe(peer_df[[BANK_COL] + fin_cols].set_index(BANK_COL))

# ---------------------------
# Key Metrics Tab
# ---------------------------
metric_defs = {
    "Core deposits / total deposits": lambda d: d["Core Deposits"] / d["Total Deposits"],
    "NPAs / total loans": lambda d: d["Non performing assets"] / d["Loans"],
    "Liquidity ratio": lambda d: d["Cash & cash equivalents"] / d["Current Liabilities"],
    "Capital adequacy ratio": lambda d: (d["Tier-1 Capital"] + d["Tier-2 capital"]) / d["Risk weighted assets"],
    "Solvency ratio": lambda d: d["Tier-1 Capital"] / d["Total Liabilities (excluding equity)"],
    "Loans / deposits": lambda d: d["Loans"] / d["Total Deposits"],
}

metric = st.selectbox("Choose metric", list(metric_defs.keys()))

peer_df[metric] = metric_defs[metric](peer_df)
sector_avg = peer_df[metric].mean()

fig = px.bar(peer_df, x=BANK_COL, y=metric, color=BANK_COL,
             title=f"{metric} vs Sector Avg ({sector_avg:.2%})",
             text=peer_df[metric].apply(lambda x: f"{x:.2%}"))
fig.add_hline(y=sector_avg, line_dash="dot", annotation_text="Sector Avg",
              annotation_position="top left")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# CCAR Stress‑Test Section
# ---------------------------
ccar_cols = [
    "Common Equity Tier 1 Capital", "Tier 1 Capital Ratio", "Total Capital",
    "Leverage Ratio", "Supplementary Tier 1",
]

with st.expander("🛡️ CCAR Stress‑Test Metrics"):
    st.dataframe(peer_df[[BANK_COL] + ccar_cols].set_index(BANK_COL))

# ---------------------------
# Narrative Summary
# ---------------------------
selected_metric_val = peer_df.loc[peer_df[BANK_COL]==selected_bank, metric].iloc[0]
of_sector = "above" if selected_metric_val > sector_avg else "below"

st.markdown(
    f"**Summary:** **{selected_bank}**’s **{metric}** is **{selected_metric_val:.2%}**, "
    f"which is **{of_sector}** the peer‑set average of **{sector_avg:.2%}**."
)
```


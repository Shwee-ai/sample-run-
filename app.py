import streamlit as st
import pandas as pd
from utils import data, metrics, plots

# Page configuration
st.set_page_config(
    page_title="BankStax 2.0",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🏦 BankStax 2.0")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    try:
        df = data.load_financial_data("Line items latest (1).xlsx")
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

df = load_data()

if df is not None:
    # Sidebar for bank selection
    st.sidebar.header("Bank Selection")
    selected_bank = st.sidebar.selectbox(
        "Choose a bank",
        data.get_bank_list(df)
    )

    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        "Key Financials", 
        "Key Metrics", 
        "CCAR Stress Test Analysis"
    ])

    # Tab 1: Key Financials
    with tab1:
        st.header("Key Financials")
        
        # Financial metrics dropdown
        financial_metrics = [
            'PAT', 'Depreciation', 'Total Liabilities', 'Cash',
            'Total Assets', 'Current Assets', 'Current Liabilities',
            'Accounts Receivables', 'Marketable Securities', 'Core Deposits',
            'Total Deposits', 'Loans', 'Non Performing Assets',
            'Tier 1 Capital', 'Tier 2 Capital', 'Risk Weighted Assets'
        ]
        
        selected_metric = st.selectbox(
            "Select Financial Metric",
            financial_metrics
        )
        
        # Create peer comparison chart
        fig = plots.create_peer_comparison_chart(
            df, selected_bank, selected_metric,
            f"{selected_metric} - Peer Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tab 2: Key Metrics
    with tab2:
        st.header("Key Metrics")
        
        # Calculate metrics for selected bank
        bank_metrics = metrics.calculate_key_metrics(df, selected_bank)
        
        # Mock market benchmarks (replace with actual data)
        market_benchmarks = {
            'core_deposits_ratio': 75.0,
            'npa_ratio': 2.0,
            'liquidity_ratio': 120.0,
            'capital_adequacy_ratio': 12.0,
            'solvency_ratio': 15.0,
            'loan_deposit_ratio': 80.0
        }
        
        # Create metrics dashboard
        fig = plots.create_key_metrics_dashboard(bank_metrics, market_benchmarks)
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics explanation
        with st.expander("Metrics Explanation"):
            st.markdown("""
            - **Core Deposits Ratio**: Measures the stability of funding sources
            - **NPA Ratio**: Indicates asset quality and credit risk
            - **Liquidity Ratio**: Measures ability to meet short-term obligations
            - **Capital Adequacy Ratio**: Shows bank's capital strength
            - **Solvency Ratio**: Indicates long-term financial stability
            - **Loan-Deposit Ratio**: Shows efficiency in converting deposits to loans
            """)

    # Tab 3: CCAR Stress Test Analysis
    with tab3:
        st.header("CCAR Stress Test Analysis")
        
        # Calculate stress test metrics
        stress_metrics = metrics.calculate_stress_test_metrics(
            df[df['Company'] == selected_bank].iloc[0]
        )
        
        # Mock market benchmarks for stress tests (replace with actual data)
        stress_benchmarks = {
            'cet1_ratio': 7.0,
            'tier1_capital_ratio': 8.5,
            'total_capital_ratio': 10.5,
            'leverage_ratio': 4.0
        }
        
        # Create stress test dashboard
        fig = plots.create_stress_test_dashboard(stress_metrics, stress_benchmarks)
        st.plotly_chart(fig, use_container_width=True)
        
        # Stress test explanation
        with st.expander("Stress Test Metrics Explanation"):
            st.markdown("""
            - **CET1 Ratio**: Core measure of bank's financial strength
            - **Tier 1 Capital Ratio**: Measures bank's core equity capital
            - **Total Capital Ratio**: Overall capital adequacy measure
            - **Leverage Ratio**: Indicates bank's ability to meet financial obligations
            """)

else:
    st.error("Unable to load data. Please check the data file and try again.")

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit | Data source: Financial Statements"
)

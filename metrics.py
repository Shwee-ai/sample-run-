def calculate_key_metrics(df, bank_name):
    """
    Calculate key financial metrics for a specific bank
    """
    bank_data = df[df['Company'] == bank_name].iloc[0]
    
    metrics = {
        'core_deposits_ratio': calculate_core_deposits_ratio(bank_data),
        'npa_ratio': calculate_npa_ratio(bank_data),
        'liquidity_ratio': calculate_liquidity_ratio(bank_data),
        'capital_adequacy_ratio': calculate_capital_adequacy_ratio(bank_data),
        'solvency_ratio': calculate_solvency_ratio(bank_data),
        'loan_deposit_ratio': calculate_loan_deposit_ratio(bank_data)
    }
    
    return metrics

def calculate_core_deposits_ratio(bank_data):
    """
    Calculate core deposits to total deposits ratio
    """
    try:
        return (bank_data['Core Deposits'] / bank_data['Total Deposits']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_npa_ratio(bank_data):
    """
    Calculate Non-Performing Assets to total loans ratio
    """
    try:
        return (bank_data['Non Performing Assets'] / bank_data['Loans']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_liquidity_ratio(bank_data):
    """
    Calculate liquidity ratio (Current Assets / Current Liabilities)
    """
    try:
        return (bank_data['Current Assets'] / bank_data['Current Liabilities']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_capital_adequacy_ratio(bank_data):
    """
    Calculate Capital Adequacy Ratio (CAR)
    (Tier 1 Capital + Tier 2 Capital) / Risk Weighted Assets
    """
    try:
        total_capital = bank_data['Tier 1 Capital'] + bank_data['Tier 2 Capital']
        return (total_capital / bank_data['Risk Weighted Assets']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_solvency_ratio(bank_data):
    """
    Calculate Solvency Ratio
    (Net Income + Depreciation) / Total Liabilities
    """
    try:
        return ((bank_data['PAT'] + bank_data['Depreciation']) / 
                bank_data['Total Liabilities']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_loan_deposit_ratio(bank_data):
    """
    Calculate Loan to Deposit ratio
    """
    try:
        return (bank_data['Loans'] / bank_data['Total Deposits']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_stress_test_metrics(bank_data):
    """
    Calculate CCAR Stress Test metrics
    """
    return {
        'cet1_ratio': calculate_cet1_ratio(bank_data),
        'tier1_capital_ratio': calculate_tier1_capital_ratio(bank_data),
        'total_capital_ratio': calculate_total_capital_ratio(bank_data),
        'leverage_ratio': calculate_leverage_ratio(bank_data)
    }

def calculate_cet1_ratio(bank_data):
    """
    Calculate Common Equity Tier 1 (CET1) ratio
    """
    try:
        return (bank_data['CET1 Ratio']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_tier1_capital_ratio(bank_data):
    """
    Calculate Tier 1 Capital ratio
    """
    try:
        return (bank_data['Tier 1 Capital'] / bank_data['Risk Weighted Assets']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_total_capital_ratio(bank_data):
    """
    Calculate Total Capital ratio
    """
    try:
        total_capital = bank_data['Tier 1 Capital'] + bank_data['Tier 2 Capital']
        return (total_capital / bank_data['Risk Weighted Assets']) * 100
    except (KeyError, ZeroDivisionError):
        return None

def calculate_leverage_ratio(bank_data):
    """
    Calculate Leverage ratio
    """
    try:
        return (bank_data['Tier 1 Capital'] / bank_data['Total Assets']) * 100
    except (KeyError, ZeroDivisionError):
        return None

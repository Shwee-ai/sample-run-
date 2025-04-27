import pandas as pd

def load_financial_data(file_path):
    """
    Load and process financial data from Excel file
    """
    try:
        df = pd.read_excel(file_path)
        
        # Rename columns based on first row
        df.columns = ['Company', 'PAT', 'Depreciation', 'Total Liabilities', 'Cash', 
                     'Total Assets', 'Current Assets', 'Current Liabilities', 
                     'Accounts Receivables', 'Marketable Securities', 'Core Deposits',
                     'Total Deposits', 'Loans', 'Non Performing Assets', 'Tier 1 Capital',
                     'Tier 2 Capital', 'Risk Weighted Assets', 'CET1 Ratio', 
                     'Tier 1 Capital Ratio', 'Total Capital Ratio', 'Leverage Ratio',
                     'Supplementary Tier 1', 'Capital Conservation']
        
        # Remove the header row since we've used it for column names
        df = df[df['Company'] != 'Company']
        
        return df
    except Exception as e:
        raise Exception(f"Error loading financial data: {str(e)}")

def get_bank_list(df):
    """
    Get list of banks for dropdown selection
    """
    return sorted(df['Company'].unique().tolist())

def get_peer_comparison(df, bank_name, metric):
    """
    Get peer comparison data for a specific bank and metric
    """
    if bank_name not in df['Company'].values:
        return None
    
    return {
        'selected_bank': df[df['Company'] == bank_name][metric].values[0],
        'peer_average': df[df['Company'] != bank_name][metric].mean(),
        'peer_max': df[df['Company'] != bank_name][metric].max(),
        'peer_min': df[df['Company'] != bank_name][metric].min()
    }

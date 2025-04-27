import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def create_peer_comparison_chart(df, bank_name, metric, title):
    """
    Create a bar chart comparing a bank's metric with peer average
    """
    bank_value = df[df['Company'] == bank_name][metric].values[0]
    peer_avg = df[df['Company'] != bank_name][metric].mean()
    
    fig = go.Figure()
    
    # Add bar for selected bank
    fig.add_trace(go.Bar(
        x=['Selected Bank'],
        y=[bank_value],
        name=bank_name,
        marker_color='#1f77b4'
    ))
    
    # Add bar for peer average
    fig.add_trace(go.Bar(
        x=['Peer Average'],
        y=[peer_avg],
        name='Peer Average',
        marker_color='#ff7f0e'
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title=metric,
        showlegend=True,
        template='plotly_white',
        height=400
    )
    
    return fig

def create_metric_trend_chart(df, bank_name, metric, market_avg, title):
    """
    Create a line chart showing metric trend with market comparison
    """
    fig = go.Figure()
    
    # Add line for selected bank
    fig.add_trace(go.Scatter(
        x=df[df['Company'] == bank_name]['Date'],
        y=df[df['Company'] == bank_name][metric],
        name=bank_name,
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Add market comparison line
    fig.add_trace(go.Scatter(
        x=df['Date'].unique(),
        y=[market_avg] * len(df['Date'].unique()),
        name='Market Average',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=metric,
        showlegend=True,
        template='plotly_white',
        height=400
    )
    
    return fig

def create_stress_test_dashboard(stress_metrics, market_benchmarks):
    """
    Create a comprehensive stress test visualization dashboard
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'CET1 Ratio',
            'Tier 1 Capital Ratio',
            'Total Capital Ratio',
            'Leverage Ratio'
        )
    )
    
    metrics = [
        ('CET1 Ratio', 'CET1 Ratio'),
        ('Tier 1 Capital Ratio', 'Tier 1 Capital Ratio'),
        ('Total Capital Ratio', 'Total Capital Ratio'),
        ('Leverage Ratio', 'Leverage Ratio')
    ]
    
    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    
    for (metric, title), (row, col) in zip(metrics, positions):
        # Add bank's metric
        fig.add_trace(
            go.Indicator(
                mode='gauge+number',
                value=stress_metrics[metric],
                title={'text': title},
                gauge={
                    'axis': {'range': [None, max(stress_metrics[metric], 
                                                market_benchmarks[metric]) * 1.2]},
                    'threshold': {
                        'line': {'color': 'red', 'width': 2},
                        'thickness': 0.75,
                        'value': market_benchmarks[metric]
                    }
                }
            ),
            row=row, col=col
        )
    
    fig.update_layout(
        height=800,
        showlegend=False,
        template='plotly_white',
        title_text='CCAR Stress Test Analysis'
    )
    
    return fig

def create_key_metrics_dashboard(metrics_data, market_benchmarks):
    """
    Create a dashboard showing all key metrics with market comparisons
    """
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Core Deposits Ratio',
            'NPA Ratio',
            'Liquidity Ratio',
            'Capital Adequacy Ratio',
            'Solvency Ratio',
            'Loan-Deposit Ratio'
        )
    )
    
    metrics = [
        ('core_deposits_ratio', 'Core Deposits/Total Deposits'),
        ('npa_ratio', 'NPAs/Total Loans'),
        ('liquidity_ratio', 'Liquidity Ratio'),
        ('capital_adequacy_ratio', 'CAR'),
        ('solvency_ratio', 'Solvency Ratio'),
        ('loan_deposit_ratio', 'Loans/Deposits')
    ]
    
    positions = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)]
    
    for (metric, title), (row, col) in zip(metrics, positions):
        fig.add_trace(
            go.Indicator(
                mode='gauge+number',
                value=metrics_data[metric],
                title={'text': title},
                gauge={
                    'axis': {'range': [None, max(metrics_data[metric], 
                                                market_benchmarks[metric]) * 1.2]},
                    'threshold': {
                        'line': {'color': 'red', 'width': 2},
                        'thickness': 0.75,
                        'value': market_benchmarks[metric]
                    }
                }
            ),
            row=row, col=col
        )
    
    fig.update_layout(
        height=1200,
        showlegend=False,
        template='plotly_white',
        title_text='Key Metrics Dashboard'
    )
    
    return fig

"""
Reusable Streamlit Components for the Intelligent Cost Database Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta


def render_kpi_card(label: str, value: str, metric: str = None, delta: str = None):
    """
    Render a KPI metric card with optional delta indicator.
    
    Args:
        label: Card title
        value: Main metric value
        metric: Optional metric description
        delta: Optional percentage change (e.g., "+5.2%")
    """
    col_style = """
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    ">
        <p style="margin: 0; font-size: 14px; opacity: 0.9; font-weight: 500;">{}</p>
        <h2 style="margin: 10px 0 0 0; font-size: 32px; font-weight: 700;">{}</h2>
        {}
    </div>
    """.format(
        label,
        value,
        f'<p style="margin: 8px 0 0 0; font-size: 12px; opacity: 0.8;">{delta}</p>'
        if delta else ''
    )
    st.markdown(col_style, unsafe_allow_html=True)


def render_metric_box(col, label: str, value: str, icon: str = "📊"):
    """
    Render a single metric box in a column.
    """
    with col:
        metric_html = f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        ">
            <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
            <div style="font-size: 12px; opacity: 0.9; margin-bottom: 5px;">{label}</div>
            <div style="font-size: 24px; font-weight: 700;">{value}</div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)


def render_comparison_table(df: pd.DataFrame, title: str = "Item Comparison"):
    """
    Render a styled comparison table.
    """
    st.subheader(title)
    
    # Add a bit of styling to the table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            col: st.column_config.TextColumn()
            for col in df.columns
        }
    )


def render_price_trend_chart(analytics_df: pd.DataFrame):
    """
    Create an interactive price trend line chart.
    """
    # Simulate time-series data based on item codes
    trend_data = analytics_df[analytics_df['trend_direction'] != 'down'].copy()
    
    fig = go.Figure()
    
    for item in trend_data['canonical_item_name'].unique():
        item_data = trend_data[trend_data['canonical_item_name'] == item]
        
        # Create price progression based on trend
        months = pd.date_range(start='2024-01', end='2024-07', freq='MS')
        
        if item_data['trend_direction'].iloc[0] == 'up':
            prices = [float(item_data['min_price'].iloc[0]) * (1 + 0.02 * i) for i in range(len(months))]
        elif item_data['trend_direction'].iloc[0] == 'down':
            prices = [float(item_data['max_price'].iloc[0]) * (1 - 0.015 * i) for i in range(len(months))]
        else:
            prices = [float(item_data['avg_price'].iloc[0])] * len(months)
        
        fig.add_trace(
            go.Scatter(
                x=months,
                y=prices,
                mode='lines+markers',
                name=item,
                line=dict(width=2),
                marker=dict(size=6)
            )
        )
    
    fig.update_layout(
        title="Price Trends Over Time (6 Months)",
        xaxis_title="Month",
        yaxis_title="Unit Price (₹)",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        font=dict(family="Segoe UI, sans-serif"),
    )
    
    return fig


def render_regional_comparison(analytics_df: pd.DataFrame):
    """
    Create a bar chart comparing prices by region.
    """
    region_avg = analytics_df.groupby('region')['avg_price'].mean().reset_index()
    region_avg = region_avg.sort_values('avg_price', ascending=False)
    
    fig = px.bar(
        region_avg,
        x='region',
        y='avg_price',
        title="Average Item Price by Region",
        labels={'region': 'Region', 'avg_price': 'Average Price (₹)'},
        color='avg_price',
        color_continuous_scale='Blues',
        height=350
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        font=dict(family="Segoe UI, sans-serif"),
    )
    
    return fig


def render_supplier_comparison(analytics_df: pd.DataFrame):
    """
    Create a bar chart comparing top suppliers by order count.
    """
    supplier_stats = analytics_df.groupby('supplier').agg({
        'avg_price': 'mean',
    }).reset_index().sort_values('avg_price', ascending=True)
    
    top_suppliers = supplier_stats.head(10)
    
    fig = px.bar(
        top_suppliers,
        y='supplier',
        x='avg_price',
        orientation='h',
        title="Top Suppliers by Average Price",
        labels={'supplier': 'Supplier', 'avg_price': 'Average Price (₹)'},
        color='avg_price',
        color_continuous_scale='Viridis',
        height=400
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        font=dict(family="Segoe UI, sans-serif"),
    )
    
    return fig


def render_confidence_progress(confidence_scores: list):
    """
    Render confidence score distribution as progress bars.
    """
    fig = go.Figure()
    
    score_ranges = ['90-100%', '80-90%', '70-80%', '60-70%']
    counts = [
        len([s for s in confidence_scores if s >= 0.9]),
        len([s for s in confidence_scores if 0.8 <= s < 0.9]),
        len([s for s in confidence_scores if 0.7 <= s < 0.8]),
        len([s for s in confidence_scores if 0.6 <= s < 0.7]),
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            y=score_ranges,
            x=counts,
            orientation='h',
            marker=dict(color=['#27AE60', '#F39C12', '#E74C3C', '#95A5A6']),
            text=counts,
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Standardization Confidence Distribution",
        xaxis_title="Count",
        yaxis_title="Confidence Range",
        height=300,
        template='plotly_white',
        showlegend=False,
        font=dict(family="Segoe UI, sans-serif"),
    )
    
    return fig


def render_anomaly_highlight(anomaly_df: pd.DataFrame):
    """
    Render anomaly data with color highlighting.
    """
    if anomaly_df.empty:
        st.info("✓ No anomalies detected in this dataset!")
        return
    
    # Add severity badge
    def get_severity_color(reason: str):
        if 'CRITICAL' in reason.upper():
            return '🔴'
        elif any(pct in reason for pct in ['40%', '50%', '60%']):
            return '🟠'
        else:
            return '🟡'
    
    anomaly_df = anomaly_df.copy()
    anomaly_df['Severity'] = anomaly_df['anomaly_reason'].apply(get_severity_color)
    
    # Display as table
    display_cols = ['Severity', 'po_id', 'item_code', 'unit_price', 'expected_price', 'anomaly_reason']
    st.dataframe(
        anomaly_df[display_cols],
        use_container_width=True,
        hide_index=True
    )


def render_prediction_chart(analytics_df: pd.DataFrame):
    """
    Render a price prediction chart (next 3 months).
    """
    # Get items with trend data
    trend_items = analytics_df[analytics_df['trend_direction'] != 'down'].copy().head(5)
    
    if trend_items.empty:
        st.info("No items with growth trends to forecast.")
        return
    
    fig = go.Figure()
    
    # Historical data (months 1-6)
    months_hist = pd.date_range(start='2024-01', end='2024-06', freq='MS')
    
    # Future months (dashed line)
    months_future = pd.date_range(start='2024-05', end='2024-09', freq='MS')
    
    for _, item in trend_items.iterrows():
        # Historical prices
        if item['trend_direction'] == 'up':
            hist_prices = [float(item['min_price']) * (1 + 0.02 * i) for i in range(6)]
            fut_prices = [hist_prices[-1] * (1 + 0.02 * (i + 1)) for i in range(4)]
        else:
            hist_prices = [float(item['avg_price'])] * 6
            fut_prices = [float(item['avg_price'])] * 4
        
        # Historical trace
        fig.add_trace(
            go.Scatter(
                x=months_hist,
                y=hist_prices,
                mode='lines+markers',
                name=item['canonical_item_name'],
                line=dict(width=2),
            )
        )
        
        # Prediction trace (dashed)
        fig.add_trace(
            go.Scatter(
                x=months_future,
                y=fut_prices,
                mode='lines+markers',
                name=f"{item['canonical_item_name']} (Forecast)",
                line=dict(width=2, dash='dash'),
                marker=dict(symbol='diamond'),
            )
        )
    
    fig.update_layout(
        title="Price Forecast - Next 3 Months",
        xaxis_title="Month",
        yaxis_title="Unit Price (₹)",
        hovermode='x unified',
        template='plotly_white',
        height=400,
        font=dict(family="Segoe UI, sans-serif"),
    )
    
    return fig


def render_search_box(placeholder: str = "Search items..."):
    """
    Render a styled search input box.
    """
    return st.text_input(
        label="🔍 Search Items",
        placeholder=placeholder,
        key="search_box",
        help="Type item name, code, or supplier to filter results"
    )


def render_copy_button(text: str, label: str = "📋 Copy"):
    """
    Render a copy-to-clipboard button.
    """
    return st.button(label, key=f"copy_{text}", help=f"Copy '{text}' to clipboard")


def apply_custom_css():
    """
    Apply custom CSS styling to the entire app.
    """
    css = """
    <style>
    /* Global Styles */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f8f9fa;
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    /* Tab Styling */
    .streamlit-tabs {
        background: white;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Alert Styling */
    .alert-critical {
        background-color: #fee;
        border-left: 4px solid #c33;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    
    .alert-warning {
        background-color: #ffeaa7;
        border-left: 4px solid #f39c12;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    
    .alert-success {
        background-color: #d4edda;
        border-left: 4px solid #27ae60;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSidebar [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    /* Heading */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 700;
    }
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

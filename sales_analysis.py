import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def load_data(file):
    df = pd.read_csv(file, parse_dates=['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    return df

def get_top_products(df):
    return df.groupby('Product')['Quantity'].sum().sort_values(ascending=False).head(5)

def get_monthly_revenue(df):
    return df.groupby(df['Month'].astype(str))['Revenue'].sum()

def get_total_summary(df):
    total_revenue = df['Revenue'].sum()
    avg_monthly = df.groupby(df['Month'].astype(str))['Revenue'].sum().mean()
    return total_revenue, avg_monthly

def create_visualizations(df):
    charts = {}
    
    # Monthly Revenue Trend
    monthly_revenue = df.groupby('Month')['Revenue'].sum().reset_index()
    monthly_revenue['Month'] = monthly_revenue['Month'].astype(str)
    charts['revenue_trend'] = px.line(
        monthly_revenue, 
        x='Month', 
        y='Revenue',
        title='Monthly Revenue Trend',
        template='plotly_white'
    )

    # Product Performance
    product_perf = df.groupby('Product').agg({
        'Revenue': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    charts['product_performance'] = px.scatter(
        product_perf,
        x='Quantity',
        y='Revenue',
        size='Revenue',
        color='Product',
        title='Product Performance Analysis',
        template='plotly_white'
    )

    # Daily Sales Pattern
    daily_sales = df.groupby('Date')['Revenue'].sum().reset_index()
    charts['daily_pattern'] = px.line(
        daily_sales,
        x='Date',
        y='Revenue',
        title='Daily Sales Pattern',
        template='plotly_white'
    )

    # Product Revenue Distribution
    product_revenue = df.groupby('Product')['Revenue'].sum()
    charts['revenue_distribution'] = px.pie(
        values=product_revenue.values,
        names=product_revenue.index,
        title='Revenue Distribution by Product'
    )

    # Monthly Quantity Trend
    monthly_qty = df.groupby([df['Month'].astype(str), 'Product'])['Quantity'].sum().reset_index()
    charts['quantity_trend'] = px.bar(
        monthly_qty,
        x='Month',
        y='Quantity',
        color='Product',
        title='Monthly Sales Quantity by Product',
        barmode='group'
    )

    return charts

def generate_insights(df):
    insights = []
    
    # Revenue Growth
    monthly_revenue = df.groupby('Month')['Revenue'].sum()
    growth = ((monthly_revenue.iloc[-1] - monthly_revenue.iloc[0]) / monthly_revenue.iloc[0]) * 100
    insights.append(f"Revenue Growth: {growth:.1f}%")

    # Best Selling Product
    best_product = df.groupby('Product')['Quantity'].sum().idxmax()
    best_qty = df.groupby('Product')['Quantity'].sum().max()
    insights.append(f"Best Selling Product: {best_product} ({best_qty:.0f} units)")

    # Highest Revenue Day
    best_day = df.groupby('Date')['Revenue'].sum().idxmax()
    max_revenue = df.groupby('Date')['Revenue'].sum().max()
    insights.append(f"Best Revenue Day: {best_day.strftime('%Y-%m-%d')} (₹{max_revenue:.2f})")

    return insights
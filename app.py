import streamlit as st
from sales_analysis import (
    load_data, get_top_products, get_monthly_revenue, 
    get_total_summary, create_visualizations, generate_insights
)
from forecast import forecast_next_month
from gemini_agent import setup_gemini, generate_summary

st.set_page_config(page_title="Sales Summary & Forecast AI", layout="wide")

st.title("📊 Sales Summary & Forecast AI Agent")

api_key = st.text_input("Enter your Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file and api_key:
    try:
        setup_gemini(api_key)
        df = load_data(uploaded_file)

        # Key Metrics
        col1, col2, col3 = st.columns(3)
        total_revenue, avg_monthly = get_total_summary(df)
        with col1:
            st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
        with col2:
            st.metric("Avg Monthly Revenue", f"₹{avg_monthly:,.2f}")
        with col3:
            prediction = forecast_next_month(get_monthly_revenue(df))
            st.metric("Next Month Forecast", f"₹{prediction:,.2f}")

        # Visualizations
        charts = create_visualizations(df)
        
        # Revenue Trends
        st.subheader("📈 Revenue Analysis")
        tab1, tab2 = st.tabs(["Monthly Trend", "Daily Pattern"])
        with tab1:
            st.plotly_chart(charts['revenue_trend'], use_container_width=True)
        with tab2:
            st.plotly_chart(charts['daily_pattern'], use_container_width=True)

        # Product Analysis
        st.subheader("🏆 Product Performance")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(charts['product_performance'], use_container_width=True)
        with col2:
            st.plotly_chart(charts['revenue_distribution'], use_container_width=True)

        # Quantity Analysis
        st.subheader("📦 Sales Quantity Analysis")
        st.plotly_chart(charts['quantity_trend'], use_container_width=True)

        # Key Insights
        st.subheader("💡 Key Insights")
        insights = generate_insights(df)
        for insight in insights:
            st.info(insight)

        # AI Summary
        st.subheader("🤖 AI Business Summary")
        ai_summary = generate_summary(get_monthly_revenue(df), get_top_products(df))
        st.write(ai_summary)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a sales CSV file and enter your Gemini API key to begin analysis.")
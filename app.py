import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
#  model = genai.GenerativeModel('models/gemini-2.5-flash')
from sales_analysis import (
    load_data, get_top_products, get_monthly_revenue, 
    get_total_summary, create_visualizations, generate_insights
)
from forecast import forecast_next_month, forecast_with_confidence
from gemini_agent import (
    setup_gemini, generate_summary, generate_product_recommendations,
    generate_seasonal_insights, generate_customer_segments
)

# PDF Generator
def create_pdf(report_text):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    
    y = height - 40
    for line in report_text.split("\n"):
        p.drawString(40, y, line)
        y -= 15
        if y < 40:  
            p.showPage()
            y = height - 40

    p.save()
    buffer.seek(0)
    return buffer.getvalue()

# Streamlit App 
st.set_page_config(page_title="Sales Summary & Forecast AI", layout="wide")
st.title("📊 Sales Summary & Forecast AI Agent")

# Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Key", type="password")
    uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv"])
    
    if api_key and uploaded_file:
        st.success("✅ Ready to analyze!")

if uploaded_file and api_key:
    try:
        setup_gemini(api_key)
        df = load_data(uploaded_file)

        # Dashboard Tabs
        tab_main, tab_products, tab_forecast, tab_ai = st.tabs([
            "📈 Overview", "🎯 Products", "🔮 Forecast", "🤖 AI Insights"
        ])

        with tab_main:
            # Key Metrics
            st.subheader("Key Performance Indicators")
            col1, col2, col3, col4 = st.columns(4)
            total_revenue, avg_monthly = get_total_summary(df)
            with col1:
                st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
            with col2:
                st.metric("Avg Monthly Revenue", f"₹{avg_monthly:,.2f}")
            with col3:
                prediction = forecast_next_month(get_monthly_revenue(df))
                st.metric("Next Month Forecast", f"₹{prediction:,.2f}")
            with col4:
                growth = ((total_revenue - avg_monthly) / avg_monthly) * 100
                st.metric("Growth Rate", f"{growth:.1f}%")

            # Revenue Trends
            charts = create_visualizations(df)
            st.plotly_chart(charts['revenue_trend'], use_container_width=True)
            st.plotly_chart(charts['daily_pattern'], use_container_width=True)

        with tab_products:
            st.subheader("Product Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(charts['product_performance'], use_container_width=True)
            with col2:
                st.plotly_chart(charts['revenue_distribution'], use_container_width=True)

            st.subheader("Product Recommendations")
            recommendations = generate_product_recommendations(df)
            st.write(recommendations)

            st.plotly_chart(charts['quantity_trend'], use_container_width=True)

        with tab_forecast:
            st.subheader("Sales Forecast")
            forecast_period = st.slider("Forecast Period (months)", 1, 6, 3)
            prediction, (lower, upper) = forecast_with_confidence(get_monthly_revenue(df))
            
            st.metric("Next Month Prediction", f"₹{prediction:,.2f}")
            st.caption(f"Confidence Interval: ₹{lower:,.2f} - ₹{upper:,.2f}")

            seasonal_insights = generate_seasonal_insights(df)
            st.write(seasonal_insights)

        with tab_ai:
            st.subheader("AI-Powered Insights")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Executive Summary")
                ai_summary = generate_summary(get_monthly_revenue(df), get_top_products(df))
                st.write(ai_summary)
            
            with col2:
                st.subheader("Customer Segments")
                segments = generate_customer_segments(df)
                st.write(segments)

            # Key Insights
            st.subheader("💡 Key Insights")
            insights = generate_insights(df)
            cols = st.columns(len(insights))
            for col, insight in zip(cols, insights):
                with col:
                    st.info(insight)

        # Download Report
        st.sidebar.subheader("Export Report")
        if st.sidebar.button("Generate Report"):
            report_data = {
                "Executive Summary": ai_summary,
                "Product Recommendations": recommendations,
                "Seasonal Insights": seasonal_insights,
                "Customer Segments": segments,
                "Key Metrics": f"Total Revenue: ₹{total_revenue:,.2f}\nAvg Monthly: ₹{avg_monthly:,.2f}\nForecast: ₹{prediction:,.2f}"
            }
            
            report_text = "\n\n".join([f"{title}\n{content}" for title, content in report_data.items()])
            pdf_bytes = create_pdf(report_text)

            st.sidebar.download_button(
                label="Download Full Report",
                data=pdf_bytes,
                file_name="sales_analysis_report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a sales CSV file to begin analysis.")

import google.generativeai as genai

def setup_gemini(api_key):
    genai.configure(api_key=api_key)

def generate_summary(monthly_revenue, top_products):
    prompt = f"""
Act as a professional business analyst.
Analyze the monthly revenue data and top-selling products provided below:

Monthly Revenue (INR): {monthly_revenue.to_dict()}
Top-Selling Products: {top_products.to_dict()}

Generate a sharp and engaging 4-sentence executive summary highlighting:
- Revenue growth or decline trends
- Best-performing products
- Any seasonality or monthly patterns
- A final insight that can help guide future sales strategy

Keep the tone confident, analytical, and suitable for a business review report.
"""
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

def generate_product_recommendations(df):
    product_data = df.groupby('Product').agg({
        'Quantity': ['sum', 'mean'],
        'Revenue': ['sum', 'mean']
    }).round(2)
    
    prompt = f"""
Analyze this product performance data and provide 3 specific recommendations:
{product_data.to_string()}

Consider:
1. Which products need inventory optimization?
2. Which products could benefit from promotions?
3. Which products show growth potential?

Format as bullet points with clear, actionable insights.
"""
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

def generate_seasonal_insights(df):
    seasonal_data = df.copy()
    seasonal_data['Month'] = df['Date'].dt.month
    seasonal_summary = seasonal_data.groupby('Month').agg({
        'Revenue': ['sum', 'mean'],
        'Quantity': ['sum', 'mean']
    }).round(2)

    prompt = f"""
Analyze this seasonal sales data and identify key patterns:
{seasonal_summary.to_string()}

Provide insights on:
1. Peak sales seasons
2. Low-performance periods
3. Seasonal product trends
4. Inventory planning recommendations

Format as clear, actionable bullet points.
"""
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

def generate_customer_segments(df):
    product_metrics = df.groupby('Product').agg({
        'Revenue': ['mean', 'std'],
        'Quantity': ['mean', 'std']
    }).round(2)

    prompt = f"""
Based on this product purchase behavior:
{product_metrics.to_string()}

Suggest customer segments and targeting strategies:
1. Identify premium vs value segments
2. Suggest product bundles
3. Recommend cross-selling opportunities
4. Propose loyalty program features

Provide practical, actionable recommendations.
"""
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text
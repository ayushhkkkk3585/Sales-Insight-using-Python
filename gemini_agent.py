import google.generativeai as genai

def setup_gemini(api_key):
    genai.configure(api_key=api_key)

def generate_summary(monthly_revenue, top_products):
    prompt = f"""
Act as a professional business analyst.

Analyze the monthly revenue data and top-selling products provided below:

Monthly Revenue (INR): {monthly_revenue.to_dict()}
Top-Selling Products: {top_products.to_dict()}

Your goal is to generate a sharp and engaging 4-sentence executive summary. Highlight:
- Revenue growth or decline trends
- Best-performing products
- Any seasonality or monthly patterns
- A final insight that can help guide future sales strategy

Keep the tone confident, analytical, and suitable for a business review report.
"""
    model = genai.GenerativeModel('models/gemini-2.5-flash')  # gemini-2.5 is not supported via API yet
    response = model.generate_content(prompt)
    return response.text
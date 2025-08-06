from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_next_month(monthly_revenue):
    months = list(range(len(monthly_revenue)))
    X = np.array(months).reshape(-1, 1)
    y = monthly_revenue.values

    model = LinearRegression()
    model.fit(X, y)

    next_month = np.array([[len(months)]])
    predicted = model.predict(next_month)[0]
    return round(predicted, 2)
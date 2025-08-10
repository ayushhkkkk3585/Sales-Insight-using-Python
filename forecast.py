from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
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

def forecast_with_confidence(monthly_revenue):
    months = list(range(len(monthly_revenue)))
    X = np.array(months).reshape(-1, 1)
    y = monthly_revenue.values

    # Split data for validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Calculate prediction
    next_month = np.array([[len(months)]])
    predicted = model.predict(next_month)[0]

    # Calculate confidence 
    y_pred = model.predict(X_test)
    mse = np.mean((y_test - y_pred) ** 2)
    std = np.sqrt(mse)
    
    lower_bound = predicted - 1.96 * std
    upper_bound = predicted + 1.96 * std

    return round(predicted, 2), (round(lower_bound, 2), round(upper_bound, 2))
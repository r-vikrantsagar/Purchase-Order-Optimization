import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

def RecommendPrice(item_ID, data_path, Time, Date):
    # Load the dataset
    data = pd.read_csv(data_path)
    print("Data loaded successfully.")
    data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')
    
    # Filtering data to item_ID and specific date
    filtered_data = data[(data['sku_id'] == item_ID) & (data['date'] == pd.to_datetime(Date, format='%d-%m-%Y'))].copy()
    
    if filtered_data.empty:
        item_data = data[data['sku_id'] == item_ID]
        median_price = item_data['price'].median() if not item_data.empty else None
        return {'Optimal Price': median_price}

    # Feature selection and preparing data
    features = ['price', 'cost']
    target = 'sales'

    # Check for columns with all missing values and handle them
    if filtered_data[features].isna().all().any() or filtered_data[target].isna().all():
        p_price = filtered_data['price'].median()
        return {'Optimal Price': p_price}

    # Impute missing values if not all values are missing
    imputer = SimpleImputer(strategy='median')
    filtered_data.loc[:, features] = imputer.fit_transform(filtered_data[features])
    y = imputer.fit_transform(filtered_data[target].values.reshape(-1, 1)).flatten()

    scaler = MinMaxScaler()
    X = scaler.fit_transform(filtered_data[features])
    
    # Consistency check
    if len(X) != len(y):
        median_price = filtered_data['price'].median()
        return {'Optimal Price': median_price}

    # Model training
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    X_train, X_test, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    print("Model trained successfully.")

    # Predicting and calculating profits
    predicted_sales = model.predict(X)
    profits = (filtered_data['price'].values - filtered_data['cost'].values) * predicted_sales
    
    if np.all(profits <= 0):
        median_price = filtered_data['price'].median()
        return {'Optimal Price': median_price}

    # Create a DataFrame for sorting and selecting top result
    results_df = pd.DataFrame({
        'price': filtered_data['price'],
        'cost': filtered_data['cost'],
        'profit': profits
    })
    
    # Get the highest profit result
    optimal_result = results_df.loc[results_df['profit'].idxmax()]

    return {'Optimal Price': optimal_result['price']}

# -*- coding: utf-8 -*-
"""cse frend nm project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sl6g1QodLoX7Q_fk40SSpw99parUCakN
"""

!pip install termcolor

# 📦 Required packages
!pip install termcolor

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from termcolor import colored

# 🗂️ Load your AQI dataset
df = pd.read_csv('city_day.csv')  # Replace with your CSV filename

# ✅ Set the city and number of days you want to predict
city_input = "Delhi"
num_days = 7

# 🧹 Filter for the selected city and clean data
city_df = df[df['City'].str.lower() == city_input.lower()].copy()
city_df = city_df[['Date', 'AQI']].dropna()
city_df['Date'] = pd.to_datetime(city_df['Date'])
city_df = city_df.sort_values('Date')

# 🧠 Feature engineering (lagging previous 3 days)
aqi_df = city_df[['Date', 'AQI']].copy()
aqi_df['AQI_1'] = aqi_df['AQI'].shift(1)
aqi_df['AQI_2'] = aqi_df['AQI'].shift(2)
aqi_df['AQI_3'] = aqi_df['AQI'].shift(3)
aqi_df = aqi_df.dropna()

# 🧪 Prepare training and test data
X = aqi_df[['AQI_1', 'AQI_2', 'AQI_3']]
y = aqi_df['AQI']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 🧠 Train model
model = LinearRegression()
model.fit(X_train, y_train)

# 🔮 Predict future AQI values
last_known_values = list(aqi_df['AQI'].values[-3:])
future_predictions = []

for _ in range(num_days):
    input_features = np.array(last_known_values[-3:]).reshape(1, -1)
    next_aqi = model.predict(input_features)[0]
    future_predictions.append(next_aqi)
    last_known_values.append(next_aqi)

# 🎨 Define AQI category with colors
def get_aqi_category(aqi):
    if aqi <= 50:
        return colored("Good", "green")
    elif aqi <= 100:
        return colored("Satisfactory", "cyan")
    elif aqi <= 200:
        return colored("Moderate", "yellow")
    elif aqi <= 300:
        return colored("Poor", "magenta")
    elif aqi <= 400:
        return colored("Very Poor", "red")
    else:
        return colored("Severe", "red", attrs=['bold'])

# 🖨️ Print results with color
print(f"\n📍 AQI Prediction for {city_input.title()} - Next {num_days} Days:\n")
for i, aqi in enumerate(future_predictions):
    category = get_aqi_category(aqi)
    print(f"Day {i+1}: AQI = {round(aqi, 2)} ==> {category}")

# 📊 Plot
plt.figure(figsize=(10, 5))
plt.plot(range(1, num_days + 1), future_predictions, marker='o', color='green', linestyle='--')
plt.title(f"Predicted AQI for Next {num_days} Days - {city_input.title()}")
plt.xlabel("Days Ahead")
plt.ylabel("Predicted AQI")
plt.grid(True)
plt.show()
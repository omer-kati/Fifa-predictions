from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error,mean_absolute_percentage_error


x_data = pd.read_csv("newSourceMarketValue.csv").drop(columns=["short_name", "player_positions"])
y_data = pd.read_csv("newTargetMarketValue.csv")
y_data = y_data.to_numpy()

x_train, x_test, y_train, y_test = train_test_split( x_data, y_data, test_size=0.1, random_state=42)
feature_names = x_data.columns.values
linreg = LinearRegression()

linreg.fit(x_train, y_train)
predictions = linreg.predict(x_test)
print("mse",mean_squared_error(y_test,predictions))
print("mae",mean_absolute_error(y_test,predictions))
print("RMSE", mean_squared_error(y_test, predictions, squared=False))
print("MAPE", mean_absolute_percentage_error(y_test, predictions))
print("R2", r2_score(y_test, predictions))


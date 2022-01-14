from sklearn.ensemble import  RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error,mean_absolute_percentage_error


x_data = pd.read_csv("source.csv")
y_data = pd.read_csv("target.csv").drop(columns=["sofifa_id"])
y_data = y_data.to_numpy()

x_train, x_test, y_train, y_test = train_test_split( x_data, y_data, test_size=0.1, random_state=42)
feature_names = x_data.columns.values
forest = RandomForestRegressor(max_depth=10, random_state=42, n_estimators=50)

forest.fit(x_train, y_train)
predictions = forest.predict(x_test)
print("mse",mean_squared_error(y_test,predictions))
print("mae",mean_absolute_error(y_test,predictions))
print("RMSE", mean_squared_error(y_test, predictions, squared=False))
print("MAPE", mean_absolute_percentage_error(y_test, predictions))
print("R2", r2_score(y_test, predictions))


# Get numerical feature importances
importances = list(forest.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_names, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
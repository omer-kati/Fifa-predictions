import sklearn.ensemble
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
import pandas as pd
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

x_data = pd.read_csv("source.csv")
y_data = pd.read_csv("target.csv").drop(columns=["sofifa_id"])
x_data["rating"] = y_data["overall"]


correlations = x_data.corr()["rating"]
print(correlations.sort_values())
correlations = x_data.corr()
plt.figure(figsize = (18,18))
sns.heatmap(correlations.sort_values(by="rating"))
plt.show()

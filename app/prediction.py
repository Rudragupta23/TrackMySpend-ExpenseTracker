import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("/content/finalDataFile.csv")

# Check the first few rows to verify the data
df.head()

# Separate features and target
X = df.drop(columns=['target'])
Y = df['target']

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=2)

# Print shapes of data
print(X.shape, X_train.shape, X_test.shape)

# Initialize and train the linear regression model
lin_reg_model = LinearRegression()
lin_reg_model.fit(X_train, Y_train)

# Predict on the training data
training_data_prediction = lin_reg_model.predict(X_train)

# Calculate Mean Absolute Error (MAE) for training data
mae_train = mean_absolute_error(Y_train, training_data_prediction)
print("Training Mean Absolute Error:", mae_train)

# Predict on the testing data
testing_data_prediction = lin_reg_model.predict(X_test)

# Calculate Mean Absolute Error (MAE) for testing data
mae_test = mean_absolute_error(Y_test, testing_data_prediction)
print("Testing Mean Absolute Error:", mae_test)

# Testing a single input
input_data = np.array([[2006.4, 1027.2, 348, 86, 804, 251, 1232.8]])

# Reshape input_data if necessary to ensure it's 2D
input_data = input_data.reshape(1, -1)

# Make a prediction for the single input
prediction = lin_reg_model.predict(input_data)

# Print the prediction
print("Prediction for input data:", prediction)

# If you want to subtract 87 from the prediction (as per your code)
prediction_adjusted = prediction - 87
print("Adjusted prediction (after subtracting 87):", prediction_adjusted)
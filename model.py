import tensorflow as tf
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization, SimpleRNN
from tensorflow.keras.metrics import MeanAbsoluteError, MeanAbsolutePercentageError, MeanSquaredError, \
    RootMeanSquaredError
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score

scaler = MinMaxScaler()
x_data = pd.read_csv("source.csv")
y_data = pd.read_csv("target.csv").drop(columns=["sofifa_id"])
x_data = scaler.fit_transform(x_data)
y_data = y_data.to_numpy()

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.1, random_state=42)

model = Sequential()
model.add(Dense(106, activation='relu', input_shape=(53,)))
model.add(Dropout(0.2))
model.add(Dense(212, activation='relu'))



model.add(Dense(1))

opt = tf.keras.optimizers.Adam()

es = EarlyStopping(monitor='val_loss', patience=10)

# Compile model
model.compile(
    loss='mean_squared_error',
    optimizer=opt,
    metrics=[MeanAbsoluteError(), MeanAbsolutePercentageError(), MeanSquaredError(), RootMeanSquaredError()]
)
checkpoint_filepath = './tmp'

# model.fit(x_train,
#           y_train,
#           epochs=100,
#           validation_split=0.1,
#           validation_data=(x_test,y_test)
#           # callbacks=[tensorboard_callback]
#           )

# Fit the model
history = model.fit(x_train,
                    y_train,
                    epochs=100,
                    validation_split=0.1,
                    callbacks=[es]
                    )
# list all data in history
print(history.history.keys())

# summarize history for loss
plt.plot(history.history['mean_squared_error'])
plt.plot(history.history['mean_absolute_error'])
plt.plot(history.history['mean_absolute_percentage_error'])
plt.plot(history.history['root_mean_squared_error'])
plt.title('Tuned model metrics')
plt.ylabel('metrics')
plt.xlabel('epoch')
plt.legend(['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'root_mean_squared_error'],
           loc='upper right')
plt.axis([0, 35, 0, 20])
plt.show()
# model.save("my_tuned_model_layers")


res = model.evaluate(x_test, y_test, verbose=0)
test_predictions = model.predict(x_test).flatten()

print("NN")
print('Results:')
print('Test R^2 score:', r2_score(y_test, test_predictions))
print('Test mean_squared_error:', res[0])
print('Test mean_absolute_error:', res[1])
print('Test mean_absolute_percentage_error:', res[2])
print('Test root_mean_squared_error:', res[4])

print(res)
# score = model.predict(x_test)
# results = model.evaluate(x_test,y_test)
# print(results)
# print(y_test)
# print(score)

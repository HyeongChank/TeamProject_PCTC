'''Dev: 고건'''

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb



'''데이터 로드 및 분할'''
data = pd.read_csv("./src/fulldataset_rev02.csv")
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



'''모델 생성 및 훈련'''
model = xgb.XGBClassifier(objective='binary:logistic')
model.fit(X_train, y_train)



'''모델 평가'''
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:")
print(report)


'''예측'''
new_data = pd.read_csv("./src/sample_new_data.csv")
y_pred = model.predict(new_data)

print(y_pred)
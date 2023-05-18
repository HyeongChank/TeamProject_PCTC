import pandas as pd
from sklearn.linear_model import LinearRegression

def load_data():
    df = pd.ExcelFile("D:/김형찬/ai-algorism/data/C975F100.xlsx")
    train_df = df.parse('fulldataset')
    train_df = train_df.dropna()
    print(train_df.shape)
    return train_df

def make_xy(train_df):
    total = train_df['total']
    congestion = train_df['congestion']
    X = total.values.reshape(-1, 1)
    y = congestion.values.reshape(-1,1)
    return X,y

def make_model(X,y):
    model = LinearRegression()
    model.fit(X, y)
    print(model.coef_)
    print(model.intercept_)
    return model

def expect_new_congestion(model, newdata):
    X_new = [[newdata]]
    y_pred = model.predict(X_new)
    print(y_pred[0][0])

if __name__ == '__main__':
    train_df = load_data()
    X,y = make_xy(train_df)
    model = make_model(X,y)
    expect_new_congestion(model, 1000)

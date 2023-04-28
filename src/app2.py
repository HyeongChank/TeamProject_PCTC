'''Dev: 김형찬'''

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
import optuna
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from plotly.subplots import make_subplots

df = pd.read_csv("./src/congestion_data.csv", encoding='euc-kr')
df = df[['landngComptQy', 'shipngComptQy','congestion']]
data = df.dropna()
X = data[['landngComptQy', 'shipngComptQy']]
print(X)
y = data['congestion']
print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, shuffle=True, test_size=0.3)
X_trainval, X_valid, y_trainval, y_valid = train_test_split(X_train, y_train, shuffle=True,  random_state=42)

def objective(trial):
    param = {
        # "tree_method":"gpu_hist",
        # "sampling_method": "gradient_based",
        "random_state": 42,
        "lambda": trial.suggest_float("lambda", 7.0, 17.0),
        "alpha": trial.suggest_float("alpha", 7.0, 17.0),
        "eta": trial.suggest_categorical("eta", [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
        "gamma": trial.suggest_categorical("gamma", [18, 19, 20, 21, 22, 23, 24, 25]),
        "learning_rate": trial.suggest_categorical("learning_rate", [0.008,0.01,0.012,0.014,0.016,0.018, 0.02]),
        "colsample_bytree": trial.suggest_categorical("colsample_bytree", [0.3,0.4,0.5,0.6,0.7,0.8,0.9, 1.0]),
        "colsample_bynode": trial.suggest_categorical("colsample_bynode", [0.3,0.4,0.5,0.6,0.7,0.8,0.9, 1.0]),
        "n_estimators": trial.suggest_int("n_estimators", 400, 1000),
        "min_child_weight": trial.suggest_int("min_child_weight", 8, 600),  
        "max_depth": trial.suggest_categorical("max_depth", [3, 4, 5, 6, 7]),  
        "subsample": trial.suggest_categorical("subsample", [0.5,0.6,0.7,0.8,1.0]),
        "early_stopping_rounds": 10,
    }
    model = XGBRegressor(**param)
    model.fit(X_trainval, y_trainval, eval_set=[(X_valid, y_valid)], verbose=False)
    predict = model.predict(X_valid)    
    r_2 = r2_score(predict, y_valid)    
    return r_2

if __name__=='__main__':
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=10,  timeout=600)
    print(f"Number of finished trials: {len(study.trials)}")
    print("Best trial:")
    trial = study.best_trial
    print(f"\t\tValue: {trial.value}")
    print(f"\t\tParams: ")
    for key, value in trial.params.items():
        print(f"\t\t\t\t{key}: {value}")
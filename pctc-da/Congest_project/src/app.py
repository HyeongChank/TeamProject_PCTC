from flask import Flask, render_template, jsonify, request

from DA import process_model
# from DA import randomForest_predict
# from DA import cnn_predict
# from DA import lstm_retrain
# from DA import cnn_truck_count_predict
from DA import process_count_model
from DA import lstm_now
from DA import process_time_result
import json
import requests
from flask_cors import CORS
import pandas as pd
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    
# @app.route('/api/r_predict', methods=['GET', 'POST'])
# def r_prediction():
#     if request.method == 'POST':
#         # new_data = request.get_json()
#         # print('json 전달 받은 데이터', new_data)
#         # new_data_df = pd.DataFrame(new_data)
        
#         grouped_df = randomForest_predict.operate()
#         grouped_df_json = grouped_df.to_json(date_format='iso', orient='records')
#         grouped_df_parsed = json.loads(grouped_df_json)
#         grouped_df_clean = json.dumps(grouped_df_parsed, ensure_ascii=False)
#         return jsonify({'grouped_df_json': grouped_df_clean})
#     else:
#         return 'error'

@app.route('/api/cnn_time_predict', methods=['GET', 'POST'])
def cnn_prediction():
    if request.method == 'POST':
        print('******************request in*********************')
        time_group, predict_group, actual_group = process_time_result.operate()
        
        return jsonify({'time': time_group, 'predict_group': predict_group, 'actual_group': actual_group})
    else:
        return 'error'

@app.route('/api/cnn_count_predict', methods=['GET', 'POST'])
def cnn_count_prediction():
    if request.method == 'POST':
        print('******************request in*********************')
        time_group, predict_group, actual_group = process_count_model.operate()
        
        return jsonify({'time': time_group, 'predict_group': predict_group, 'actual_group': actual_group})
    else:
        return 'error'

# @app.route('/api/lstm_predict', methods=['GET', 'POST'])
# def lstm_prediction():
#     if request.method == 'POST':
#         new_data = request.get_json()
#         print(new_data)
#         prediction_list = lstm_retrain.operate(new_data)
#         # Convert float32 to native Python float
#         prediction_list = [float(i) for i in prediction_list]

#         return jsonify({'predict_group': prediction_list})
#     else:
#         return 'error'
        

if __name__ == '__main__':
    # host, port를 설정하고 여기로 요청을 하게 하면 됨
    app.run(host='10.125.121.220', port=5001, debug=True)
from flask import Flask, render_template, jsonify, request
from DA import randomForest
from DA import quarter
from DA import test2
from DA import congestAnal
from DA import main
from DA import retraining
import requests
from flask_cors import CORS
import pandas as pd
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    
@app.route('/api/congest2', methods=['GET', 'POST'])
def congestion():
    if request.method == 'POST':
        new_data = request.get_json()
        print('json 전달 받은 데이터', new_data)
        new_data_df = pd.DataFrame(new_data)
        # new_data_df = pd.concat([])
        waitingTime, congest_level = main.commit_model(new_data_df)
        
        return jsonify({'congest_level': congest_level.tolist()}, {'waiting_time': waitingTime.tolist()})
    else:
        return 'error'    

# @app.route('./api/updatedata', methods =['GET'])
# def update_data():
#     response = requests.get()
#     retraining.add_data(response)
    
#     return jsonify(response.json())


if __name__ == '__main__':
    # host, port를 설정하고 여기로 요청을 하게 하면 됨
    app.run(host='10.125.121.220', port=5001, debug=True)
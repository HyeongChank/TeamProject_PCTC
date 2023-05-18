import os


def add_data(data, new_data):
    
    # new_data = pd.DataFrame(new_data)
    new_data = new_data[['작업 지시 시간', '작업 완료 시간', '작업코드']]
    # new_data['작업코드'] = new_data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})        
    print('new_data', new_data)
    data = data[['작업 지시 시간', '작업 완료 시간', '작업코드']]
    # Combine existing data and new data
    print('기존', data)
    combined_data = pd.concat([data, new_data], ignore_index=True)
    combined_data['작업코드'] = combined_data['작업코드'].replace({'양하': 1, '적하': -1, '반입': 1, '반출': -1})
    combined_data['누적 컨테이너'] = combined_data['작업코드'].cumsum()
###### 기존 데이터를 포함한 데이터프레임을 CSV 파일로 저장
    existing_csv_path = "./data/congestcsv.csv"
    new_data.to_csv(existing_csv_path, index=False, mode='a', header=not os.path.exists(existing_csv_path))
    print(f"데이터를 '{existing_csv_path}' 파일에 업데이트하여 저장했습니다.")

    print('combined_data', combined_data)
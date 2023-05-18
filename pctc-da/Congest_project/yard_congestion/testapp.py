import unittest
import json
from app import app

class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_congestion_api(self):
        # API 요청에 필요한 데이터 생성
        data = {
            'new_value': 123,
            'new_termCode': 'BNCT'
        }

        # API 호출
        response = self.app.post('/api/congestion', data=json.dumps(data), content_type='application/json')

        # 응답 결과 확인
        self.assertEqual(response.status_code, 200)  # HTTP 상태 코드가 200인지 확인
        self.assertEqual(response.content_type, 'application/json')  # MIME 타입이 JSON인지 확인
        response_data = json.loads(response.get_data())
        self.assertEqual(response_data['new_value'], 123)
        self.assertEqual(response_data['new_termCode'], 'BNCT')

if __name__ == '__main__':
    unittest.main()
from django.urls import reverse
from rest_framework.test import APITestCase


class MovieTest(APITestCase):
    '''
    Movie API를 올바르게 가져오는지 검증하는 테스트 클래스입니다.
    '''
    def test_get_movieapi(self):
        """
        Movie API의 GET 요청을 테스트합니다.

        Movie GET API:
        1. `main` 경로에 대한 GET 요청을 보냅니다.
        2. 요청에는 "api_key"와 "language"라는 파라미터를 포함시킵니다.
        3. status_code가 200인지 확인합니다.
        4. response.data가 10개인지 확인합니다. (view에서 random 10개를 가져오고 있습니다.)
        """
        response = self.client.get(
            path=reverse("main"),
            params = {
                    "api_key": "dfffda402827c71395fe46139633c254",
                    "language": "ko-KR"
                 }
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 380)

from unittest.mock import patch
import sample_responses as sr
from ..settings.constants import RANKING_PATH, SCORE_BOARD_PATH


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if SCORE_BOARD_PATH in args[0]:
        return MockResponse(sr.score_board, 200)
    elif RANKING_PATH in args[0]:
        return MockResponse(sr.ranking, 200)

    return MockResponse(None, 404)


class TestFetch:
    def test_wrong_api_key(self, client):
        response = client.post(f"/fetch", headers={'Authorization': f"Bearer wrong_key"})
        assert response.status_code == 401

    @patch('app.utils.functions.save_backup')
    @patch('app.utils.functions.save_events')
    @patch('app.utils.functions.save_ranking')
    @patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch_ok(self, mock_get, mock_backup, mock_events, mock_ranking, client):

        expected_response = {
            "success": True
        }

        body = {
            "start_date": "2022-01-01",
            "end_date": "2022-01-02"
        }

        response = client.post(f"/fetch/", json=body)
        assert response.status_code == 200
        assert response.json() == expected_response

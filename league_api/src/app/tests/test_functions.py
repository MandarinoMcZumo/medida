from unittest.mock import patch
from datetime import datetime, timedelta
import pytest
import app.utils.functions as f


class TestFetchUtils:
    def test_scoreboard_url(self):
        start_date = '2022-01-01'
        end_date = '2022-01-02'
        scoreboard_url = f'https://delivery.chalk247.com/scoreboard/NFL/{start_date}/{end_date}.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0'
        assert f.score_board_url(start_date, end_date, 'NFL') == scoreboard_url

    def test_ranking_url(self):
        ranking_url = f'https://delivery.chalk247.com/team_rankings/NFL.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0'
        assert f.ranking_url('NFL') == ranking_url

    def test_dates_check_ok(self):
        start_date = '2022-01-01'
        end_date = '2022-01-08'
        expected_start_date, expected_end_date = f.dates_check(start_date)

        assert expected_start_date == start_date
        assert expected_end_date == end_date

    def test_dates_check_ko(self):
        invalid_date = datetime.now() + timedelta(days=1)

        with pytest.raises(Exception) as e_info:
            f.dates_check(str(invalid_date.date()))


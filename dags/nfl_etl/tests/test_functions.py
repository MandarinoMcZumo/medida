import utils.functions as f
import pandas as pd

ranking_doc = {
    '1': {
        'team_id': '54',
        'rank': 1,
        'adjusted_points': 0.1234
    },

    '2': {
        'team_id': '39',
        'rank': 2,
        'adjusted_points': -4.3210
    }
}

events_doc = [
    {
        "event_id": "1654926", "event_date": "2022-10-16 13:00", "home_team_id": "39",
        "home_nick_name": "Packers", "home_city": "Green Bay", "away_team_id": "54",
        "away_nick_name": "Jets", "away_city": "New York"}
]

dashboard_dict = {'event_id': '1654926',
                  'event_date': '2022-10-16',
                  'home_team_id': '39',
                  'home_nick_name': 'Packers',
                  'home_city': 'Green Bay',
                  'away_team_id': '54',
                  'away_nick_name': 'Jets',
                  'away_city': 'New York',
                  'event_time': '13:00',
                  'home_rank': 2,
                  'home_rank_points': -4.32,
                  'away_rank': 1,
                  'away_rank_points': 0.12}
dashboard_series = pd.Series(dashboard_dict)


class TestFunctionsModule:
    def test_build_ranking(self):
        test_df = pd.DataFrame(ranking_doc).T
        expected_df = f.build_ranking_df(ranking_doc)
        assert expected_df.shape == test_df.shape

    def test_build_events_df(self):
        test_df = pd.DataFrame(events_doc)
        expected_df = f.build_events_df(events_doc)
        assert test_df.shape == expected_df.shape

    def test_build_dashboard(self):
        ranking = pd.DataFrame(ranking_doc).T
        events = pd.DataFrame(events_doc)
        expected_df = f.build_dashboard(events, ranking)
        assert expected_df.shape == (1, 13)
        assert expected_df['event_time'].to_list()[0] == '13:00'
        assert expected_df['event_date'].to_list()[0] == '2022-10-16'
        assert expected_df['home_rank_points'].to_list()[0] == -4.32
        assert expected_df['away_rank_points'].to_list()[0] == 0.12

    def test_build_query(self):
        expected_query = f.build_query(dashboard_series)
        test_query = """
        INSERT INTO events_nfl (event_id, event_date, event_time, away_team_id, away_nick_name, away_city, 
                            away_rank, away_rank_points, home_team_id, home_nick_name, home_city, home_rank, home_rank_points)
                            VALUES (
                            '1654926', '2022-10-16', '13:00', 
                            '54', 'Jets', 'New York', 
                            1, 0.12, '39', 
                            'Packers', 'Green Bay', 2, -4.32)
        ON CONFLICT ON CONSTRAINT events_nfl_pkey
            DO
        UPDATE SET event_date = '2022-10-16',
                   event_time = '13:00',
                   away_team_id = '54',
                   away_nick_name = 'Jets',
                   away_city = 'New York',
                   away_rank = 1,
                   away_rank_points = 0.12,
                   home_team_id = '39',
                   home_nick_name = 'Packers',
                   home_city = 'Green Bay',
                   home_rank = 2,
                   home_rank_points = -4.32;"""
        assert test_query == expected_query

"""
Tests for src/wd_bots/utils/lag_bot.py
"""

import pytest


class TestFindLag:
    """Tests for find_lag function"""

    def test_updates_ffa_lag_when_different(self, mocker):
        """Test that FFa_lag is updated when lag value is different"""
        from src.wd_bots.utils.lag_bot import find_lag, FFa_lag

        mocker.patch("src.wd_bots.utils.lag_bot.logger")
        mock_sleep = mocker.patch("src.wd_bots.utils.lag_bot.time.sleep")

        initial_lag = FFa_lag[1]
        err = {"lag": "10"}

        find_lag(err)

        assert FFa_lag[1] == 10
        mock_sleep.assert_called_once_with(11)  # lag + 1

    def test_logs_when_lag_unchanged(self, mocker):
        """Test logging when lag value stays the same"""
        from src.wd_bots.utils.lag_bot import find_lag, FFa_lag

        mock_logger = mocker.patch("src.wd_bots.utils.lag_bot.logger")
        mocker.patch("src.wd_bots.utils.lag_bot.time.sleep")

        # Set to known value
        FFa_lag[1] = 5
        err = {"lag": "5"}

        find_lag(err)

        # Verify it logged the comparison
        assert any("FFa_lag[1]" in str(call) for call in mock_logger.debug.call_args_list)

    def test_sleeps_for_lag_plus_one(self, mocker):
        """Test that sleep duration is lag + 1"""
        from src.wd_bots.utils.lag_bot import find_lag

        mocker.patch("src.wd_bots.utils.lag_bot.logger")
        mock_sleep = mocker.patch("src.wd_bots.utils.lag_bot.time.sleep")

        err = {"lag": "7"}
        find_lag(err)

        mock_sleep.assert_called_once_with(8)  # 7 + 1


class TestMakeSleepDef:
    """Tests for make_sleep_def function"""

    def test_creates_session_on_first_call(self, mocker):
        """Test that session is created on first call"""
        from src.wd_bots.utils.lag_bot import make_sleep_def, session

        mocker.patch("src.wd_bots.utils.lag_bot.logger")
        mock_requests_session = mocker.patch("src.wd_bots.utils.lag_bot.requests.session")
        mock_session_instance = mocker.MagicMock()
        mock_requests_session.return_value = mock_session_instance

        # Reset session
        session[1] = None

        make_sleep_def()

        mock_requests_session.assert_called_once()
        assert session[1] == mock_session_instance

    def test_parses_lag_from_response(self, mocker):
        """Test that lag is extracted from API response"""
        from src.wd_bots.utils.lag_bot import make_sleep_def, FFa_lag, session

        mocker.patch("src.wd_bots.utils.lag_bot.logger")

        # Create mock session
        mock_response = mocker.MagicMock()
        mock_response.text = "Waiting for db1234: 8.5 seconds lagged"

        mock_session_instance = mocker.MagicMock()
        mock_session_instance.post.return_value = mock_response
        session[1] = mock_session_instance

        make_sleep_def()

        assert FFa_lag[1] == 8  # Should be int(float(8.5))

    def test_handles_no_lag_in_response(self, mocker):
        """Test handling when no lag info in response"""
        from src.wd_bots.utils.lag_bot import make_sleep_def, session

        mocker.patch("src.wd_bots.utils.lag_bot.logger")

        mock_response = mocker.MagicMock()
        mock_response.text = "No lag information"

        mock_session_instance = mocker.MagicMock()
        mock_session_instance.post.return_value = mock_response
        session[1] = mock_session_instance

        # Should not raise an exception
        make_sleep_def()

    def test_updates_newsleep_based_on_lag(self, mocker):
        """Test that newsleep is updated based on lag thresholds"""
        from src.wd_bots.utils.lag_bot import make_sleep_def, FFa_lag, newsleep, session

        mocker.patch("src.wd_bots.utils.lag_bot.logger")

        mock_response = mocker.MagicMock()
        mock_response.text = "Waiting for db1234: 7.0 seconds lagged"

        mock_session_instance = mocker.MagicMock()
        mock_session_instance.post.return_value = mock_response
        session[1] = mock_session_instance

        # Reset
        FFa_lag[2] = 0
        newsleep[1] = 0

        make_sleep_def()

        # For lag 7-8, newsleep should be 3
        assert newsleep[1] == 3

    def test_handles_exception_during_request(self, mocker):
        """Test handling of exception during API request"""
        from src.wd_bots.utils.lag_bot import make_sleep_def, session

        mock_logger = mocker.patch("src.wd_bots.utils.lag_bot.logger")

        mock_session_instance = mocker.MagicMock()
        mock_session_instance.post.side_effect = Exception("Network error")
        session[1] = mock_session_instance

        # Should not raise an exception
        make_sleep_def()

        # Should log the warning
        assert mock_logger.warning.called


class TestDoLag:
    """Tests for do_lag function"""

    def test_does_not_loop_when_lag_below_threshold(self, mocker):
        """Test that loop doesn't execute when lag is low"""
        from src.wd_bots.utils.lag_bot import do_lag, FFa_lag

        mocker.patch("src.wd_bots.utils.lag_bot.make_sleep_def")
        mock_sleep = mocker.patch("src.wd_bots.utils.lag_bot.time.sleep")

        FFa_lag[1] = 3  # Below threshold of 5

        do_lag()

        # Should not sleep since lag is below 5
        mock_sleep.assert_not_called()

    def test_loops_when_lag_above_threshold(self, mocker):
        """Test that loop executes when lag is high"""
        from src.wd_bots.utils.lag_bot import do_lag, FFa_lag

        mock_make_sleep = mocker.patch("src.wd_bots.utils.lag_bot.make_sleep_def")
        mock_sleep = mocker.patch("src.wd_bots.utils.lag_bot.time.sleep")
        mocker.patch("src.wd_bots.utils.lag_bot.logger")

        # Simulate lag starting high then going low
        call_count = [0]

        def side_effect():
            call_count[0] += 1
            if call_count[0] > 1:
                FFa_lag[1] = 2  # Drop below threshold after first iteration

        mock_make_sleep.side_effect = side_effect
        FFa_lag[1] = 10  # Start above threshold

        do_lag()

        assert mock_sleep.called

    def test_calculates_sleep_time_correctly(self, mocker):
        """Test that sleep time is calculated as lag * 2"""
        from src.wd_bots.utils.lag_bot import do_lag, FFa_lag

        mocker.patch("src.wd_bots.utils.lag_bot.logger")
        mock_make_sleep = mocker.patch("src.wd_bots.utils.lag_bot.make_sleep_def")
        mock_sleep = mocker.patch("src.wd_bots.utils.lag_bot.time.sleep")

        # Simulate one iteration
        call_count = [0]

        def side_effect():
            call_count[0] += 1
            if call_count[0] > 1:
                FFa_lag[1] = 2

        mock_make_sleep.side_effect = side_effect
        FFa_lag[1] = 8

        do_lag()

        # First sleep should be 8 * 2 = 16
        assert any(call[0][0] == 16 for call in mock_sleep.call_args_list)


class TestBadLag:
    """Tests for bad_lag function"""

    def test_returns_false_for_testwikidata(self, mocker):
        """Test that bad_lag returns False when testwikidata in sys.argv"""
        from src.wd_bots.utils.lag_bot import bad_lag

        mocker.patch("src.wd_bots.utils.lag_bot.sys.argv", ["script.py", "testwikidata"])

        result = bad_lag(True)
        assert result is False

    def test_returns_true_when_nowait_and_high_lag(self, mocker):
        """Test returns True when nowait=True and lag > 5"""
        from src.wd_bots.utils.lag_bot import bad_lag, FFa_lag

        mocker.patch("src.wd_bots.utils.lag_bot.sys.argv", [])

        FFa_lag[1] = 10

        result = bad_lag(nowait=True)
        assert result is True

    def test_returns_false_when_nowait_false(self, mocker):
        """Test returns False when nowait=False regardless of lag"""
        from src.wd_bots.utils.lag_bot import bad_lag, FFa_lag

        mocker.patch("src.wd_bots.utils.lag_bot.sys.argv", [])

        FFa_lag[1] = 10

        result = bad_lag(nowait=False)
        assert result is False

    def test_returns_false_when_lag_below_threshold(self, mocker):
        """Test returns False when lag <= 5 even with nowait=True"""
        from src.wd_bots.utils.lag_bot import bad_lag, FFa_lag

        mocker.patch("src.wd_bots.utils.lag_bot.sys.argv", [])

        FFa_lag[1] = 3

        result = bad_lag(nowait=True)
        assert result is False

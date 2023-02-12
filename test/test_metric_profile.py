"""Unit test for the metric profile class."""
from unittest.mock import patch, mock_open, call, Mock, ANY

from src.profile.metric_profile import MetricProfile
from src.profile.metric_region import MetricRegion
from src.profile.show import show_profile
from src.profile.sqatt_profiles import create_function_size_profile


def test_profile_can_have_one_region():
    """Test that a profile can have only one region."""

    # arrange
    regions = [MetricRegion("0-15", 0, 15)]

    # act
    profile = MetricProfile("Function size", regions)

    # assert
    assert len(profile.regions()) == 1


def test_profile_regions_updated_correctly():
    """Test that a profile is updated correctly."""

    # arrange
    regions = [
        MetricRegion("0-15", 0, 15),
        MetricRegion("16-30", 16, 30),
        MetricRegion("31-60", 31, 60),
        MetricRegion("60+", 61, 1001),
    ]

    profile = MetricProfile("Fan-in", regions)

    # act
    profile.update(1, 100)
    profile.update(15, 100)
    profile.update(16, 100)
    profile.update(30, 100)
    profile.update(31, 100)
    profile.update(60, 100)
    profile.update(61, 100)
    profile.update(1000, 100)
    profile.update(1001, 100)

    # assert
    assert profile.regions()[0].loc() == 200
    assert profile.regions()[1].loc() == 200
    assert profile.regions()[2].loc() == 200
    assert profile.regions()[3].loc() == 300
    assert profile.total_loc() == 900


def test_profile_can_have_four_regions():
    """Test that a profile can have 4 regions."""

    # arrange
    regions = [
        MetricRegion("0-15", 0, 16),
        MetricRegion("16-30", 15, 31),
        MetricRegion("31-60", 30, 61),
        MetricRegion("60+", 60, 1001),
    ]

    # act
    profile = MetricProfile("Function size", regions)

    # assert
    assert len(profile.regions()) == 4


def test_profile_printed_correctly(capsys):
    """Test that the profile is printed to console correctly."""

    # arrange
    regions = [
        MetricRegion("0-15", 0, 15),
        MetricRegion("16-30", 16, 30),
        MetricRegion("31-60", 31, 60),
        MetricRegion("60+", 61),
    ]

    profile = MetricProfile("Function size", regions)

    profile.update_loc(1)
    profile.update_loc(15)
    profile.update_loc(16)
    profile.update_loc(17)
    profile.update_loc(60)
    profile.update_loc(61)
    profile.update_loc(1000)
    profile.update_loc(1001)

    # act
    profile.print()

    # assert
    captured = capsys.readouterr()
    assert captured.out == "Function size : loc\n0-15 : 16\n16-30 : 33\n31-60 : 60\n60+ : 2062\n"


@patch("src.profile.MetricProfile.csv")
def test_profile_saved_correctly(csv_mock):
    """Test that the profile is saved to console correctly."""

    # arrange
    regions = [
        MetricRegion("0-15", 0, 15),
        MetricRegion("16-30", 16, 30),
        MetricRegion("31-60", 31, 60),
        MetricRegion("60+", 61),
    ]

    profile = MetricProfile("Function size", regions)

    profile.update_loc(2)
    profile.update_loc(15)
    profile.update_loc(16)
    profile.update_loc(17)
    profile.update_loc(60)
    profile.update_loc(61)
    profile.update_loc(1001)
    profile.update_loc(1001)

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Function size", "Lines Of Code"]),
        call.writerow(["0-15", 17]),
        call.writerow(["16-30", 33]),
        call.writerow(["31-60", 60]),
        call.writerow(["60+", 2063]),
    ]

    report_file = "report.csv"

    # act
    with patch("src.profile.MetricProfile.open", mock_open()) as mocked_file:
        profile.save(report_file)

    # assert
    mocked_file.assert_called_once_with(report_file, "w", encoding="utf-8")
    csv_mock.writer().assert_has_calls(calls)


@patch("src.profile.show.go.Figure")
def test_profile_is_shown_correctly(figure_mock):
    """Test that the profile is show correctly in a figure."""

    # arrange
    profile = create_function_size_profile()

    profile.update_loc(20)
    profile.update_loc(100)
    profile.update_loc(10)
    profile.update_loc(40)

    # act
    with patch("src.profile.show.go.Pie") as pie_mock:
        figure_mock.show = Mock()
        show_profile(profile)

    # assert
    pie_mock.assert_called_once_with(
        title={"text": "Function size"},
        labels=["0-15", "16-30", "31-60", "60+"],
        values=[10, 20, 40, 100],
        hole=ANY,
        marker_line=ANY,
        marker_colors=ANY,
    )

    figure_mock().show.assert_called_once()

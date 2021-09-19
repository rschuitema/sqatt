"""Unit test for cloc language analysis."""
from unittest.mock import patch, Mock, call, mock_open, ANY

import src.profile.show
from src.cloc.cloc_languages import save_language_profile, show_language_profile


@patch("src.cloc.cloc_languages.csv")
def test_metrics_are_written_to_file(csv_mock):
    """Test that the metrics are written correctly to file."""

    # arrange
    production_code_metrics = {
        "Python": {"files": 201, "blank": 20, "code": 1003, "comment": 230},
        "C#": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
    }

    csv_mock.writer = Mock(writerow=Mock())
    calls = [
        call.writerow(["Language", "Number Of Files", "Blank Lines", "Lines Of Code", "Comment Lines"]),
        call.writerow(["Python", 201, 20, 1003, 230]),
        call.writerow(["C#", 100, 7, 1220, 30]),
    ]

    # act
    with patch("src.cloc.cloc_languages.open", mock_open()) as mocked_file:
        save_language_profile("language_profile.csv", production_code_metrics)
        mocked_file.assert_called_once_with("language_profile.csv", "w", encoding="utf-8")

    # assert
    csv_mock.writer().writerow.assert_has_calls(calls)
    assert csv_mock.writer().writerow.call_count == 3


@patch("src.cloc.cloc_languages.csv")
def test_metrics_are_not_written_to_file_when_profile_could_not_be_determined(csv_mock):
    """Test that no metrics are written to file."""

    # arrange
    production_code_metrics = {}

    csv_mock.writer = Mock(writerow=Mock())

    # act
    with patch("src.cloc.cloc_languages.open", mock_open()) as mocked_file:
        language_profile_filename = "language_profile.csv"
        save_language_profile(language_profile_filename, production_code_metrics)
        mocked_file.assert_called_once_with(language_profile_filename, "w", encoding="utf-8")

        # assert
        csv_mock.writer().writerow.assert_called_once_with(
            ["Language", "Number Of Files", "Blank Lines", "Lines Of Code", "Comment Lines"]
        )


@patch("src.profile.show.go.Figure")
def test_show_language_profile_figure_created_with_correct_values(figure_mock):
    """Test that the figure is created with the correct values."""

    # arrange
    language_profile = {
        "Python": {"files": 201, "blank": 20, "code": 1003, "comment": 230},
        "C#": {"files": 100, "blank": 7, "code": 1220, "comment": 30},
    }

    # act
    with patch("src.profile.show.go.Pie") as pie_mock:
        figure_mock.data = [pie_mock]
        figure_mock.show = Mock()
        show_language_profile(language_profile)

    # assert
    pie_mock.assert_called_once_with(
        title={"text": "Language profile"},
        labels=["Python", "C#"],
        values=[1003, 1220],
        hole=ANY,
        marker_line=ANY,
        marker_colors=ANY,
    )

    figure_mock().show.assert_called_once()

"""Unit test for the metric profile class."""
from src.profile.MetricProfile import MetricProfile
from src.profile.MetricRegion import MetricRegion


def test_profile_can_have_one_region():
    """Test that a profile can have only one region."""

    # arrange
    regions = [MetricRegion("0-15", 0, 15)]

    # act
    profile = MetricProfile("Function size", regions)

    # assert
    assert len(profile.regions()) == 1


def test_profile_can_have_four_regions():
    """Test that a profile can have 4 regions."""

    # arrange
    regions = [MetricRegion("0-15", 0, 16),
               MetricRegion("16-30", 15, 31),
               MetricRegion("31-60", 30, 61),
               MetricRegion("60+", 60, 1001)]

    # act
    profile = MetricProfile("Function size", regions)

    # assert
    assert len(profile.regions()) == 4


def test_profile_regions_updated_correctly():
    """Test that a profile is updated correctly."""

    # arrange
    regions = [MetricRegion("0-15", 0, 15),
               MetricRegion("16-30", 16, 30),
               MetricRegion("31-60", 31, 60),
               MetricRegion("60+", 61)]

    profile = MetricProfile("Function size", regions)

    # act
    profile.update_loc(1)
    profile.update_loc(15)
    profile.update_loc(16)
    profile.update_loc(17)
    profile.update_loc(60)
    profile.update_loc(61)
    profile.update_loc(1000)
    profile.update_loc(1001)

    # assert
    assert profile.regions()[0].loc() == 16
    assert profile.regions()[1].loc() == 33
    assert profile.regions()[2].loc() == 60
    assert profile.regions()[3].loc() == 2062
    assert profile.total_loc() == 2171


def test_profile_printed_correctly(capsys):
    """Test that the profile is printed to console correctly."""

    # arrange
    regions = [MetricRegion("0-15", 0, 15),
               MetricRegion("16-30", 16, 30),
               MetricRegion("31-60", 31, 60),
               MetricRegion("60+", 61)]

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

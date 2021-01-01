"""Unit tests for the sqatt profiles."""

from src.profile.sqatt_profiles import (
    create_function_size_profile,
    create_complexity_profile,
    create_function_parameters_profile,
    create_fan_in_profile,
    create_fan_out_profile,
)


def test_create_function_size_profile():
    """Test the creation of the function size profile."""

    # arrange

    # act
    profile = create_function_size_profile()

    # assert
    assert profile.name() == "Function size"
    assert profile.regions()[0].loc() == 0
    assert profile.regions()[1].loc() == 0
    assert profile.regions()[2].loc() == 0
    assert profile.regions()[3].loc() == 0


def test_create_complexity_profile():
    """Test the creation of the complexity profile."""

    # arrange

    # act
    profile = create_complexity_profile()

    # assert
    assert profile.name() == "Complexity"
    assert profile.regions()[0].loc() == 0
    assert profile.regions()[1].loc() == 0
    assert profile.regions()[2].loc() == 0
    assert profile.regions()[3].loc() == 0


def test_create_function_parameters_profile():
    """Test the creation of the function parameters profile."""

    # arrange

    # act
    profile = create_function_parameters_profile()

    # assert
    assert profile.name() == "Function parameters"
    assert profile.regions()[0].loc() == 0
    assert profile.regions()[1].loc() == 0
    assert profile.regions()[2].loc() == 0
    assert profile.regions()[3].loc() == 0


def test_create_fan_in_profile():
    """Test the creation of the fan in profile."""

    # arrange

    # act
    profile = create_fan_in_profile()

    # assert
    assert profile.name() == "Fan in"
    assert profile.regions()[0].loc() == 0
    assert profile.regions()[1].loc() == 0
    assert profile.regions()[2].loc() == 0
    assert profile.regions()[3].loc() == 0


def test_create_fan_out_profile():
    """Test the creation of the fan out profile."""

    # arrange

    # act
    profile = create_fan_out_profile()

    # assert
    assert profile.name() == "Fan out"
    assert profile.regions()[0].loc() == 0
    assert profile.regions()[1].loc() == 0
    assert profile.regions()[2].loc() == 0
    assert profile.regions()[3].loc() == 0

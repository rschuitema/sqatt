"""Unit tests for the sqatt profiles."""

from src.profile.sqatt_profiles import (
    create_function_size_profile,
    create_complexity_profile,
    create_function_parameters_profile,
    create_fan_in_profile,
    create_fan_out_profile,
    create_file_size_profile,
)


def test_create_function_size_profile():
    """Test the creation of the function size profile."""

    # act
    profile = create_function_size_profile()

    # assert
    assert profile.name() == "Function size"
    assert that_profile_has_no_lines_of_code(profile)


def test_create_complexity_profile():
    """Test the creation of the complexity profile."""

    # act
    profile = create_complexity_profile()

    # assert
    assert profile.name() == "Complexity"
    assert that_profile_has_no_lines_of_code(profile)


def test_create_function_parameters_profile():
    """Test the creation of the function parameters profile."""

    # act
    profile = create_function_parameters_profile()

    # assert
    assert profile.name() == "Function parameters"
    assert that_profile_has_no_lines_of_code(profile)


def test_create_fan_in_profile():
    """Test the creation of the fan in profile."""

    # act
    profile = create_fan_in_profile()

    # assert
    assert profile.name() == "Fan in"
    assert that_profile_has_no_lines_of_code(profile)


def test_create_fan_out_profile():
    """Test the creation of the fan out profile."""

    # act
    profile = create_fan_out_profile()

    # assert
    assert profile.name() == "Fan out"
    assert that_profile_has_no_lines_of_code(profile)


def test_create_file_size_profile():
    """Test the creation of the file size profile."""

    # act
    profile = create_file_size_profile()

    # assert
    assert profile.name() == "File size"
    assert that_profile_has_no_lines_of_code(profile)


def that_profile_has_no_lines_of_code(profile):
    """Check that a profile has no lines of code."""

    result = profile.regions()[0].loc() == 0
    result = result and profile.regions()[1].loc() == 0
    result = result and profile.regions()[2].loc() == 0
    result = result and profile.regions()[3].loc() == 0

    return result

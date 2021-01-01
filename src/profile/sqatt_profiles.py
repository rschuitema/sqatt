from src.profile.MetricProfile import MetricProfile
from src.profile.MetricRegion import MetricRegion


def create_function_size_profile():
    """Create the function size profile."""

    regions = [
        MetricRegion("0-15", 0, 16),
        MetricRegion("16-30", 15, 31),
        MetricRegion("31-60", 30, 61),
        MetricRegion("60+", 60, 1001),
    ]

    return MetricProfile("Function size", regions)


def create_complexity_profile():
    """Create the complexity profile."""

    regions = [
        MetricRegion("0-5", 0, 5),
        MetricRegion("6-10", 6, 10),
        MetricRegion("11-25", 11, 25),
        MetricRegion("25+", 26, 1001),
    ]

    return MetricProfile("Complexity", regions)


def create_fan_in_profile():
    """Create the fan in profile."""

    regions = [
        MetricRegion("1-10", 1, 10),
        MetricRegion("11-20", 11, 20),
        MetricRegion("21-50", 21, 50),
        MetricRegion("50+", 51, 1001),
    ]

    return MetricProfile("Fan in", regions)


def create_fan_out_profile():
    """Create the fan out profile."""

    regions = [
        MetricRegion("1-10", 1, 10),
        MetricRegion("11-20", 11, 20),
        MetricRegion("21-50", 21, 50),
        MetricRegion("50+", 51, 1001),
    ]

    return MetricProfile("Fan out", regions)


def create_function_parameters_profile():
    """Create the function parameters profile."""

    regions = [
        MetricRegion("1-2", 1, 2),
        MetricRegion("3-4", 3, 4),
        MetricRegion("5-6", 5, 6),
        MetricRegion("6+", 6, 10),
    ]

    return MetricProfile("Function parameters", regions)

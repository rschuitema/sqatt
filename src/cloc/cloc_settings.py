"""Manage the settings for the cloc analysis."""
import yaml


def read_settings(settings_file):
    """Read the settings from a yaml file."""

    with open(settings_file, "r", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    return config


def create_default_settings():
    """Create default settings."""

    default_settings = {
        "analysis_directory": ".",
        "code_type": ["production", "test"],
        "production_filter": "--exclude-dir=test,tst",
        "test_filter": "--match-d=(test|tst)",
        "file_size_filter": "--exclude-dir=test,tst",
        "report_directory": "./reports",
    }
    return default_settings


def get_settings(config_file, report_directory, analysis_directory):
    """Get the settings for the lines of code analysis."""

    try:
        local_settings = read_settings(config_file)
    except (OSError, yaml.YAMLError):
        local_settings = create_default_settings()

    if report_directory:
        local_settings["report_directory"] = report_directory

    if analysis_directory:
        local_settings["analysis_directory"] = analysis_directory

    return local_settings

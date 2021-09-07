"""Report utility functions."""
import os
import shutil


def create_report_directory(directory):
    """Create the report directory."""

    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def setup_report_directory(directory):
    """Create an empty report directory."""

    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.makedirs(directory)

    return directory

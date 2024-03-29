"""Generic class that represents a profile for a metric."""

import csv


class MetricProfile:
    """Metric profile definition."""

    def __init__(self, name, regions):
        """Construct the class."""

        self._name = name
        self._total_loc = 0
        if isinstance(regions, list):
            self._regions = regions or []

    def update_loc(self, loc):
        """Update the loc in the correct region."""

        self._total_loc += loc
        for region in self._regions:
            region.update_loc(loc)

    def regions(self):
        """Return the regions."""

        return self._regions

    def total_loc(self):
        """Return the total lines of code."""

        return self._total_loc

    def name(self):
        """Return the name of the profile."""
        return self._name

    def print(self):
        """Print the profile to console."""

        print(self._name, ": loc")
        for region in self._regions:
            print(region.label(), ":", region.loc())

    def update(self, metric, loc):
        """Update the loc in the correct region."""

        self._total_loc += loc
        for region in self._regions:
            region.update(metric, loc)

    def save(self, report_file):
        """Save the profile to a csv file."""

        with open(report_file, "w", encoding="utf-8") as report:
            csv_writer = csv.writer(report, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_ALL)
            csv_writer.writerow([self._name, "Lines Of Code"])
            for region in self._regions:
                csv_writer.writerow([region.label(), region.loc()])

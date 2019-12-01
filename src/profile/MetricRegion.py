"""Generic definition of a metric region."""


class MetricRegion:
    """Metric region definition."""

    def __init__(self, label, lower_limit, upper_limit=None):
        """Construct the class."""

        self._upper_limit = upper_limit
        self._lower_limit = lower_limit
        self._label = label
        self._loc = 0

    def update_loc(self, loc):
        """Update the loc if between lower and upper limits."""

        if self._upper_limit:
            if self._lower_limit <= loc <= self._upper_limit:
                self._loc += loc
        else:
            if self._lower_limit <= loc:
                self._loc += loc

    def label(self):
        """Return region label."""

        return self._label

    def loc(self):
        """Return loc in region."""

        return self._loc

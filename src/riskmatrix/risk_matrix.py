"""
Represent a matrix that defines quality thresholds for each risk quadrant.

Furthermore it knows to which risk quadrant each component belongs.
"""
import csv


class RiskMatrix:
    """
    Represents a matrix that defines quality thresholds for each risk quadrant.

    It knows the thresholds and to which risk quadrant each component belongs.
    """

    def __init__(self):
        """Construct a risk matrix."""

        self.metric_thresholds = {}
        self.component_risk_level = {}
        self.metric_comparators = {
            "<": RiskMatrix.metric_lt,
            "<=": RiskMatrix.metric_le,
            ">": RiskMatrix.metric_gt,
            ">=": RiskMatrix.metric_ge,
        }

    @staticmethod
    def metric_lt(metric1, metric2):
        """Check if metric1 is less than metric2."""

        return metric1 < metric2

    @staticmethod
    def metric_le(metric1, metric2):
        """Check if metric1 is less than or equal to metric2."""

        return metric1 <= metric2

    @staticmethod
    def metric_gt(metric1, metric2):
        """Check if metric1 is greater than metric2."""

        return metric1 > metric2

    @staticmethod
    def metric_ge(metric1, metric2):
        """Check if metric1 is greater than or equal to metric2."""

        return metric1 >= metric2

    def add_component_risk_level(self, filename, csv_reader=None):
        """Add risk level for each component."""

        with open(filename) as csv_file:
            reader = csv_reader or csv.DictReader(csv_file, skipinitialspace=True)
            for row in reader:
                self.component_risk_level[row["Component"]] = row["Quadrant"]

    def add_metric_thresholds(self, filename, csv_reader=None):
        """Add metric thresholds for each quadrant."""

        with open(filename) as csv_file:
            reader = csv_reader or csv.DictReader(csv_file, skipinitialspace=True)
            for row in reader:
                self.metric_thresholds[row["Quadrant"]] = row

    def verify_metric(self, filename, csv_reader=None):
        """Verify if all the components comply to the specified metric threshold of its quadrant."""

        result = True
        with open(filename) as csv_file:
            reader = csv_reader or csv.reader(csv_file, skipinitialspace=True)
            metric_label = reader.fieldnames[1]
            for row in reader:
                component = row[reader.fieldnames[0]]
                metric_value = row[reader.fieldnames[1]]
                quadrant = self.component_risk_level[component]
                quadrant_thresholds = self.metric_thresholds[quadrant]
                values = quadrant_thresholds[metric_label].split(" ")
                comparison = values[0]
                threshold_value = values[1]

                print(component, quadrant_thresholds[metric_label], metric_value)
                result = result and self.metric_comparators[comparison](
                    metric_value, threshold_value
                )

        return result

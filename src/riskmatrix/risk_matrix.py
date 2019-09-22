import csv


class RiskMatrix:
    def __init__(self):
        self.metric_thresholds = {}
        self.component_risk_level = {}
        self.metric_comparators = {'<': RiskMatrix.metric_lt, '<=': RiskMatrix.metric_le, '>': RiskMatrix.metric_gt,
                                   '>=': RiskMatrix.metric_ge}

    @staticmethod
    def metric_lt(metric1, metric2):
        return metric1 < metric2

    @staticmethod
    def metric_le(metric1, metric2):
        return metric1 < metric2

    @staticmethod
    def metric_gt(metric1, metric2):
        return metric1 > metric2

    @staticmethod
    def metric_ge(metric1, metric2):
        return metric1 >= metric2

    def add_component_risk_level(self, filename):
        with open(filename) as csv_file:
            reader = csv.DictReader(csv_file, skipinitialspace=True)
            for row in reader:
                self.component_risk_level[row['Component']] = row['Quadrant']

    def add_metric_thresholds(self, filename):
        with open(filename) as csv_file:
            reader = csv.DictReader(csv_file, skipinitialspace=True)
            for row in reader:
                self.metric_thresholds[row['Quadrant']] = row

    def verify_metric(self, filename):
        result = True
        with open(filename) as csv_file:
            reader = csv.reader(csv_file, skipinitialspace=True)
            row = next(reader)
            metric_label = row[1]
            for row in reader:
                component = row[0]
                metric_value = row[1]
                quadrant = self.component_risk_level[component]
                quadrant_thresholds = self.metric_thresholds[quadrant]
                metric_threshold = quadrant_thresholds[metric_label]
                values = metric_threshold.split(' ')
                comparison = values[0]
                threshold_value = values[1]

                print(component, metric_threshold, metric_value)
                result = result and self.metric_comparators[comparison](metric_value, threshold_value)

        return result

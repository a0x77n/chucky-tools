import numpy as np

from chucky_tools.base import GroupTool

ARGPARSE_DESCRIPTION = """ROC curve generator. Generate ROC curve data from a two columns input file containing the
label (0 or 1) and the corresponing score. Returns the true-positive and false-positive rates for each threshold."""


class ROCCurve(GroupTool):
    def __init__(self, description=None):
        super(ROCCurve, self).__init__(ARGPARSE_DESCRIPTION)
        self._with_check = None
        self._without_check = None

    def _initializeOptParser(self):
        super(ROCCurve, self)._initializeOptParser()
        self.argParser.add_argument(
            '-n', '--number-of-thresholds',
            type=int,
            default=11,
            help='''the number of equidistant thresholds to be applied'''
        )

    def process_group(self, group_key, group_data):
        label = bool(int(group_key[0]))
        if label:
            self._with_check = [float(score) for _, score in group_data]
        else:
            self._without_check = [float(score) for _, score in group_data]

    def streamEnd(self):
        super(ROCCurve, self).streamEnd()
        if self._with_check and self._without_check:
            for threshold in np.linspace(1, 0, self.args.number_of_thresholds):
                tp, fp = self._classify(threshold)
                self.write_fields([tp / len(self._without_check), fp / len(self._with_check)])

    def _classify(self, threshold):
        fp, tp = 0, 0
        for score in self._with_check:
            if score >= threshold:
                fp += 1
        for score in self._without_check:
            if score >= threshold:
                tp += 1
        return float(tp), float(fp)

import numpy as np

from chucky_tools.base.chucky_fields_tool import FieldsTool

ARGPARSE_DESCRIPTION = """Area under the curve (AUC) calculator. Calculates the area under the curve from
true-positive-false-positive pairs."""


class AUC(FieldsTool):
    def __init__(self, description=None):
        super(AUC, self).__init__(ARGPARSE_DESCRIPTION)
        self._tp = None
        self._fp = None

    def streamStart(self):
        self._tp = []
        self._fp = []

    def process_fields(self, line):
        fp, tp = line
        self._fp.append(float(fp))
        self._tp.append(float(tp))

    def streamEnd(self):
        auc = np.trapz(self._tp, x=self._fp)
        self.write_fields([auc])

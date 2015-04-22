import sys
from argparse import FileType

from sklearn.datasets import dump_svmlight_file

from chucky_tools.base import ChuckyEmbeddingLoader
from chucky_tools.base import ChuckyLogger
from chucky_tools.base import DimensionReductionTool


DESCRIPTION = "Dimension reduction tool."


class EmbeddingReducer(ChuckyEmbeddingLoader, DimensionReductionTool, ChuckyLogger):
    def __init__(self):
        super(EmbeddingReducer, self).__init__(DESCRIPTION)

    def _initializeOptParser(self):
        super(EmbeddingReducer, self)._initializeOptParser()
        self.argParser.add_argument(
            '-o', '--out',
            nargs='?',
            type=FileType('w'),
            default=sys.stdout,
            help='write output to provided file'
        )

    def _runImpl(self):
        super(EmbeddingReducer, self)._runImpl()
        x = self.perform_svd(self.x)
        dump_svmlight_file(x, self.y, self.args.out)


    @classmethod
    def main(cls):
        cls().run()

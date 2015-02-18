from joerntools.mlutils.EmbeddingLoader import EmbeddingLoader

from chucky_tools.base import ChuckyLogger
from chucky_tools.base import FieldsTool


ARGPARSE_DESCRIPTION = """Chucky anomaly ranker."""


class ChuckyScoreTool(FieldsTool, ChuckyLogger):
    def __init__(self):
        super(ChuckyScoreTool, self).__init__(ARGPARSE_DESCRIPTION)
        self._emb = None

    def _initializeOptParser(self):
        super(ChuckyScoreTool, self)._initializeOptParser()
        self.argParser.add_argument(
            'embedding',
            type=str,
            help='the directory containing the embedding'
        )

    def streamStart(self):
        try:
            loader = EmbeddingLoader()
            loader.load(self.args.embedding)
            loader._loadFeatureTable()
            self._emb = loader.emb
        except Exception as e:
            self.logger.error('Failed while loading embedding: %s', e.message)
            exit()

    def process_fields(self, fields):
        node = fields[0]
        if len(fields) < 2:
            self.output('{}\t'.format(str(node)))
            self.output('     n/a\t')
            self.output('n/a')
            self.output('\n')
            return

        neighbors = fields[1:]
        node_index = self._emb.rTOC[node]
        neighbor_index = map(lambda x: self._emb.rTOC[x], neighbors)
        data_point = self._emb.x[node_index]
        mean = self._emb.x[neighbor_index].mean(axis=0).getA()
        deviation = (mean - data_point)
        index = deviation.argmax()
        score = deviation[0, index]
        try:
            feat = self._emb.rFeatTable[index].replace('%20', ' ')
        except KeyError:
            feat = None
        self.output('{}\t'.format(str(node)))
        self.output('{:< 6.5f}\t'.format(score))
        self.output(str(feat))
        self.output('\n')

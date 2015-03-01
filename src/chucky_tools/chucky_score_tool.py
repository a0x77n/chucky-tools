import numpy as np

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
        self.argParser.add_argument(
            '--ignore-missing-datapoints',
            action='store_true',
            default=False,
            help="""Treat missing datapoints as zero vectors"""
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
        neighbors = fields[1:]

        if len(fields) < 2:
            self.write_fields([node, '     n/a', 'n/a'])
            return

        node_index = self._get_index(node)
        neighbor_indices = map(self._get_index, neighbors)
        nonzero_neighbor_indices = [n for n in neighbor_indices if n is not None]
        if len(nonzero_neighbor_indices) > 0:
            mean = (self._emb.x[nonzero_neighbor_indices].sum(axis=0) / len(neighbors))
        else:
            mean = np.zeros((1, self._emb.x.shape[1]))
        if node_index is not None:
            datapoint = self._emb.x[[node_index]]
        else:
            datapoint = np.zeros((1, self._emb.x.shape[1]))
        deviation = mean - datapoint
        index = deviation.argmax()
        score = deviation[0, index]
        feat = self._index_to_feature(index)
        self.write_fields([node, '{:< 6.5f}'.format(score), feat])

    def _get_index(self, node_id):
        try:
            return self._emb.rTOC[node_id]
        except KeyError:
            if self.args.ignore_missing_datapoints:
                return None
            raise

    def _index_to_feature(self, index):
        try:
            return self._emb.rFeatTable[index].replace("%20", " ")
        except KeyError:
            return None


import numpy as np
import gzip

from chucky_tools.base import ChuckyEmbeddingLoader
from chucky_tools.base import FieldsTool


ARGPARSE_DESCRIPTION = """Chucky anomaly ranker."""


class ChuckyScoreTool(FieldsTool, ChuckyEmbeddingLoader):
    def __init__(self):
        super(ChuckyScoreTool, self).__init__(ARGPARSE_DESCRIPTION)
        self._feats = None

    def _initializeOptParser(self):
        super(ChuckyScoreTool, self)._initializeOptParser()
        self.argParser.add_argument(
            '--ignore-missing-datapoints',
            action='store_true',
            default=False,
            help="""Treat missing datapoints as zero vectors"""
        )
        self.argParser.add_argument(
            '--feats',
            type=str,
            default=None,
            help="load feature table"
        )

    def streamStart(self):
        super(ChuckyScoreTool, self).streamStart()
        if self.args.feats:
            self._feats = {}
            with gzip.open(self.args.feats, 'rb') as f:
                f.readline()
                for line in f:
                    line = line.strip()
                    dim, feat = line[4:].split(':', 1)
                    dim = int(dim, 16)
                    feat = feat.replace("%20", " ").strip()
                    self._feats[dim] = feat

    def process_fields(self, fields):
        node = int(fields[0])
        neighbors = map(int, fields[1:])

        if len(fields) < 2:
            self.write_fields([node, 0, '     n/a', 'n/a'])
            return

        nonzero_neighbors = [n for n in neighbors if n in self.toc]
        if len(nonzero_neighbors) > 0:
            mean = self.feature_matrix(nonzero_neighbors).sum(axis=0) / len(neighbors)
            mean = np.squeeze(np.asarray(mean))
        else:
            mean = np.zeros(self.number_of_features)
        if node in self.toc:
            datapoint = self.feature_matrix([node])
            datapoint = np.squeeze(datapoint.toarray())
        else:
            datapoint = np.zeros(self.number_of_features)
        deviation = mean - datapoint
        index = deviation.argmax()
        score = deviation[index]
        if score > 0:
            feat = self.dimension_to_feature(index)
        else:
            feat = 'n/a'

        self.write_fields([node, len(neighbors), '{:< 6.5f}'.format(score), feat])

    def get_index(self, node_id):
        try:
            return super(ChuckyScoreTool, self).get_index(node_id)
        except KeyError:
            if self.args.ignore_missing_datapoints:
                self.logger.info("Datapoint {} not found".format(node_id))
                return None
            raise

    def dimension_to_feature(self, index):
        dim = self.get_dimension(index)
        if self.args.feats:
            return self._feats[dim]
        else:
            return None


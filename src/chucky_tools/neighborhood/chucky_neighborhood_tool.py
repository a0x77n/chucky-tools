import sys
import numpy as np
# from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

from sklearn.metrics.pairwise import pairwise_distances

from chucky_tools.base import ChuckyEmbeddingLoader
from chucky_tools.base import ChuckyJoern
from chucky_tools.base import ChuckyLogger
from chucky_tools.base import DimensionReductionTool
from chucky_tools.base import FieldsTool


class NeighborhoodTool(FieldsTool, DimensionReductionTool, ChuckyEmbeddingLoader, ChuckyLogger, ChuckyJoern):
    def __init__(self, description):
        super(NeighborhoodTool, self).__init__(description)
        self.__map = None

    def _initializeOptParser(self):
        super(NeighborhoodTool, self)._initializeOptParser()
        group = self.argParser.add_argument_group("neighborhood options")
        group.add_argument(
            '--metric',
            type=str,
            default='cosine',
            choices=['cityblock', 'cosine', 'hamming', 'braycurtis', 'jaccard'],
            help="use this metric"
        )
        group.add_argument(
            '--disable-map-to-functions',
            action='store_true',
            help="use function ids as key"
        )
        group.add_argument(
            '-l', '--local-svd',
            action='store_true',
            help="perform local dimension reduction"
        )

    def _parseCommandLine(self):
        super(NeighborhoodTool, self)._parseCommandLine()
        if self.args.local_svd and not self.args.number_of_components:
            self.argParser.error("option '--local-svd' requires option '--number-of-components' to be set")

    def streamStart(self):
        # Load embedding
        try:
            self._load_embedding()
        except Exception as e:
            self.logger.error('Failed while loading embedding: %s', e.message)
            sys.exit(1)
        # Dimension reduction
        if not self.args.local_svd and self.args.number_of_components:
            self._x = self.perform_svd(self._x)
        self.__map = {}

    def write_neighborhood(self, target, neighborhood):
        self.write_fields([target] + neighborhood)

    def distances(self, x):
        y = pairwise_distances(x, metric=self.args.metric, n_jobs=2)
        if self.args.metric == 'cosine':
            np.clip(y, 0, 2, out=y)
            # y /= 2
        y = squareform(y, checks=False)
        return y

    def feature_matrix(self, datapoints):
        x = super(NeighborhoodTool, self).feature_matrix(datapoints)
        # Dimension reduction
        if self.args.local_svd and self.args.number_of_components:
            columns = np.unique(x.nonzero()[1])
            x = x[:, columns]
            x = self.perform_svd(x)
        return x

    def _map_to_function(self, ast_node):
        ast_node = int(ast_node)
        if ast_node not in self.__map:
            query = 'g.v({}).functionId'.format(ast_node)
            self.__map[ast_node] = int(self.run_query(query))
        return self.__map[ast_node]

    def get_index(self, node_id):
        if not self.args.disable_map_to_functions:
            node_id = self._map_to_function(node_id)
        return self.toc[node_id]

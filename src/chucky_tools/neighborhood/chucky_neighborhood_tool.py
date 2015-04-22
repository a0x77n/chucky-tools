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
            '--map-to-functions',
            action='store_false',
            help="use function ids as key"
        )
        group.add_argument(
            '-l', '--local-svd',
            action='store_true',
            help="perform local dimension reduction"
        )

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

    def process_fields(self, line):
        nodes = map(int, line)

        # If the embedding is based on function ids we need
        # to map each node to their function node ids.
        if self.args.map_to_functions:
            functions = self._map_to_functions(nodes)
            # Keep relation between nodes and their functions (the reverse mapping).
            # NOTICE: this is not a 1:1 relation
            d = {}
            for function, node in zip(functions[1:], nodes[1:]):
                if function not in d:
                    d[function] = []
                d[function].append(node)

            neighborhood = self.neighborhood(functions[0], functions[1:])
            # if neighborhood:
            # self.logger.info('Max. distance: {}'.format(self.diameter(neighborhood)))
            neighborhood = [d[function].pop(0) for function in neighborhood]
        else:
            neighborhood = self.neighborhood(nodes[0], nodes[1:])
            # if neighborhood:
            # self.logger.info('Max. distance: {}'.format(self.diameter(neighborhood)))

        self.write_neighborhood(nodes[0], neighborhood)

    def neighborhood(self, target, candidates):
        pass

    def write_neighborhood(self, target, neighborhood):
        self.write_fields([target] + neighborhood)

    def distances(self, x):
        y = pairwise_distances(x, metric=self.args.metric, n_jobs=2)
        if self.args.metric == 'cosine':
            np.clip(y, 0, 2, out=y)
            y /= 2
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

    def _map_to_functions(self, ast_nodes):
        query = 'idListToNodes({}).functionId'.format(ast_nodes)
        return map(int, self.run_query(query))

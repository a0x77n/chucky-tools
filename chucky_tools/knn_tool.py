import sys

from joerntools.KNN import KNN

from chucky_tools.base import ChuckyJoern
from chucky_tools.base import ChuckyLogger
from chucky_tools.base import FieldsTool


ARGPARSE_DESCRIPTION = """K-nearest neighbors tool."""
ARGPARSE_DEFAULT_N = 20


class KNNTool(FieldsTool, ChuckyJoern, ChuckyLogger):
    def __init__(self):
        super(KNNTool, self).__init__(ARGPARSE_DESCRIPTION)
        self._knn = None

    def _initializeOptParser(self):
        super(KNNTool, self)._initializeOptParser()
        self.argParser.add_argument(
            'embedding',
            type=str,
            help='directory containing the global api embedding'
        )
        self.argParser.add_argument(
            '-n', '--n-neighbors',
            type=int,
            default=ARGPARSE_DEFAULT_N,
            help='number of neighbors'
        )

    def streamStart(self):
        super(KNNTool, self).streamStart()
        self._init_knn()

    def _init_knn(self):
        self._knn = KNN()
        self._knn.setEmbeddingDir(self.args.embedding)
        self._knn.setK(self.args.n_neighbors + 1)
        self._knn.setNoCache(False)
        try:
            self._knn.initialize()
        except Exception as e:
            self.logger.error(
                'Failed while initializing k-nearest neighbor tool: %s',
                e.message)
            sys.exit(1)

    def process_fields(self, fields):
        node_ids = map(int, fields)
        function_ids = self._ast_node_ids_to_function_ids(node_ids)
        d = dict(zip(function_ids, node_ids))

        if len(node_ids) - 1 < self.args.n_neighbors:
            self.logger.warning('To few candidates.')
            self.write_fields(fields)
            return

        key = function_ids[0]
        limit = function_ids
        self._knn.setLimitArray(limit)
        neighbors = self._knn.getNeighborsFor(key)
        if key in neighbors:
            neighbors.remove(key)

        self.write_fields([d[key]] + [d[n] for n in neighbors])

    def _ast_node_ids_to_function_ids(self, ast_nodes):
        query = 'idListToNodes({}).functionId'.format(ast_nodes)
        return map(int, self.run_query(query))

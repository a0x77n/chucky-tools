import numpy as np

from chucky_tools.neighborhood import NeighborhoodTool

ARGPARSE_DESCRIPTION = """K-nearest neighbors tool. Reads lists of node IDs from the provided input and reduces each
list to the k-nearest neighbors with respect to the first list entry based on the provided features."""
ARGPARSE_DEFAULT_N = 20


class KNNTool(NeighborhoodTool):
    def __init__(self):
        super(KNNTool, self).__init__(ARGPARSE_DESCRIPTION)

    def _initializeOptParser(self):
        super(KNNTool, self)._initializeOptParser()
        group = self.argParser.add_argument_group('k-nearest neighbors options')
        group.add_argument(
            '-n', '--n-neighbors',
            type=int,
            default=ARGPARSE_DEFAULT_N,
            help='number of neighbors'
        )

    def process_fields(self, line):
	super(KNNTool, self).process_fields(line)
        nodes = map(int, line)
        self.neighborhood(nodes[0], nodes[1:])

    def neighborhood(self, target, candidates):
        neighbors = self.knn(target, candidates)
        self.write_neighborhood(target, neighbors)

    def knn(self, target, candidates):
        if len(candidates) - 1 < self.args.n_neighbors:
            self.logger.warning('To few candidates.')
            knn = candidates
        else:
            from sklearn.preprocessing import normalize

            x = self.feature_matrix([target] + candidates)
            x = normalize(x)
            d = 1.0 - (x[1:, :] * x[0, :].T).toarray().flatten()

            knn = [candidates[i] for i in np.argsort(d)[:self.args.n_neighbors]]

        return knn

import numpy as np

from chucky_tools.neighborhood import NeighborhoodTool

ARGPARSE_DESCRIPTION = """K-nearest neighbors tool."""
ARGPARSE_DEFAULT_N = 20


class KNNTool(NeighborhoodTool):
    def __init__(self):
        super(KNNTool, self).__init__(ARGPARSE_DESCRIPTION)
        self._knn = None

    def _initializeOptParser(self):
        super(KNNTool, self)._initializeOptParser()
        group = self.argParser.add_argument_group('k-nearest neighbors options')
        group.add_argument(
            '-n', '--n-neighbors',
            type=int,
            default=ARGPARSE_DEFAULT_N,
            help='number of neighbors'
        )

    def neighborhood(self, target, candidates):
        if len(candidates) - 1 < self.args.n_neighbors:
            self.logger.warning('To few candidates.')
            neighbors = candidates
        else:
            from sklearn.preprocessing import normalize

            x = self.feature_matrix([target] + candidates)
            x = normalize(x)
            d = 1.0 - (x[1:, :] * x[0, :].T).toarray().flatten()

            neighbors = [candidates[i] for i in np.argsort(d)[:self.args.n_neighbors]]

        # self.logger.info('Diameter : {}'.format(self.diameter([target] + neighbors)))
        return neighbors

    @property
    def knn(self):
        return self._knn

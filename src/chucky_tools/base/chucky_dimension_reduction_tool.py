from scipy.sparse import csr_matrix

from sklearn.decomposition import TruncatedSVD

from chucky_tools.base import ChuckyLogger


class DimensionReductionTool(ChuckyLogger):
    """
    A basic tool for performing dimension reduction.
    """

    def __init__(self, description):
        super(DimensionReductionTool, self).__init__(description)
        self._svd = None
        self.__is_initialized = False

    def _initializeOptParser(self):
        super(DimensionReductionTool, self)._initializeOptParser()
        group = self.argParser.add_argument_group("dimension reduction options")
        group.add_argument(
            '-c', '--number-of-components',
            type=int,
            default=None,
            help="desired number of dimensions after dimension reducion"
        )

    def perform_svd(self, x):
        if 0 < self.args.number_of_components < x.shape[1]:
            self.logger.debug("Performing dimension reduction ...")
            y = self.svd.fit_transform(x)
            z = csr_matrix(y)
            self.logger.info("Number of dimensions after reduction: {}".format(z.shape[1]))
            self.logger.info("Explained variance after reduction: {}".format(self.svd.explained_variance_ratio_.sum()))
            return z
        else:
            return x

    def _init_svd(self):
        self._svd = TruncatedSVD(n_components=self.args.number_of_components, algorithm='randomized',
                                 random_state=2, tol=0.001)

        self.__is_initialized = True

    @property
    def svd(self):
        if not self.__is_initialized:
            self._init_svd()
        return self._svd


import sys
import numpy as np

from sklearn.datasets import load_svmlight_file

from chucky_tools.base import ChuckyLogger


class ChuckyEmbeddingLoader(ChuckyLogger):
    """
    A basic tool for loading an embedding in libsvm/svmlight format.:wq
    """

    def __init__(self, description):
        super(ChuckyEmbeddingLoader, self).__init__(description)
        self._x = None
        self._y = None
        self._toc = None
        self.__is_initialized = False

    def _initializeOptParser(self):
        super(ChuckyEmbeddingLoader, self)._initializeOptParser()
        self.argParser.add_argument(
            'embedding',
            type=str,
            help="directory containing the embedding"
        )
        self.argParser.add_argument(
            '--toc',
            type=str,
            default=None,
            help="use toc file as labels"
        )

    def _load_embedding(self):
        try:
            self._x, self._y = load_svmlight_file(self.args.embedding)
            self._toc = self._create_toc()
            self.logger.info("Loaded dimensions: {}".format(self._x.shape[1]))
            columns = np.unique(self._x.nonzero()[1])
            self._x = self._x[:, columns]
            self.logger.info("Nonzero dimensions: {}".format(self._x.shape[1]))
            self.__is_initialized = True
        except Exception as e:
            self.logger.error('Failed while loading embedding: %s', e.message)
            sys.exit(1)

    def feature_matrix(self, datapoints):
        rows = [self.get_index(x) for x in datapoints]
        return self.x[rows, :]

    def _create_toc(self):
        if self.args.toc:
            with open(self.args.toc) as f:
                lines = [int(x.rstrip()) for x in f.readlines()]

            lines = [lines[int(self._y[i])] for i in range(len(lines))]
            return dict(zip(lines, range(len(lines))))
        else:
            return dict(self._y)

    def get_index(self, node_id):
        return self.toc[node_id]

    @property
    def number_of_features(self):
        return self.x.shape[1]

    @property
    def number_of_datapoints(self):
        return self.x.shape[0]

    @property
    def x(self):
        if not self.__is_initialized:
            self._load_embedding()
        return self._x

    @property
    def y(self):
        if not self.__is_initialized:
            self._load_embedding()
        return self._y

    @property
    def toc(self):
        if not self.__is_initialized:
            self._load_embedding()
        return self._toc

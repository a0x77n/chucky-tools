# from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import fcluster
from collections import Counter
from operator import itemgetter
from itertools import groupby

from fastcluster import linkage as fast_linkage

from chucky_tools.neighborhood import NeighborhoodTool

DESCRIPTION = """Cluster tool. Reads lists of node IDs from the provided input and splits each list in multiple list,
each representing a cluster based on the provided features. With compatibility mode enabled only the lists containing
the first list entries are returned."""


class ClusterTool(NeighborhoodTool):
    def __init__(self):
        super(ClusterTool, self).__init__(DESCRIPTION)
        self._global_cluster = None

    def _initializeOptParser(self):
        super(ClusterTool, self)._initializeOptParser()
        group = self.argParser.add_argument_group("cluster options")
        group.add_argument(
            '--algorithm',
            type=str,
            choices=['linkage'],
            default='linkage',
            help='the clustering algorithm'
        )
        group.add_argument(
            '-g', '--global-cluster',
            action='store_true',
            help='use global cluster rather than local cluster'
        )
        group.add_argument(
            '--compatibility-mode',
            action='store_true',
            help='use compatibility mode, i.e write target cluster only.'
        )
        linkage_group = self.argParser.add_argument_group('linkage parameters')
        linkage_group.add_argument(
            '--method',
            type=str,
            default='complete',
            choices=['single', 'complete', 'average', 'weighted', 'centroid']
        )
        linkage_group.add_argument(
            '--threshold',
            type=float,
            default=0.5,
            help='threshold used for forming flat clusters'
        )
        linkage_group.add_argument(
            '--criterion',
            type=str,
            default='distance',
            choices=['distance', 'maxclust'],
            help='criterion used in forming flat clusters'
        )

    def streamStart(self):
        super(ClusterTool, self).streamStart()
        if self.args.global_cluster:
            datapoints = self.toc.keys()
            labels = self.cluster(self.x)
            self._global_cluster = dict(zip(datapoints, labels))

    def process_fields(self, line):
        super(ClusterTool, self).process_fields(line)
        nodes = map(int, line)
        self.neighborhood(nodes[0], nodes[1:])

    def cluster(self, feature_matrix):
        self.logger.debug("Clustering {} datapoints ...".format(feature_matrix.shape[0]))
        self.logger.debug("Calculating distances ...")
        distances = self.distances(feature_matrix)
        self.logger.debug("Calculating linkage ...")
        z = fast_linkage(distances, self.args.method, self.args.metric, preserve_input=False)
        # z = linkage(distances, self.args.method, self.args.metric)
        self.logger.debug("Forming flat clusters ...")
        t = fcluster(z, t=self.args.threshold, criterion=self.args.criterion)

        cluster_sizes = Counter(t.tolist())
        cluster_sizes_dist = Counter(cluster_sizes.values())

        self.logger.debug('Number of clusters : {}'.format(len(cluster_sizes)))
        self.logger.debug(
            'Distribution of cluster sizes : {}'.format(
                ', '.join(map(lambda (size, freq): '{}:{}'.format(size, freq), cluster_sizes_dist.items()))))
        return t.tolist()

    def neighborhood(self, target, candidates):
        datapoints = [target] + candidates
        if not self.args.global_cluster:
            labels = self.cluster(self.feature_matrix(datapoints))
            clusters = dict(zip(datapoints, labels))
        else:
            clusters = {}
            for datapoint in datapoints:
                clusters[datapoint] = self.global_label(datapoint)

        # group datapoints by label
        data = sorted(clusters.items(), key=itemgetter(1))
        for cluster_label, datapoints in groupby(data, key=itemgetter(1)):
            cluster_data = list(map(itemgetter(0), datapoints))
            if not self.args.compatibility_mode:  # or cluster_label == clusters[target]:
                self.write_fields(cluster_data)
            elif cluster_label == clusters[target]:
                cluster_data.remove(target)
                self.write_neighborhood(target, cluster_data)

    def global_label(self, node_id):
        if self.args.disable_map_to_functions:
            return self._global_cluster[node_id]
        else:
            return self._global_cluster[self._map_to_function(node_id)]

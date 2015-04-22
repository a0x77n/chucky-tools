# from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import fcluster
from collections import Counter

from fastcluster import linkage as fast_linkage

from chucky_tools.neighborhood import NeighborhoodTool


DESCRIPTION = """Cluster tool."""


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
            labels = self.cluster(datapoints)
            self._global_cluster = dict(zip(datapoints, labels))


    def cluster(self, datapoints):
        self.logger.debug("Clustering {} datapoints ...".format(len(datapoints)))
        self.logger.debug("Calculating distances ...")
        x = self.feature_matrix(datapoints)
        distances = self.distances(x)
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
        if not self.args.global_cluster:
            datapoints = [target] + candidates
            labels = self.cluster(datapoints)
            local_cluster = dict(zip(datapoints, labels))
            target_label = local_cluster[target]
            cluster = [x for x in candidates if local_cluster[x] == target_label]
            cluster_size = len(cluster) + 1
            self.logger.info('Cluster size : {}'.format(cluster_size))
        else:
            target_label = self.global_label(target)
            cluster = [x for x in candidates if self.global_label(x) == target_label]
            cluster_size = len(cluster) + 1
            global_cluster_size = self._global_cluster.values().count(target_label)
            self.logger.info('Cluster size : {} ({})'.format(cluster_size, global_cluster_size))

            # self.logger.info('Diameter : {}'.format(self.diameter(cluster)))

        return cluster

    def global_label(self, node_id):
        return self._global_cluster[node_id]

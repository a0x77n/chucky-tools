from chucky_tools.base import ChuckyJoern
from chucky_tools.base import BatchTool, ChuckyLogger

ARGPARSE_DESCRIPTION = """Simple traversal tool. Perform a traversal
starting at a list of start nodes."""

QUERY = 'idListToNodes({}).transform{{ it.{}.id.toList() }}'


class TraversalTool(BatchTool, ChuckyJoern, ChuckyLogger):
    def __init__(self):
        super(TraversalTool, self).__init__(ARGPARSE_DESCRIPTION)
        self._traversal = None

    def _initializeOptParser(self):
        super(TraversalTool, self)._initializeOptParser()
        self.argParser.add_argument(
            'traversal',
            type=str,
            help='the traversal'
        )
        self.argParser.add_argument(
            '-c', '--column',
            type=int,
            default=0,
            help='the column containing the start nodes'
        )
        self.argParser.add_argument(
            '-e', '--echo',
            action='store_true',
            default=False,
            help='''echo the input line in the first fields of the
            output line'''
        )
        self.argParser.add_argument(
            '-r', '--read',
            action='store_true',
            default=False,
            help='read traversal from file'
        )

    def process_batch(self, batch):
        start_nodes = [int(x[self.args.column]) for x in batch]
        query = QUERY.format(start_nodes, self.traversal)
        result = self.run_query(query)
        for line, nodes in zip(batch, result):
            if not nodes:
                continue
            if self.args.echo:
                self.write_fields(line + nodes)
            else:
                self.write_fields(nodes)

    @property
    def traversal(self):
        if not self._traversal:
            if self.args.read:
                with open(self.args.traversal) as f:
                    self._traversal = f.read().strip()
            else:
                self._traversal = self.args.traversal
        return self._traversal

import os.path as path

from chucky_tools.base import ChuckyJoern
from chucky_tools.base import GroupedBatchTool


ARGPARSE_BATCH_SIZE = None
ARGPARSE_DESCRIPTION = """Statement tainter."""

STEPS_DIR = path.join(path.dirname(__file__), 'data', 'steps')

TAINT_FORWARD_QUERY = 'idListToNodes({}).transform{{ it.taintForward("{}", {}).id.toList(); }}'
TAINT_BACKWARD_QUERY = 'idListToNodes({}).transform{{ it.taintBackward("{}", {}).id.toList(); }}'


class TaintTool(GroupedBatchTool, ChuckyJoern):
    def __init__(self):
        super(TaintTool, self).__init__(ARGPARSE_DESCRIPTION)
        self._query = None

    def _initializeOptParser(self):
        super(TaintTool, self)._initializeOptParser()
        self.argParser.add_argument(
            '-k', '--max-hops',
            type=int,
            default=5,
            help='the maximum number of edges to follow'
        )
        self.argParser.add_argument(
            '-e', '--echo',
            action='store_true',
            default=True,
            help='''echo the input line'''
        )
        self.argParser.add_argument(
            '-m', '--mode',
            action='store',
            choices=['forward', 'backward'],
            default='forward',
            help='tainting mode'
        )
        self.argParser.add_argument(
            '-s', '--statement',
            type=int,
            default=0
        )
        self.argParser.add_argument(
            '-i', '--identifier',
            type=int,
            default=1
        )

    def streamStart(self):
        super(TaintTool, self).streamStart()
        self._init_joern_interface(STEPS_DIR)
        if self.args.mode == 'forward':
            self._query = TAINT_FORWARD_QUERY
        else:
            self._query = TAINT_BACKWARD_QUERY
        self._group_by_columns = [self.args.identifier]

    def process_group(self, group_key, group_data):
        statement_ids = map(lambda x: x[self.args.statement], group_data)
        identifier = group_key[0]

        query = self._query.format(statement_ids, identifier, self.args.max_hops)
        results = self.run_query(query)
        for line, result in zip(group_data, results):
            if not result:
                continue
            if self.args.echo:
                self.write_fields(line + result)
            else:
                self.write_fields(result)

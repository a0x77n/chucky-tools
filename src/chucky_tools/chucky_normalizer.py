from chucky_tools.base import ChuckyJoern
from chucky_tools.base import GroupedBatchTool

ARGPARSE_DESCRIPTION = """Condition normalization tool."""

QUERY = "idListToNodes({}).transform{{ it.normalize(['{}' : '$SYM']).toList() }}"


class ChuckyNormalizer(GroupedBatchTool, ChuckyJoern):
    def __init__(self):
        super(ChuckyNormalizer, self).__init__(ARGPARSE_DESCRIPTION)

    def _initializeOptParser(self):
        super(ChuckyNormalizer, self)._initializeOptParser()
        self.argParser.add_argument(
            '-e', '--echo',
            action='store_true',
            default=True,
            help='''echo the input line'''
        )
        self.argParser.add_argument(
            '-c', '--condition',
            type=int,
            default=0,
            help='the column containing the node id of a condition'
        )
        self.argParser.add_argument(
            '-s', '--symbol',
            type=int,
            default=0,
            help='the column containing the symbol name '
        )

    def streamStart(self):
        super(ChuckyNormalizer, self).streamStart()
        self._group_by_columns = [self.args.symbol]

    def process_group(self, group_key, group_data):
        statement_ids = map(lambda x: int(x[self.args.condition]), group_data)
        symbol = group_key[0]

        query = QUERY.format(statement_ids, symbol)
        results = self.run_query(query)
        for line, result in zip(group_data, results):
            if self.args.echo:
                self.write_fields(line + result)
            else:
                self.write_fields(result)

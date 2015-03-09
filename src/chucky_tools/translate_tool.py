from chucky_tools.base import BatchTool
from chucky_tools.base import ChuckyJoern
from chucky_tools.base import field_select, attribute_escape

ARGPARSE_DESCRIPTION = """Simple translation tool. Replace node/edge
ids by an attribute."""


class TranslateTool(BatchTool, ChuckyJoern):
    def __init__(self):
        super(TranslateTool, self).__init__(ARGPARSE_DESCRIPTION)
        self._query = None

    def _initializeOptParser(self):
        super(TranslateTool, self)._initializeOptParser()
        self.argParser.add_argument(
            'attribute',
            type=str,
            help='the attribute'
        )
        self.argParser.add_argument(
            '-t', '--type',
            type=str,
            choices=['node', 'edge'],
            default='node',
            help='''the interpretation of the id'''
        )
        self.argParser.add_argument(
            '-c', '--columns',
            type=int,
            nargs='+',
            default=None,
            help='''translate only these columns'''
        )

    def streamStart(self):
        super(TranslateTool, self).streamStart()
        if self.args.type == 'node':
            self._query = 'idListToNodes({}).{}'
        else:
            self._query = 'idListToEdges({}).{}'

    def process_batch(self, batch):
        nodes = []
        for line in batch:
            if self.args.columns:
                selection = map(int, field_select(line, self.args.columns))
            else:
                selection = map(int, line)
            nodes.extend(selection)

        nodes = list(set(nodes))
        query = self._query.format(nodes, attribute_escape(self.args.attribute))
        attributes = self.run_query(query)
        translation = dict(zip(nodes, attributes))

        for line in batch:
            for column in xrange(len(line)):
                if not self.args.columns or column in self.args.columns:
                    line[column] = str(translation[int(line[column])])
                else:
                    line[column] = line[column]
            self.write_fields(line)

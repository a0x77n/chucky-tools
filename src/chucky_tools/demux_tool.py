from chucky_tools.base import FieldsTool
from chucky_tools.base import field_select, field_select_complement

ARGPARSE_DESCRIPTION = """Demultiplexing tool. Split lines by a set of
columns used as keys."""


class DemuxTool(FieldsTool):
    def __init__(self, description=None):
        super(DemuxTool, self).__init__(ARGPARSE_DESCRIPTION)

    def _initializeOptParser(self):
        super(DemuxTool, self)._initializeOptParser()
        self.argParser.add_argument(
            '-k', '--keys',
            type=int,
            nargs='+',
            default=[0],
            help='''use these column(s) as key(s)'''
        )

    def process_fields(self, fields):
        keys = field_select(fields, self.args.keys)
        values = field_select_complement(fields, self.args.keys)
        for value in values:
            self.write_fields(list(keys) + [value])

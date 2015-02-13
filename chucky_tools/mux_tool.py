from chucky_tools.base import GroupTool
from chucky_tools.base import field_select_complement

ARGPARSE_DESCRIPTION = """Multiplexing tool. Merge lines by a set of
columns used as keys."""


class MuxTool(GroupTool):
    def __init__(self, description=None):
        super(MuxTool, self).__init__(ARGPARSE_DESCRIPTION)

    def _initializeOptParser(self):
        super(MuxTool, self)._initializeOptParser()
        self.argParser.add_argument(
            '-k', '--keys',
            type=int,
            nargs='+',
            default=[0],
            help='''use these column(s) as key(s)'''
        )

    def streamStart(self):
        super(MuxTool, self).streamStart()
        self._group_by_columns = self.args.keys

    def process_group(self, group_key, group_data):
        fields = list(group_key)
        for data in group_data:
            fields.extend(field_select_complement(data, self.args.keys))
        self.write_fields(fields)



from .chucky_group_tool import GroupTool
from .misc import field_select

ARGPARSE_BATCH_SIZE = 256


class GroupedBatchTool(GroupTool):
    """
    A basic tool that groups input lines by common fields and before processing.
    Groups are processed after a fixed size is reached or all lines are consumed.
    """

    def _initializeOptParser(self):
        super(GroupedBatchTool, self)._initializeOptParser()
        self.argParser.add_argument(
            '-b', '--batch-size',
            type=int,
            default=ARGPARSE_BATCH_SIZE,
            help="""the amount of input lines handled at once"""
        )

    def process_fields(self, fields):
        super(GroupedBatchTool, self).process_fields(fields)
        key = field_select(fields, self._group_by_columns)
        if len(self._groups[key]) == self.args.batch_size:
            self.process_group(key, self._groups[key])
            del self._groups[key]



from chucky_tools.base.chucky_fields_tool import FieldsTool


ARGPARSE_DESCRIPTION = """Rotate input lines."""


class RotateTool(FieldsTool):
    def __init__(self, description=None):
        super(RotateTool, self).__init__(ARGPARSE_DESCRIPTION)

    def process_fields(self, fields):
        for i in xrange(len(fields)):
            self.write_fields(fields[i:] + fields[0:i])
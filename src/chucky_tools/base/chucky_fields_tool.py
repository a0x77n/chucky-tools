import os

from joerntools.shelltool.PipeTool import PipeTool


ARGPARSE_DELIMITER = '\t'


class FieldsTool(PipeTool):
    """
    A pipetool that splits input lines by a delimiter into fields before processing.
    """

    def _initializeOptParser(self):
        super(FieldsTool, self)._initializeOptParser()
        self.argParser.add_argument(
            '--delimiter',
            type=str,
            default=ARGPARSE_DELIMITER,
            help="""the input and output field delimiter"""
        )

    def processLine(self, line):
        self.process_fields(line.split(self.args.delimiter))

    def process_fields(self, fields):
        pass

    def write_fields(self, fields):
        self.output(self.args.delimiter.join(map(str, fields)))
        self.output(os.linesep)

    @classmethod
    def main(cls):
        cls().run()

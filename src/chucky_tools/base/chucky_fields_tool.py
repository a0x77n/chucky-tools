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
        self.argParser.add_argument(
            '--echo-comments',
            action='store_true',
            help="""echo comments from input to output"""
        )

    def processLine(self, line):
        if line.startswith('#'):
            if self.args.echo_comments:
                self.output(line)
                self.output(os.linesep)
        else:
            self.process_fields(line.split(self.args.delimiter))

    def process_fields(self, fields):
        pass

    def write_fields(self, fields):
        self.output(self.args.delimiter.join(map(str, fields)))
        self.output(os.linesep)

    @classmethod
    def main(cls):
        cls().run()

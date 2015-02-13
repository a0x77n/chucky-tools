from .chucky_fields_tool import FieldsTool

ARGPARSE_BATCH_SIZE = 1024


class BatchTool(FieldsTool):
    """
    A basic tool that accumulates input lines into batches before processing.
    Batches are processed after a fixed size is reached or all lines are consumed.
    """

    def __init__(self, description):
        super(BatchTool, self).__init__(description)
        self._batch = None

    def _initializeOptParser(self):
        super(BatchTool, self)._initializeOptParser()
        self.argParser.add_argument(
            '-b', '--batch-size',
            type=int,
            default=ARGPARSE_BATCH_SIZE,
            help="""the amount of input lines handled at once"""
        )

    def streamStart(self):
        self._batch = []

    def streamEnd(self):
        if self._batch:
            self.process_batch(self._batch)

    def process_fields(self, fields):
        self._batch.append(fields)
        if len(self._batch) == self.args.batch_size:
            self.process_batch(self._batch)
            self._batch = []

    def process_batch(self, batch):
        pass

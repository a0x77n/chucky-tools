import os
import sys
import shutil

from chucky_tools.base import FieldsTool
from chucky_tools.base import ChuckyLogger


DESCRIPTION = """Data directory creator."""


class StoreTool(FieldsTool, ChuckyLogger):
    def __init__(self):
        super(StoreTool, self).__init__(DESCRIPTION)
        self._data_dir = None
        self._toc_file = None
        self._toc = None

    def _initializeOptParser(self):
        super(StoreTool, self)._initializeOptParser()
        self.argParser.add_argument(
            'output',
            type=str,
            help='the output directory'
        )
        self.argParser.add_argument(
            '--force',
            action='store_true',
            default=False,
            help='overwrite existing directories'
        )

    def streamStart(self):
        if os.path.exists(self.args.output):
            if self.args.force:
                self.logger.info("Directory exists. Removing directory.")
                shutil.rmtree(self.args.output)
            else:
                self.logger.error("Directory exists.")
                self.logger.error("Remove directory first or use --force")
                sys.exit(0)
        self._data_dir = os.path.join(self.args.output, 'data')
        self._toc_file = os.path.join(self.args.output, 'TOC')
        os.makedirs(self._data_dir)

        self._toc = {}

    def streamEnd(self):
        with open(self._toc_file, 'w') as f:
            for key, _ in sorted(self._toc.items(), key=lambda x: x[1]):
                f.write(key)
                f.write(os.linesep)

    def process_fields(self, line):
        key = line[0]
        features = line[1:]
        if key not in self._toc:
            self._toc[key] = len(self._toc)

        self._write_data(self._toc[key], features)

    def _write_data(self, suffix, data):
        with open(os.path.join(self._data_dir, str(suffix)), 'a') as f:
            for feature in data:
                f.write(feature)
                f.write(os.linesep)

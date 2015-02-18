import logging

from joerntools.shelltool.CmdLineTool import CmdLineTool

ARGPARSE_DEFAULT_LOGGING_LEVEL = logging.WARNING


class ChuckyLogger(CmdLineTool):
    """
    Logging support for chucky tools.
    """

    def __init__(self, description=None):
        super(ChuckyLogger, self).__init__(description)
        self._logger = None
        self.__is_initialized = False

    def _initializeOptParser(self):
        super(ChuckyLogger, self)._initializeOptParser()
        logging_group = self.argParser.add_argument_group(
            "logging levels")
        group = logging_group.add_mutually_exclusive_group()
        group.add_argument(
            '-d', '--debug',
            action='store_const',
            const=logging.DEBUG,
            dest='logging_level',
            default=ARGPARSE_DEFAULT_LOGGING_LEVEL,
            help="""enable debug output""")
        group.add_argument(
            '-v', '--verbose',
            action='store_const',
            const=logging.INFO,
            dest='logging_level',
            default=ARGPARSE_DEFAULT_LOGGING_LEVEL,
            help="""increase verbosity""")
        group.add_argument(
            '-q', '--quiet',
            action='store_const',
            const=logging.ERROR,
            dest='logging_level',
            default=ARGPARSE_DEFAULT_LOGGING_LEVEL,
            help="""be quiet during processing""")

    def _init_logger(self, level):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
        self.__is_initialized = True

    @property
    def logger(self):
        if not self.__is_initialized:
            self._init_logger(self.args.logging_level)
        return self._logger

from joerntools.shelltool.CmdLineTool import CmdLineTool
from joern.all import JoernSteps, DEFAULT_GRAPHDB_URL


class ChuckyJoern(CmdLineTool):
    """
    Joern interface used by chucky tools.
    """

    def __init__(self, description):
        super(ChuckyJoern, self).__init__(description)
        self._joern = None
        self.__is_initialized = False

    def _initializeOptParser(self):
        super(ChuckyJoern, self)._initializeOptParser()
        group = self.argParser.add_argument_group("joern options")
        group.add_argument(
            '--steps',
            type=str,
            nargs='+',
            default=[],
            help='load additional steps from directory'
        )
        group.add_argument(
            '--uri',
            type=str,
            default=DEFAULT_GRAPHDB_URL,
            help='the uniform resource identifier of the database'
        )

    def _init_joern_interface(self):
        self._joern = JoernSteps()
        self._joern.connectToDatabase()

        self._joern.stepsDirs = []
        for directory in self.args.steps:
            self._joern.addStepsDir(directory)
        self._joern.sendInitCommand()

        self.__is_initialized = True

    def run_query(self, query):
        return self.joern.runGremlinQuery(query)

    @property
    def joern(self):
        if not self.__is_initialized:
            self._init_joern_interface()
        return self._joern

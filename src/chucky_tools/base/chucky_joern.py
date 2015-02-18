from joerntools.shelltool.CmdLineTool import CmdLineTool
from joern.all import JoernSteps


class ChuckyJoern(CmdLineTool):
    """
    Joern interface used by chucky tools.
    """

    def __init__(self, description):
        super(ChuckyJoern, self).__init__(description)
        self._joern = None
        self.__is_initialized = False

    def _init_joern_interface(self, step_dir=None):
        self._joern = JoernSteps()
        if step_dir:
            self._joern.addStepsDir(step_dir)
        self._joern.connectToDatabase()
        self.__is_initialized = True

    def run_query(self, query):
        return self.joern.runGremlinQuery(query)

    @property
    def joern(self):
        if not self.__is_initialized:
            self._init_joern_interface()
        return self._joern

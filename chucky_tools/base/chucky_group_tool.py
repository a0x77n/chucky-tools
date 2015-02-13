from .chucky_fields_tool import FieldsTool
from .misc import field_select


class GroupTool(FieldsTool):
    """
    A basic tool that groups input lines by common fields before processing.
    Groups are processed after all lines are consumed.
    """

    def __init__(self, description):
        super(GroupTool, self).__init__(description)
        self._groups = None
        self._group_by_columns = None

    def streamStart(self):
        self._groups = {}
        self._group_by_columns = [0]

    def streamEnd(self):
        for key, data in self._groups.items():
            self.process_group(key, data)

    def process_fields(self, fields):
        key = field_select(fields, self._group_by_columns)
        if key not in self._groups:
            self._groups[key] = []
        self._groups[key].append(fields)

    def process_group(self, group_key, group_data):
        pass

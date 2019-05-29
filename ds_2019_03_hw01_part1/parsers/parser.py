import abc
from typing import List, Dict, AnyStr, Any


class Parser(object):
    """Abstract class for data parsing to exact attributes (fields)"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, fields=None):
        self.fields = fields
        self.fields_set = set(fields) if fields is not None else None

    @abc.abstractmethod
    def parse(self, data: Any) -> List[Dict[AnyStr, Any]]:

        return [{f: None for f in self.fields}]

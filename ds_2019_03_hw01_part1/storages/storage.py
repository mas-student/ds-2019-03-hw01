import abc
from typing import Dict, List


class Storage(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read_data(self) -> Dict[str, List]:
        raise NotImplementedError

    @abc.abstractmethod
    def write_data(self, data: Dict[str, List]):
        raise NotImplementedError

    @abc.abstractmethod
    def append_data(self, data: Dict[str, List]):
        raise NotImplementedError

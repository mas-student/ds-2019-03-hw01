import logging
from typing import Dict, List
import pandas as pd

from ds_2019_03_hw01_part1.storages.storage import Storage


logger = logging.getLogger(__name__)


class DataFrameStorage(Storage):
    def __init__(self, dtypes: Dict[str, List]):
        self.dtypes = dtypes
        self.data_frame = pd.DataFrame(
            {key: pd.Series([], dtype=value) for key, value in dtypes.items()}
        )

    def read_data(self) -> Dict[str, List]:
        return {column: self.data_frame[column] for column in self.data_frame.columns}

    def write_data(self, data: Dict[str, List]):

        logger.debug(
            'Writing data keys = {} lengths {}'.format(
                list(data.keys()), list(map(len, data.values()))
            ),
            extra={'data': data},
        )

        if not set(self.dtypes.keys()).issuperset(set(data.keys())):
            msg = 'Data to write contains unknown keys'
            logger.error(
                msg, extra={'dtypes_keys': self.dtypes.keys(), 'data_keys': data.keys()}
            )
            raise ValueError(msg)

        self.data_frame = pd.DataFrame(
            {
                key: pd.Series(data.get(key, []), dtype=self.dtypes[key])
                for key in self.dtypes.keys()
            }
        )

    def append_data(self, data: Dict[str, List]):
        logger.debug(
            'data to append',
            extra={'keys': list(data.keys()), 'lengths': list(map(len, data.values()))},
        )

        if not set(self.dtypes.keys()).issuperset(set(data.keys())):
            msg = 'Data to append contains unknown columns'
            logger.error(
                msg, extra={'dtypes_keys': self.dtypes.keys(), 'data_keys': data.keys()}
            )
            raise ValueError(msg)

        if self.data_frame.shape[0] != 0 and set(self.data_frame.columns) != set(
            data.keys()
        ):
            msg = 'New columns do not match old columns'
            logger.warning(
                msg,
                extra={'old': list(self.data_frame.columns), 'new': list(data.keys())},
            )

        temp_series = {}

        for key in data:
            idx = list(
                range(
                    self.data_frame[key].size,
                    self.data_frame[key].size + len(data[key]),
                )
            )
            series = self.data_frame[key].append(pd.Series(data[key], index=idx))

            temp_series[key] = series

        self.data_frame = pd.DataFrame(
            {
                key: pd.Series(temp_series.get(key, []), dtype=value)
                for key, value in self.dtypes.items()
            }
        )

import unittest
from unittest.mock import patch
import responses

from ds_2019_03_hw01_part1.scrappers.scrapper import Scrapper
from ds_2019_03_hw01_part1.storages.dataframe_storage import DataFrameStorage
from ds_2019_03_hw01_part1.core.constants import IMDB_TITLE_TYPES
from ds_2019_03_hw01_part1.test.test_data import single_data, multiple_data


class TestScrapperParser(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = DataFrameStorage(IMDB_TITLE_TYPES)
        self.scrapper = Scrapper()

    @responses.activate
    def test_single(self):
        responses.add(
            responses.GET,
            'https://www.imdb.com/search/title?title=example&count=1&start=0',
            body=single_data.encode('utf-8'),
        )

        self.scrapper.scrap_process(self.storage, limit=1)

        self.assertEqual((1, 7), self.storage.data_frame.shape)
        self.assertCountEqual(IMDB_TITLE_TYPES.keys(), self.storage.data_frame.columns)

    @responses.activate
    def test_multiple(self):
        responses.add(
            responses.GET,
            'https://www.imdb.com/search/title?title=example&count=10&start=0',
            body=multiple_data.encode('utf-8'),
        )

        self.scrapper.scrap_process(self.storage)

        self.assertEqual((2, 7), self.storage.data_frame.shape)
        self.assertCountEqual(IMDB_TITLE_TYPES.keys(), self.storage.data_frame.columns)

    @patch('ds_2019_03_hw01_part1.scrappers.scrapper.fetch')
    def test_title(self, mock_fetch):
        mock_fetch.return_value = single_data

        self.scrapper.scrap_process(self.storage)

        mock_fetch.assert_called()
        mock_fetch.assert_called_with(
            'https://www.imdb.com/search/title?title=example&count=10&start=0'
        )

        self.scrapper.scrap_process(self.storage, title='another')

        mock_fetch.assert_called()
        mock_fetch.assert_called_with(
            'https://www.imdb.com/search/title?title=another&count=10&start=0'
        )

    @patch('ds_2019_03_hw01_part1.scrappers.scrapper.fetch')
    def test_limit(self, mock_fetch):
        mock_fetch.return_value = single_data

        self.scrapper.scrap_process(self.storage)

        mock_fetch.assert_called()
        mock_fetch.assert_called_with(
            'https://www.imdb.com/search/title?title=example&count=10&start=0'
        )

        self.scrapper.scrap_process(self.storage, limit=1)

        mock_fetch.assert_called()
        mock_fetch.assert_called_with(
            'https://www.imdb.com/search/title?title=example&count=1&start=0'
        )

import unittest

from ds_2019_03_hw01_part1.storages.dataframe_storage import DataFrameStorage
from ds_2019_03_hw01_part1.core.constants import IMDB_TITLE_TYPES


class TestDataFrameStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.instance = DataFrameStorage(IMDB_TITLE_TYPES)

    def test_unknown_columns(self):
        data = {
            'title': ['Eyes of the Roshi'],
            'year': ['2017'],
            'link': ['/title/tt3729774/?ref_=adv_li_tt'],
            'rating': [7.7],
            'votes': [27],
            'genre': ['Action'],
            'runtime': ['90 min'],
            'ufo': ['Flying saucer'],
        }

        with self.assertRaises(ValueError) as context:
            self.instance.write_data(data)

        self.assertTrue('Data to write contains unknown keys' in str(context.exception))

    def test_write_data(self):
        data = {
            'title': ['Eyes of the Roshi'],
            'year': ['2017'],
            'link': ['/title/tt3729774/?ref_=adv_li_tt'],
            'rating': [7.7],
            'votes': [27],
            'genre': ['Action'],
            'runtime': ['90 min'],
        }

        self.instance.write_data(data)

        dump = {
            key: list(self.instance.data_frame[key]) for key in IMDB_TITLE_TYPES.keys()
        }

        self.assertEqual(['Eyes of the Roshi'], dump['title'])
        self.assertEqual(['2017'], dump['year'])
        self.assertEqual(['/title/tt3729774/?ref_=adv_li_tt'], dump['link'])
        self.assertEqual([7.7], dump['rating'])
        self.assertEqual([27], dump['votes'])
        self.assertEqual(['Action'], dump['genre'])
        self.assertEqual(['90 min'], dump['runtime'])

    def test_append_data(self):
        data1 = {
            'title': ['0'],
            'year': ['0'],
            'link': ['0'],
            'rating': [0],
            'votes': [0],
            'genre': ['0'],
            'runtime': ['0'],
        }
        data2 = {
            'title': ['Eyes of the Roshi'],
            'year': ['2017'],
            'link': ['/title/tt3729774/?ref_=adv_li_tt'],
            'rating': [7.7],
            'votes': [27],
            'genre': ['Action'],
            'runtime': ['90 min'],
        }

        self.instance.write_data(data1)

        self.instance.append_data(data2)

        dump = {
            key: list(self.instance.data_frame[key]) for key in IMDB_TITLE_TYPES.keys()
        }

        self.assertEqual(['0', 'Eyes of the Roshi'], dump['title'])
        self.assertEqual(['0', '2017'], dump['year'])
        self.assertEqual(['0', '/title/tt3729774/?ref_=adv_li_tt'], dump['link'])
        self.assertEqual([0, 7.7], dump['rating'])
        self.assertEqual([0, 27], dump['votes'])
        self.assertEqual(['0', 'Action'], dump['genre'])
        self.assertEqual(['0', '90 min'], dump['runtime'])

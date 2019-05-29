# -*- coding: utf8 -*-


import unittest
from ds_2019_03_hw01_part1.parsers.imdb_parser import ImdbParser
from ds_2019_03_hw01_part1.test.test_data import single_data


class TestImdbParser(unittest.TestCase):
    def test_parse(self):
        parser = ImdbParser()
        items = list(parser.parse(single_data.encode('utf-8')))

        self.assertEqual(1, len(items))

        data = items[0]

        self.assertEqual('Eyes of the Roshi', data['title'])
        self.assertEqual('2017', data['year'])
        self.assertEqual('/title/tt3729774/?ref_=adv_li_tt', data['link'])
        self.assertEqual('7.7', data['rating'])
        self.assertEqual('27', data['votes'])
        self.assertEqual('Action', data['genre'])
        self.assertEqual('90 min', data['runtime'])

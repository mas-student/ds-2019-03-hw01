from ds_2019_03_hw01_part1.parsers.parser import Parser

from bs4 import BeautifulSoup
from typing import List, Dict, AnyStr, Any


class HtmlParser(Parser):

    root_selector = None
    selectors = {}

    def extract_by_selector(self, root, selector: List):
        value = None
        options = None
        sub_element = root

        for sub_selector in selector:
            if not sub_element:
                break
            if type(sub_selector) == tuple:
                sub_element = sub_element.find(
                    sub_selector[0], {sub_selector[1]: sub_selector[2]}
                )
            elif type(sub_selector) == dict:
                options = sub_selector
            else:
                sub_element = sub_element.find(sub_selector)

        if sub_element is not None:
            if options and 'attr' in options:
                value = sub_element.attrs[options['attr']]
            else:
                value = sub_element.get_text()
            if options and 'strip' in options:
                value = value.strip(options['strip'])
            if options and options.get('type') in ['year']:
                value = value.strip('()')
            if options and options.get('type') in ['int']:
                value = value.strip(' ').replace(',', "")

        return value

    def parse(self, data: bytes, limit: int = 10) -> List[Dict[AnyStr, Any]]:
        if not self.root_selector:
            raise NotImplementedError('root_selector not defined')

        if not self.selectors:
            raise NotImplementedError('selectors not defined')

        if self.fields_set is not None:
            selectors = {
                key: value
                for key, value in self.selectors.items()
                if key in self.fields_set
            }
        else:
            selectors = self.selectors

        results = []
        soup = BeautifulSoup(data, features='html.parser')
        elements = soup.findAll(
            self.root_selector[0], {self.root_selector[1]: self.root_selector[2]}
        )

        for element in elements:
            if len(results) >= limit:
                break

            data = {}
            for key, selector in selectors.items():
                data[key] = self.extract_by_selector(element, selector)

            results.append(data)

        return results

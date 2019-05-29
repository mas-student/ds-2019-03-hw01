from ds_2019_03_hw01_part1.parsers.html_parser import HtmlParser


class ImdbParser(HtmlParser):

    root_selector = ('div', 'class', 'lister-item')
    selectors = {
        'title': [('h3', 'class', 'lister-item-header'), 'a'],
        'year': [('span', 'class', 'lister-item-year'), {'type': 'year'}],
        'link': [('h3', 'class', 'lister-item-header'), 'a', {'attr': 'href'}],
        'rating': [('div', 'class', 'ratings-bar'), 'strong'],
        'votes': [
            ('p', 'class', 'sort-num_votes-visible'),
            ('span', 'name', 'nv'),
            {'type': 'int'},
        ],
        'genre': [('span', 'class', 'genre'), {'strip': ' \n'}],
        'runtime': [('span', 'class', 'runtime'), {'strip': ' \n'}],
    }

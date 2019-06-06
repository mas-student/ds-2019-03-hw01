import logging
from typing import List
import requests
import math
from datetime import date

from ds_2019_03_hw01_part1.parsers.imdb_parser import ImdbParser
from ds_2019_03_hw01_part1.storages.storage import Storage
from ds_2019_03_hw01_part1.core.constants import IMDB_TITLE_TYPES


logger = logging.getLogger(__name__)


def fetch(url):
    try:
        response = requests.get(url)

    except Exception as e:
        logger.error('Fetching failed: {}: {}'.format(str(e), url))
        return

    if not response.ok:
        logger.error(
            'Request is not valid: {}: {}'.format(url, response.status_code),
            extra={'url': url, 'code': response.status_code, 'message': response.text},
        )
        return

    else:
        return response.text


class Scrapper(object):
    parser_class = ImdbParser
    initial_url = (
        'https://www.imdb.com/search/title?release_date={release_date_from},{release_date_to}&count={count}&start={start}'
    )
    per_page = 250

    def __init__(self, skip_objects: List = None):
        self.skip_objects = skip_objects or []

    def scrap_process(
            self,
            storage: Storage,
            release_date_from: date = None,
            release_date_to: date = None,
            title: str = 'example',
            limit: int = 10
        ):
        parser = self.parser_class()

        release_date_from = release_date_from or date.today()
        release_date_to = release_date_to or date.today()
        per_page = min(self.per_page, limit)
        page_count = math.ceil(limit / self.per_page)
        rest = limit

        for page_no in range(page_count):
            url = self.initial_url.format(
                release_date_from=release_date_from.strftime('%Y-%m-%d'),
                release_date_to=release_date_to.strftime('%Y-%m-%d'),
                title=title,
                start=page_no * self.per_page,
                count=per_page
            )

            logging.info('Start scrapping', extra={'url': url})

            text = fetch(url)

            if text is None:
                continue

            items = list(parser.parse(text, limit=limit))

            items = items[: min(self.per_page, rest)]

            if len(items) == 0:
                logger.debug('zero objects count', extra={'url': url})
                break

            logging.debug(
                'parsed objects from html content', extra={'url': url, 'items': items}
            )

            data = {
                key: [item.get(key) for item in items]
                for key in IMDB_TITLE_TYPES.keys()
            }

            storage.append_data(data)

            rest -= self.per_page

            logging.info('finish scrapping page', extra={url: url})

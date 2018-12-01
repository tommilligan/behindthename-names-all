import csv
import os
import sys
import logging
from itertools import count
from typing import Optional, List, Iterable


import attr
from bs4 import BeautifulSoup, SoupStrainer
import requests

BEHINDTHENAMES_ROOT = "https://surnames.behindthename.com/"

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stderr)
root_logger.handlers = [ch]
_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

def get_and_assert_ok(url: str):
    r = requests.get(url)
    assert r.status_code == 200
    return r



@attr.s(auto_attribs=True, frozen=True, slots=True)
class Name:
    description: str
    text: str
    usage: str

    @staticmethod
    def from_listing(soup) -> "Name":
        usage=soup.contents[1].text,
        text=soup.contents[0].text,

        soup.contents = soup.contents[2:]
        description = soup.text
        return Name(
            description=description,
            usage=usage[0],
            text=text[0],
        )


@attr.s(auto_attribs=True, frozen=True, slots=True)
class BehindTheNamesSite:
    base_url: str

    def _names_list_url(self, i: int) -> Name:
        url = self.base_url + "names"
        if i > 0:
            url = url + "/{}".format(i + 1)
        return url

    def scrape_all_names(self):
        for page_index in count():
            _log.info("Scraping page {}".format(page_index))
            results_from_page = 0
            response = get_and_assert_ok(self._names_list_url(page_index))
            for name in scrape_names_results(response.text):
                results_from_page = results_from_page + 1
                yield name

            _log.info("Scraped {} names".format(results_from_page))
            if results_from_page == 0:
                break


def scrape_names_results(text: str) -> Iterable[Name]:
    soup = BeautifulSoup(text, "html.parser", parse_only=SoupStrainer("div", class_="browsename"))
    return map(Name.from_listing, soup)


def scrape():
    names = BehindTheNamesSite(BEHINDTHENAMES_ROOT).scrape_all_names()
    writer = csv.DictWriter(
        sys.stdout, ["text", "description", "usage"], quoting=csv.QUOTE_ALL
    )
    writer.writeheader()
    for name in names:
        writer.writerow(attr.asdict(name))


def main():
    scrape()


if __name__ == "__main__":
    main()

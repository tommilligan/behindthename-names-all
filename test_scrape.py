import unittest

from scrape import (
    Name,
    NameKind,
    scrape,
    scrape_names_results,
    BehindTheNamesSite,
    BASE_URLS,
)


class TestBehindTheNamesSite(unittest.TestCase):
    def test_names_list_url(self):
        site = BehindTheNamesSite("foo/")
        self.assertEqual(site._names_list_url(0), "foo/names")
        self.assertEqual(site._names_list_url(8), "foo/names/9")


class TestScrapeNamesResults(unittest.TestCase):
    def setUp(self):
        self.raw = """<div class="browsename"><span class="listname"><a href="/name/africano">AFRICANO</a></span><span class="info listusage"><a href="/names/usage/italian" class="usg">Italian</a></span><br>From the given name <i>Africano</i>, the Italian form of <a href="//www.behindthename.com/name/africanus" class="nl">AFRICANUS</a>.</div>"""
        self.parsed = Name(
            text="AFRICANO",
            description="From the given name Africano, the Italian form of AFRICANUS.",
            usage="Italian",
        )

    def test_empty(self):
        self.assertEqual(list(scrape_names_results("")), [])

    def test_single(self):
        self.assertEqual(list(scrape_names_results(self.raw)), [self.parsed])

    def test_multiple(self):
        self.assertEqual(
            list(scrape_names_results(self.raw * 3)), [self.parsed] * 3
        )


class TestScrape(unittest.TestCase):
    def test_integration(self):
        self.assertEqual(
            next(
                BehindTheNamesSite(
                    BASE_URLS[NameKind.SURNAME]
                ).scrape_all_names()
            ),
            Name(
                text="AAFJES",
                description='Means "son of AAFJE".',
                usage="Dutch",
            ),
        )


if __name__ == "__main__":
    unittest.main()

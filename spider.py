from bs4 import BeautifulSoup

import scrapy


from open_parliament.parsers import Row, PersonalPage, CommitteesPage


class NationalratsSpider(scrapy.Spider):
    """
    A scraper for MPs of the Austrian Nationalrat_.

    Scrapes biographical data, contact information, party information and committee membership.

    .. seealso:: :mod:`open_parliament.parsers`
    .. _Nationalrat: https://www.parlament.gv.at/WWER/NR/AKT/
    """

    name = "nationalrat"
    BASE = "https://www.parlament.gv.at"
    start_urls = [BASE + "/WWER/NR/AKT/index.shtml"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, features="html.parser")
        next_page = soup.find("div", class_="paginationRechts").a.attrs["href"]
        if next_page is not None:
            yield response.follow(next_page, self.parse_table)

    def parse_table(self, response):
        soup = BeautifulSoup(response.text, features="html.parser")
        table = soup.find(
            "table",
            summary="Liste zeigt die ausgewählten Abgeordnete, die derzeit ein Mandat innehaben",
        )
        rows = table.find_all("tr")
        for row in rows:
            parser = Row(row)
            mp = parser.parse()
            if mp:
                request = scrapy.Request(self.BASE + mp["url"], callback=self.parse_mp)
                request.meta["mp"] = mp
                yield request

    def parse_mp(self, response):
        mp = response.meta["mp"]
        soup = BeautifulSoup(response.text, features="html.parser")
        is_president = soup.find(id="biogr_Einleitung") is not None

        if is_president:
            request = scrapy.Request(
                self.BASE + mp["url"] + "zurPerson.shtml", callback=self.parse_president
            )
            request.meta["mp"] = mp
            yield request
        else:
            mp = self.parse_details(response, False)
            url = self.BASE + mp["url"] + "index.shtml#tab-Ausschuesse"
            request = scrapy.Request(url, callback=self.parse_committees)
            request.meta["mp"] = mp
            yield request

    def parse_president(self, response):
        mp = self.parse_details(response, True)
        url = self.BASE + mp["url"] + "ausschuesse.shtml"

        request = scrapy.Request(url, callback=self.parse_committees)
        request.meta["mp"] = mp
        yield request

    def parse_committees(self, response):
        mp = response.meta["mp"]
        committee_parser = CommitteesPage(response.text)
        mp.update(committee_parser.parse())
        yield mp

    @staticmethod
    def parse_details(response, is_president):
        mp = response.meta["mp"]
        parser = PersonalPage(response.text)
        mp.update(parser.parse(is_president))
        return mp

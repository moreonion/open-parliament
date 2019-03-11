class Row:
    """
    Parses a row from the `MPs table`_ obtaining an MP's general information.

    Calling :func:`parse` will return a dictionary with the following keys:
    - id
    - url (to an MP's personal page)
    - first_name
    - last_name
    - title
    - wahlkreis
    - state
    - political_affiliation

    .. _`MPs table`: https://www.parlament.gv.at/WWER/NR/AKT/
    """

    def __init__(self, row):
        """
        :param row: A :mod:`BeautifulSoup` object containing a single row from the `MPs table`_.
        """
        self.row = row

    def parse(self):
        """
        Parse an MP's general information.

        :returns: A dictionary containing the keys described in :class:`Row`.
        """
        mp = {}
        cells = self.row.find_all("td")

        for cell in cells:
            if "visible-mobile" in cell.attrs["class"]:
                continue
            title = self._get_cell_title(cell)
            content = cell.find("span", class_="table-responsive__inner")

            if title == "name":
                mp.update(self._parse_name(cell, content))
            elif title == "fraktion":
                fraktion, klub = self._parse_abbreviation(
                    content
                )
                mp["political_affiliation"] = klub + " (" + fraktion + ")"
            elif title == "wahlkreis":
                mp["wahlkreis"] = content.text.strip()
            elif title == "bundesland":
                mp["state"] = self._parse_abbreviation(content)[1]

        return mp

    def _get_cell_title(self, cell):
        """Return the title of a cell."""
        return (
            cell.find("span", class_="table-responsive__prefix")
            .text.rstrip(":")
            .strip()
        ).lower()

    def _parse_abbreviation(self, cell_content):
        """
        Parse a cell containing an abbreviation and a full name of something.

        :returns: A tuple containing the abbreviation and the full name.
        """
        span = cell_content.find("span")
        full = span.attrs["title"].strip()
        abbrv = span.text.strip()
        return abbrv, full

    def _parse_name(self, cell, cell_content):
        """
        Parse the cell containing the name of the MP, as well as the link to their personal page.

        :returns: A dictionary with keys :code:`id, url, first_name, last_name, title`.
        """
        mp_page = cell_content.find("a").attrs["href"]

        full_name = cell_content.text.strip()
        name, *title = full_name.split(",")
        last, *first = name.split(" ")

        id_ = mp_page[mp_page.find("PAD_") + 4 : mp_page.rfind("/")]
        url = re.sub("index.shtml$", "", mp_page)

        first_name = " ".join(first).rstrip(",").strip()
        last_name = last.strip()
        title = ",".join(title).strip()

        return {
            "id": id_,
            "url": url,
            "first_name": first_name,
            "last_name": last_name,
            "title": title,
        }

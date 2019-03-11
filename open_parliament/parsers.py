from bs4 import BeautifulSoup

import re


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


class PersonalPage:
    """
    Parses an MP's personal page containing personal, contact and biographical information.

    Calling :func:`parse` will return a dictionary with the following keys:
    - salutation
    - picture
    - address
    - emails
    - phone_numbers
    - websites
    - education
    - work_history
    - mandates
    - posts
    - date_of_birth
    - place_of_birth
    - occupation
    - is_president (set to :code:`False`)
    """

    def __init__(self, html):
        """
        :param html: A text response from an MP's personal page.
        """
        self.page = BeautifulSoup(html, features="html.parser")

    def _get_current_and_former(self, values):
        """
        Takes a list of strings and returns those who are currently active and former ones.

        Currently active values are determined by not containing a "–" in their last word,
        which is used to connect years (e.g. "Teacher 2000–2018").

        :rtype: dict
        :returns: A dictionary containing the corresponding lists indexed by the keys
                  'current' and 'former'.
        """
        stripped = [v.text.strip() for v in values]
        current = []
        former = []

        for s in stripped:
            if "–" not in s.split(" ")[-1]:
                current.append(s)
            else:
                former.append(s)

        return {"current": current, "former": former}

    def parse(self, is_president):
        """
        Parses an MP's personal and contact information and biography.

        :param is_president: Whether the MP is the first president of the Austrian Nationalrat.
        :returns: A dictionary containing the keys described in :class:`PersonalPage`.
        """
        mp = {}
        self.content = self.page.find(id="content")

        salutation = self.content.find(id="inhalt").text.strip()
        if is_president:
            salutation = salutation[: salutation.rfind(" - ")]
        mp["is_president"] = is_president
        mp["salutation"] = salutation
        mp.update(self._parse_picture())
        mp.update(self._parse_contact_information())
        mp.update(self._parse_biography())
        return mp

    def _parse_picture(self):
        """
        Parses an MP's portrait picture.

        :returns: A dictionary with key :code:`picture` indexing a dictionary containing a link to the
        full resolution picture and a link to the thumbnail, with keys :code:`full` and :code:`thumbnail`.
        """
        pic = self.content.find("picture")
        full = pic.find("source").attrs["srcset"]
        thumb = pic.find("img").attrs["src"]
        return {"picture": {"full": full, "thumbnail": thumb}}

    def _parse_contact_information(self):
        """
        Parses an MP's contact information.

        :returns: A dictionary with keys :code:`address, emails, phone_numbers, websites`.
        """
        left_column = self.content.find("div", class_="linkeSpalte40")
        graubox = left_column.find(
            lambda tag: tag.name == "div" and tag["class"] == ["grauBox"]
        )

        emails_raw = graubox.find_all("a", class_="mail")
        websites_raw = graubox.find_all("a", class_="noDecoration")
        telephone_raw = graubox.find_all("span", class_="telefonnummer")
        address_raw = [
            e.nextSibling for e in graubox.find_all("em") if e.text == "Anschrift:"
        ]

        address = address_raw[0].li.get_text("\n")
        emails = [re.sub(r"^mailto:", "", e.attrs["href"]) for e in emails_raw]
        phone_numbers = [t.text for t in telephone_raw]
        websites = [w.attrs["href"] for w in websites_raw]

        return {
            "address": address,
            "emails": emails,
            "phone_numbers": phone_numbers,
            "websites": websites,
        }

    def _parse_biography(self):
        """
        Parses an MP's biographical information.

        :returns: A dictionary consisting of the return values of :func:`_parse_dob_job`,
                  :func:`_parse_political_mandates`, :func:`_parse_political_posts`,
                  :func:`_parse_work_history`, :func:`parse_education`.
        """
        data = {}
        self.right_column = self.content.find("div", class_="rechteSpalte60")
        heading = self.right_column.find("h3")
        # The page of the second president hides the details information
        # and displays a biography instead. By selecting the second div,
        # we get the hidden div containing the MPs details.
        if not heading:
            self.right_column = self.content.find_all("div", class_="rechteSpalte60")[1]
        data.update(self._parse_dob_job())
        data.update(self._parse_political_mandates())
        data.update(self._parse_political_posts())
        data.update(self._parse_work_history())
        data.update(self._parse_education())
        return data

    def _parse_dob_job(self):
        """
        Parses date/place of birth and side-occupation in the right column.

        :returns: A dictionary with keys :code:`date_of_brith, place_of_birth, occupation`.
        """
        # Find date and place of birth and occupation
        dob_job = self.right_column.find("h3", class_="hidden").nextSibling.nextSibling
        dob, job = dob_job.find_all("em")

        # Date/place of birth
        dob = dob.nextSibling.strip()
        try:
            dob, pob = [d.strip() for d in dob.split(",")]
        except ValueError:
            try:
                # https://www.parlament.gv.at/WWER/PAD_88823/
                dob, pob = [d.strip().rstrip(")") for d in dob.split("(")]
            except ValueError:
                # https://www.parlament.gv.at/WWER/PAD_83142/
                dob = dob.strip()
                pob = None

        return {
            "date_of_birth": dob,
            "place_of_birth": pob,
            "occupation": job.nextSibling.strip(),
        }

    def _parse_political_mandates(self):
        """
        Parses the political mandates in the right column.

        :returns: A dictionary with key :code:`mandates`.
        """
        mandates = []
        mandates_raw = self.right_column.find_all("div", class_="aktiv")

        for m in mandates_raw:
            mandate = m.get_text("\n").strip()
            mandate, since = [m.rstrip("–").strip() for m in mandate.split("\n")]
            mandate, *party = [m.strip() for m in mandate.split(",")]
            mandates.append(
                {"title": mandate, "party": party[0] if party else None, "since": since}
            )

        return {"mandates": mandates}

    def _parse_political_posts(self):
        """
        Parses the political posts in the right column.

        :returns: A dictionary with key :code:`posts`.
        """
        functions = [
            h
            for h in self.right_column.find_all("h4")
            if h.text == "Politische Funktionen"
        ]
        if functions:
            functions = functions[0].nextSibling.nextSibling.find_all("li")
            # TODO: Can we do better than just taking the whole string?
            return {"posts": self._get_current_and_former(functions)}
        return {}

    def _parse_work_history(self):
        """
        Parses the work history in the right column.

        :returns: A dictionary with :code:`work_history`.
        """
        work_history = [
            h
            for h in self.right_column.find_all("h4")
            if h.text == "Beruflicher Werdegang"
        ]
        if work_history:
            work_history = work_history[0].nextSibling.nextSibling.find_all("li")
            # TODO: Can we do better than just taking the whole string?
            return {"work_history": self._get_current_and_former(work_history)}
        return {}

    def _parse_education(self):
        """
        Parses the educational history in the right column.

        :returns: A dictionary with :code:`education`.
        """
        education = [
            h for h in self.right_column.find_all("h4") if h.text == "Bildungsweg"
        ]
        if education:
            education = education[0].nextSibling.nextSibling.find_all("li")
            return {"education": [e.text.strip() for e in education]}
        return {}

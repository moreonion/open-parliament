import contextlib
from unittest.mock import Mock, patch

import requests
from bs4 import BeautifulSoup

import pytest
from open_parliament import parsers


def mock_response_from_file(path):
    """Create a mock response from a JSON file."""
    with open(path, "rb") as f:
        data = f.read()

    return Mock(spec=requests.Response, content=data, status_code=200)


@pytest.fixture(scope="session")
def request_response_from_files():
    """Provide a contextmananger to patch requests.get with JSON response files."""

    def _build_response_map(file_map):
        response_map = {}
        for p, path in file_map.items():
            for p_ in path:
                response_map.setdefault(p, []).append(mock_response_from_file(p_))

        return response_map

    @contextlib.contextmanager
    def request_response_from_files_cm(prefix, file_map):
        """Mock request.get and give answers according to paths."""
        response_map = _build_response_map(file_map)

        def mock_get(url):
            if url.startswith(prefix):
                path = url[len(prefix) :]
                return response_map[path].pop(0)

        with patch("requests.get", new=mock_get):
            yield response_map

    return request_response_from_files_cm


BASE = "https://www.parlament.gv.at"
AKTUELL = BASE + "/WWER/NR/AKT/index.shtml"


def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, features="html.parser")


def get_mp_table():
    soup = BeautifulSoup(fetch_page(AKTUELL), features="html.parser")
    if soup:
        show_all = soup.find("div", class_="paginationRechts").a.attrs["href"]
        html = BeautifulSoup(fetch_page(BASE + show_all), features="html.parser")
        return html.find(
            "table",
            summary="Liste zeigt die ausgewählten Abgeordnete, die derzeit ein Mandat innehaben",
        )


@pytest.fixture(scope="function")
def mps_base(request_response_from_files, shared_datadir):
    """Provide basic information about all MPs."""
    file_map = {
        "": [shared_datadir / "nationalrat_aktuell.html"],
        (
            "?xdocumentUri=%2FWWER%2FNR%2FAKT%2Findex.shtml&pageNumber=&GP=AKT&STEP=1110&"
            "BL=ALLE&feldRnr=1&FR=ALLE&FUNK=ALLE&M=M&ascDesc=ASC&NRBR=NR&FBEZ=FW_002&WK=ALLE&"
            "requestId=6DFF285AA9&LISTE=&jsMode=&R_PBW=PLZ&W=W&WP=ALLE&listeId=2&R_WF=FR&PLZ="
        ): [shared_datadir / "nationalrat_aktuell_full.html"],
    }
    mps = {}

    with request_response_from_files(AKTUELL, file_map):
        table = get_mp_table()
        for row in table.find_all("tr"):
            row_parser = parsers.Row(row)
            mp = row_parser.parse()
            if mp:
                mps[mp["id"]] = mp

    return mps

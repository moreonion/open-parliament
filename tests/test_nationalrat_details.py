"""Tests for scraping the pages of single MPs."""
from open_parliament.parsers import PersonalPage


def test_president_details(parse_page):
    mp = parse_page(
        "/WWER/PAD_88386/zurPerson.shtml",
        "nationalrat_sobotka_zur_person.html",
        PersonalPage,
        is_president=True,
    )

    # Using a compare function allows for easier debugging
    def compare(a, b):
        for k in a:
            assert a[k] == b[k]

    details = {
        "salutation": "Mag. Wolfgang Sobotka",
        "date_of_birth": "05.01.1956",
        "place_of_birth": "Waidhofen an der Ybbs",
        "occupation": "Präsident des Nationalrates",
        "emails": ["wolfgang.sobotka@parlament.gv.at"],
        "address": "Parlament\nDr. Karl Renner-Ring 3\n1017 Wien",
    }
    compare(details, mp)

    political_mandates = {
        "mandates": [
            {
                "title": "Abgeordneter zum Nationalrat (XXVI. GP)",
                "party": "ÖVP",
                "since": "09.11.2017",
            },
            {
                "title": "Präsident des Nationalrates",
                "party": None,
                "since": "20.12.2017",
            },
        ]
    }
    compare(political_mandates, mp)

    posts = {
        "posts": {
            "current": [
                (
                    "Landesobmann des Österreichischen Arbeitnehmerinnen- und Arbeitnehmerbundes (ÖAAB)"
                    " Niederösterreich seit 2010"
                )
            ],
            "former": [
                "Bundesminister für Inneres Österreich 2016–2017",
                "Landeshauptmann-Stellvertreter von Niederösterreich 2009–2016",
                (
                    "Mitglied der Landesregierung von Niederösterreich (Landesrat für Finanzen, Wohnbau "
                    "und Gemeinden) 2008–2016"
                ),
                (
                    "Mitglied der Landesregierung von Niederösterreich (Landesrat für Finanzen, Wohnbau "
                    "und Lebensqualität) 2005–2008"
                ),
                (
                    "Mitglied der Landesregierung von Niederösterreich (Landesrat für Finanzen, Umwelt "
                    "und Raumordnung) 1998–2005"
                ),
                "Bürgermeister der Statutarstadt Waidhofen an der Ybbs 1996–1998",
                "Stadtrat für Finanzen der Statutarstadt Waidhofen an der Ybbs 1992–1996",
                "Mitglied des Gemeinderates der Statutarstadt Waidhofen an der Ybbs 1982–1992",
                "Fraktionsobmann der ÖVP Waidhofen an der Ybbs 1992–1996",
                "Betriebsgruppenobmann des ÖAAB der Statutarstadt Waidhofen an der Ybbs 1985–1993",
            ],
        }
    }
    compare(posts, mp)

    work_history = {
        "work_history": {
            "current": [],
            "former": [
                "Referent für Politik und Bildung der ÖVP Niederösterreich 1992–1996",
                "Musikschulleiter der Statutarstadt Waidhofen an der Ybbs 1988–1998",
                "Lehrbeauftragter an der Hochschule für Musik und darstellende Kunst in Wien 1987–1998",
                "Stadtarchivar der Statutarstadt Waidhofen an der Ybbs 1980–1987",
                (
                    "Lehrer an einer Allgemeinbildenden Höheren Schule (AHS) der Statutarstadt "
                    "Waidhofen an der Ybbs 1976–1992 sowie 1996–1998"
                ),
                "Musikschullehrer der Statutarstadt Waidhofen an der Ybbs 1972–1998",
            ],
        }
    }
    compare(work_history, mp)

    education = {
        "education": [
            "Studium an der Hochschule für Musik und darstellende Kunst in Wien (Violoncello und Musikpädagogik)",
            "Studium am Brucknerkonservatorium in Linz (Dirigieren)",
            "Studium der Geschichte an der Universität Wien (Mag. phil.)",
        ]
    }
    compare(education, mp)

    picture = {
        "picture": {
            "full": "/WWER/PAD_88386/7256051_180.jpg",
            "thumbnail": "/WWER/PAD_88386/7256051_500.jpg",
        }
    }
    compare(picture, mp)


def test_2nd_3rd_president_details(parse_page):
    """Test whether the 2nd and 3rd Nationalrat's president is scraped correctly."""
    bures = parse_page(
        "/WWER/PAD_00145/", "nationalrat_bures.html", PersonalPage, is_president=False
    )
    kitzmueller = parse_page(
        "/WWER/PAD_51565/",
        "nationalrat_kitzmueller.html",
        PersonalPage,
        is_president=False,
    )

    assert "salutation" in bures
    assert "emails" in bures
    assert "mandates" in bures
    assert "posts" in bures
    assert "work_history" in bures
    assert "education" in bures
    # We're only interested in the *first* president here, since their details page differs from all others
    assert bures["is_president"] is False

    assert "salutation" in kitzmueller
    assert "emails" in kitzmueller
    assert "mandates" in kitzmueller
    assert "posts" in kitzmueller
    assert "work_history" in kitzmueller
    assert "education" in kitzmueller
    assert kitzmueller["is_president"] is False


def test_hannes_mp(parse_page):
    """Test whether the MP Hannes is scraped correctly."""
    mp = parse_page(
        "/WWER/PAD_51879/", "nationalrat_hannes.html", PersonalPage, is_president=False
    )

    hannes = {
        "is_president": False,
        "salutation": "Hannes Amesbauer, BA",
        "emails": ["hannes.amesbauer@parlament.gv.at", "hannes.amesbauer@fpoe.at"],
        "address": "Freiheitlicher Parlamentsklub\nDr. Karl Renner-Ring 3\n1017 Wien",
        "websites": [],
        "phone_numbers": [],
        "date_of_birth": "18.04.1981",
        "place_of_birth": "Bruck an der Mur (Steiermark)",
        "occupation": "Vertragsbediensteter",
        "mandates": [
            {
                "title": "Abgeordneter zum Nationalrat (XXVI. GP)",
                "party": "FPÖ",
                "since": "09.11.2017",
            }
        ],
        "posts": {
            "former": [
                "Abgeordneter zum  Steiermärkischen Landtag 2010–2017",
                "Mitglied des Gemeinderates der Marktgemeinde Neuberg an der Mürz 2010–2015",
                "Bundesgeschäftsführer Ring Freiheitlicher Studenten (RFS) 2006–2009",
            ],
            "current": [
                "Vizebürgermeister der Marktgemeinde Neuberg an der Mürz seit 2015",
                "Mitglied des Bundesparteivorstandes der FPÖ  seit 2017",
                "Landesparteiobmann-Stellvertreter der FPÖ Steiermark seit 2016",
                "Bezirksparteiobmann der FPÖ Bruck-Mürzzuschlag seit 2009",
                "Ortsparteiobmann der FPÖ Neuberg an der Mürz seit 2005",
                "Bundesobmann-Stellvertreter des Ringes Freiheitlicher Jugend (RFJ)",
                "Landesobmann des Ringes Freiheitlicher Jugend (RFJ) Steiermark",
            ],
        },
        "work_history": {
            "current": ["Vertragsbediensteter, Land Steiermark  seit 2011"],
            "former": [],
        },
        "education": [
            "Universität Wien, Politikwissenschaft (BA, 2011) Wien",
            "Präsenzdienst",
            "Berufsreifeprüfung Wien",
            "Landesberufsschule für Steinmetze (erlernter Beruf: Steinmetz) Graz",
            "Polytechnische Schule Mürzzuschlag",
            "Hauptschule Neuberg an der Mürz",
            "Volksschule Neuberg an der Mürz",
        ],
        "picture": {
            "full": "/WWER/PAD_51879/7182826_180.jpg",
            "thumbnail": "/WWER/PAD_51879/7182826_500.jpg",
        },
    }
    assert sorted(hannes.pop("emails")) == sorted(mp.pop("emails"))
    assert sorted(hannes.pop("posts")) == sorted(mp.pop("posts"))
    assert hannes == mp


def test_ruth_mp(parse_page):
    """Test whether the MP Ruth is scraped correctly."""
    mp = parse_page(
        "/WWER/PAD_14836/", "nationalrat_ruth.html", PersonalPage, is_president=False
    )

    assert ["+43 1 401 10-3734"] == mp["phone_numbers"]
    assert mp["websites"] == []


def test_belakowitsch_mp(parse_page):
    """Test whether the MP Belakowitsch is scraped correctly."""
    mp = parse_page(
        "/WWER/PAD_35468/",
        "nationalrat_belakowitsch.html",
        PersonalPage,
        is_president=False,
    )

    assert mp["websites"] == ["http://www.fpoe-parlamentsklub.at/"]


def test_deimek_mp(parse_page):
    """Test whether the MP Deimek is scraped correctly."""
    mp = parse_page(
        "/WWER/PAD_51557/", "nationalrat_deimek.html", PersonalPage, is_president=False
    )

    work_history = {
        "current": ["Großprojektmanager, Siemens  seit 2004"],
        "former": [
            "Berechnungsingenieur, VAI 1990–1992",
            "Projektant, VAI 1992–1994",
            "Produktmanager Reduktionstechnik, VAI 1995–1999",
            "Vertriebsleiter Automation, VAI 2000–2004",
        ],
    }
    assert work_history == mp["work_history"]


def test_missing_comma(parse_page):
    """Test if the one MP missing a comma before his place of birth is parsed correctly."""
    mp = parse_page(
        "/WWER/PAD_88823",
        "nationalrat_no_comma_dob_pob.html",
        PersonalPage,
        is_president=False,
    )

    assert mp["date_of_birth"] == "05.10.1952"
    assert mp["place_of_birth"] == "Wien"


def test_lintl(parse_page):
    """
    Test if MP Lintl is parsed correctly.

    MP Lintl is missing a place of birth and has listed multiple websites.
    """
    mp = parse_page(
        "/WWER/PAD_83142", "nationalrat_lintl.html", PersonalPage, is_president=False
    )

    assert mp["date_of_birth"] == "30.06.1956"
    assert mp["place_of_birth"] is None

    assert mp["websites"] == [
        "http://www.jessi-lintl.at",
        "http://twitter.com/jessilintl",
        "https://www.flickr.com/people/131627891@N03/",
    ]


def test_multiple_phone_numbers(parse_page):
    """Test if multiple phone numbers are parsed correctly."""
    mp = parse_page(
        "/WWER/PAD_55227/", "nationalrat_hammer.html", PersonalPage, is_president=False
    )
    assert mp["phone_numbers"] == ["+43 664 829 80 88", "+43 732 77 20-16238"]


def test_baumgartner(parse_page):
    mp = parse_page(
        "/WWER/PAD_01974/",
        "nationalrat_baumgartner.html",
        PersonalPage,
        is_president=False,
    )
    assert mp["emails"][0] == "angela.baumgartner@parlament.gv.at"

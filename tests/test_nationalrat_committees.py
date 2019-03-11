"""Tests for scraping the committee page of single MPs."""
from open_parliament.parsers import CommitteesPage

base = "/PAKT/VHG/XXVI"


def test_president_committees(parse_page):
    """Test whether the Nationalrat president's committees are scraped correctly."""
    president = parse_page(
        "/WWER/PAD_88386/ausschuesse.shtml",
        "nationalrat_sobotka_ausschuesse.html",
        CommitteesPage,
    )
    committees = {
        "Mitglied": {
            "SA-HA_00001_00830": {
                "url": base + "/SA-HA/SA-HA_00001_00830/index.shtml",
                "since": "21.12.2017",
                "name": "Ständiger Unterausschuss des Hauptausschusses",
            },
            "A-GO_00001_00838": {
                "url": base + "/A-GO/A-GO_00001_00838/index.shtml",
                "since": "26.09.2018",
                "name": "Geschäftsordnungsausschuss",
            },
            "A-HA_00001_00823": {
                "url": base + "/A-HA/A-HA_00001_00823/index.shtml",
                "since": "26.09.2018",
                "name": "Hauptausschuss",
            },
        },
        "Ersatzmitglied": {},
    }
    assert committees["Mitglied"] == president["committees"]["Mitglied"]
    assert "Ersatzmitglied" not in president["committees"]


def test_hannes_committees(parse_page):
    """Test whether MP Hannes committees are scraped correctly."""
    hannes = parse_page(
        "/WWER/PAD_51879/index.shtml#tab-Ausschuesse",
        "nationalrat_hannes_committees.html",
        CommitteesPage,
    )
    date = "26.09.2018"

    committees = {
        "Mitglied": {
            "A-AS_00001_00834": {
                "url": base + "/A-AS/A-AS_00001_00834/index.shtml",
                "since": date,
                "name": "Ausschuss für Arbeit und Soziales",
            },
            "A-KO_00001_00842": {
                "url": base + "/A-KO/A-KO_00001_00842/index.shtml",
                "since": date,
                "name": "Ausschuss für Konsumentenschutz",
            },
            "A-ME_00001_00847": {
                "url": base + "/A-ME/A-ME_00001_00847/index.shtml",
                "since": date,
                "name": "Ausschuss für Menschenrechte",
            },
            "A-RH_00001_00849": {
                "url": base + "/A-RH/A-RH_00001_00849/index.shtml",
                "since": date,
                "name": "Rechnungshofausschuss",
            },
            "A-SP_00001_00851": {
                "url": base + "/A-SP/A-SP_00001_00851/index.shtml",
                "since": date,
                "name": "Sportausschuss",
            },
            "A-VE_00001_00855": {
                "url": base + "/A-VE/A-VE_00001_00855/index.shtml",
                "since": date,
                "name": "Verkehrsausschuss",
            },
        },
        "Ersatzmitglied": {
            "A-TO_00001_00852": {
                "url": base + "/A-TO/A-TO_00001_00852/index.shtml",
                "since": date,
                "name": "Tourismusausschuss",
            },
            "A-UN_00001_00854": {
                "url": base + "/A-UN/A-UN_00001_00854/index.shtml",
                "since": date,
                "name": "Unterrichtsausschuss",
            },
            "A-WI_00001_00857": {
                "url": base + "/A-WI/A-WI_00001_00857/index.shtml",
                "since": date,
                "name": "Wissenschaftsausschuss",
            },
        },
    }

    assert hannes["committees"] == committees


def test_belakowitsch_committees(parse_page):
    """Test whether MP Hannes committees are scraped correctly."""
    belakowitsch = parse_page(
        "/WWER/PAD_35468/index.shtml#tab-Ausschuesse",
        "nationalrat_belakowitsch_committees.html",
        CommitteesPage,
    )

    committees = {
        "Vorsitzender-Stellvertreterin": {
            "A-USA_00002_00862": {
                "url": base + "/A-USA/A-USA_00002_00862/index.shtml",
                "since": "19.04.2018",
                "name": (
                    "Untersuchungsausschuss: Untersuchungsausschuss über das "
                    'Kampfflugzeugsystem "Eurofighter Typhoon"'
                ),
            }
        },
        "Vorsitzende-Stellvertreterin": {
            "A-USA_00003_00862": {
                "url": base + "/A-USA/A-USA_00003_00862/index.shtml",
                "since": "20.04.2018",
                "name": "Untersuchungsausschuss: BVT-Untersuchungsausschuss",
            }
        },
        "Obmannstellvertreterin": {
            "A-AS_00001_00834": {
                "url": base + "/A-AS/A-AS_00001_00834/index.shtml",
                "since": "26.09.2018",
                "name": "Ausschuss für Arbeit und Soziales",
            }
        },
    }

    belakowitsch["committees"].pop("Mitglied")
    belakowitsch["committees"].pop("Ersatzmitglied")
    assert belakowitsch["committees"] == committees

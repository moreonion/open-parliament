def test_mps(mps_base):
    """Test whether the MPs are scraped correctly."""
    hannes = {
        "id": "51879",
        "first_name": "Hannes",
        "last_name": "Amesbauer",
        "title": "BA",
        "url": "/WWER/PAD_51879/",
        "political_affiliation": "Freiheitlicher Parlamentsklub (FPÖ)",
        "wahlkreis": "6D Obersteiermark",
        "state": "Steiermark",
    }
    assert hannes == mps_base[hannes["id"]]


def test_name_parsing(mps_base):
    """Test whether MP's names are parsed correctly."""
    martha = mps_base["02349"]
    assert martha["first_name"] == "Martha"
    assert martha["last_name"] == "Bißmann"
    assert martha["title"] == "Dipl.-Ing. (FH)"

    elisabeth = mps_base["02189"]
    assert elisabeth["first_name"] == "Elisabeth"
    assert elisabeth["last_name"] == "Feichtinger"
    assert elisabeth["title"] == "BEd BEd"

    gudenus = mps_base["18665"]
    assert gudenus["first_name"] == "Johann"
    assert gudenus["last_name"] == "Gudenus"
    assert gudenus["title"] == "Mag., M.A.I.S."

    klaus = mps_base["83298"]
    assert klaus["first_name"] == "Klaus Uwe"
    assert klaus["last_name"] == "Feichtinger"
    assert klaus["title"] == "Mag. Dr."

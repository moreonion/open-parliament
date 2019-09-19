"""Convert JSON to CSV for open_parliament_at source."""

import csv
import json
import logging
import os
import re
import subprocess

import click


logger = logging.getLogger(__name__)

WANTED_FIELDS = [
    "first_name",
    "last_name",
    "salutation",
    "title",
    "political_affiliation",
    "state",
    "occupation",
    "place_of_birth",
    "date_of_birth",
]

party_extract_re = re.compile(r"^.* \((?P<party>\w+)\)$")


@click.group()
def cli():
    """CLI group."""


@cli.command()
@click.argument("output", default="-")
def scrape(output):
    """Command to scrape parlament.gv.at."""
    proc = subprocess.run(
        [
            "scrapy",
            "runspider",
            os.path.join(os.path.dirname(__file__), "spider.py"),
            "-o",
            output,
            "--loglevel=INFO",
        ]
    )
    return proc.returncode == 0


@cli.command()
@click.argument("jsonfile", type=click.File("rb"), default="-")
@click.argument("output", type=click.File("w"), default="-")
def convert_to_csv(jsonfile, output):
    """Command to convert JSON to CSV."""
    scraped = json.load(jsonfile)

    sorted_input = sorted(scraped, key=lambda x: int(x["id"]))

    contacts = []
    for mp_data in sorted_input:
        mp = {"identifier": mp_data["id"]}
        emails = mp_data.pop("emails")
        if len(emails) > 0:
            mp["email"] = emails[0]
        else:
            mp["email"] = ""
            logger.warning(
                "Contact without email: %s (%s %s)",
                mp_data["id"],
                mp_data["first_name"],
                mp_data["last_name"],
            )
        mp.update({k: mp_data[k] for k in WANTED_FIELDS})
        if "committees" in mp_data:
            committees = sorted(
                [c["name"] for f in mp_data["committees"].values() for c in f.values()]
            )
            mp["committees"] = "," + ",".join(committees) + ","
        else:
            mp["committees"] = ""
        mandates = [m["title"] for m in mp_data["mandates"]]
        mp["mandates"] = "," + ",".join(mandates) + ","
        # extract party from political_affiliation field
        party = party_extract_re.match(mp_data["political_affiliation"])
        if party and party.group("party"):
            mp["party"] = party.group("party")
        else:
            mp["party"] = ""
            logger.warning(
                "Contact without party: %s (%s %s)",
                mp_data["id"],
                mp_data["first_name"],
                mp_data["last_name"],
            )
        contacts.append(mp)

        display_title = ""
        if mp_data["title"]:
            display_title = ", " + mp_data["title"]
        display_party = ""
        if mp["party"]:
            display_party = " (" + mp["party"] + ")"
        mp["display_name"] = "{} {}{}{}".format(
            mp_data["last_name"], mp_data["first_name"], display_title, display_party
        )

    output_mapping = [
        "identifier",
        "first_name",
        "last_name",
        "email",
        "salutation",
        "display_name",
        "title",
        "party",
        "political_affiliation",
        "state",
        "occupation",
        "place_of_birth",
        "date_of_birth",
        "mandates",
        "committees",
    ]
    csvwriter = csv.DictWriter(output, fieldnames=output_mapping, extrasaction="ignore")
    csvwriter.writeheader()
    for item in contacts:
        csvwriter.writerow(item)


if __name__ == "__main__":
    cli()

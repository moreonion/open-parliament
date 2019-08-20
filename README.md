# Open Parliament

A scraper for https://parlament.gv.at

To scrape the data of all MPs of the Austrian Nationalrat run `scrapy runspider spider.py -o mps.json` in the top directory.

Install the scrapy with `pip install -e .`.

You can scape and convert the result to a CSV with `scrapy runspider -t json -o - spider.py | open-parliament convert-to-csv > nationalrat.csv 2> nationalrat.log`.

## Issues

Running `open-parliament scrape` in a pipe with `open-parliament convert-to-csv` has issues.

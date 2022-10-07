import datetime
import json
import re
from pathlib import Path

import pandas as pd
import requests
import slugify.slugify


def match_and_map(txt):
    try:
        return json.loads(txt)
    except:
        return None


def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'referer': 'https://www.google.com/',
        'accept-language': 'en-IN,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ml;q=0.6,hi;q=0.5',
    }
    regex = r"""^location_data\.push\((.*)\)\;$"""
    with requests.get('https://thehumanbean.com/find/', headers=headers) as r:
        response_html = r.text.replace("\t", '').replace("\n", '').replace('location_data.push',
                                                                           '\n\nlocation_data.push').replace(
            "'", '"').replace(",}", '}')
        matches = re.findall(regex, response_html, re.VERBOSE | re.IGNORECASE | re.MULTILINE)
        return [match_and_map(x) for x in matches]


if __name__ == '__main__':
    base_folder = 'Datasets'
    scrape_datetime = datetime.datetime.now()
    scrape_domain = 'thehumanbean.com'
    scrape_store_name = 'The Human Bean'
    scrape_file_folder = f'{base_folder}/{slugify.slugify(scrape_store_name)}/{scrape_datetime.strftime("%m-%Y")}/'
    scrape_file_name = scrape_file_folder + f'{slugify.slugify(scrape_store_name)}_{scrape_datetime.strftime("%m_%d_%Y_%H_%M_%S")}.json'
    Path(scrape_file_folder).mkdir(parents=True, exist_ok=True)

    results = main()

    df = pd.DataFrame(results)
    df['scrape_datetime'] = scrape_datetime
    df['scrape_domain'] = scrape_domain
    df['scrape_store_name'] = scrape_store_name

    df.to_json(scrape_file_name, orient='records')

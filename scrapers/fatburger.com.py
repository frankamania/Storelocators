import datetime
import json
import re
from pathlib import Path

import pandas as pd
import requests
import slugify.slugify


def scrape_recursive(_session,_header,_page):
    params = {
        'auth_token': 'BBOAPSVZOXCPKFUV',
        'center': '',
        'coordinates': '',
        'multi_account': 'true',
        'page': f'{_page}',
        'pageSize': '100',
    }
    response = _session.get('https://api.momentfeed.com/v1/analytics/api/llp.json', params=params, headers=_header).json()
    for item in response:
        yield item
    if len(response)==100:
        yield from scrape_recursive(_session,_header,_page+1)




def main():
    headers = {
        'Host': 'api.momentfeed.com',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://locations.fatburger.com',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://locations.fatburger.com/',
        'accept-language': 'en-IN,en;q=0.9',
    }
    session = requests.session()
    return [x for x in scrape_recursive(session,headers,1)]


if __name__ == '__main__':
    base_folder = 'Datasets'
    scrape_datetime = datetime.datetime.now()
    scrape_domain = 'fatburger.com'
    scrape_store_name = 'Fatburger'
    scrape_file_folder = f'{base_folder}/{slugify.slugify(scrape_store_name)}/{scrape_datetime.strftime("%m-%Y")}/'
    scrape_file_name = scrape_file_folder + f'{slugify.slugify(scrape_store_name)}_{scrape_datetime.strftime("%m_%d_%Y_%H_%M_%S")}.json'
    Path(scrape_file_folder).mkdir(parents=True, exist_ok=True)

    results = main()

    df = pd.DataFrame(results)
    df['scrape_datetime'] = scrape_datetime
    df['scrape_domain'] = scrape_domain
    df['scrape_store_name'] = scrape_store_name

    df.to_json(scrape_file_name, orient='records')

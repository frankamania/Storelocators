import datetime
import json
import re
from pathlib import Path

import pandas as pd
import requests
import slugify.slugify


class BaseScraper:

    def __init__(self,
                 base_folder_path='Datasets',
                 scrape_domain='fatburger.com',
                 scrape_store_name='Fatburger',
                 extra_data=None
                 ):
        if extra_data is None:
            extra_data = {}

        self.base_folder = base_folder_path
        self.scrape_datetime = datetime.datetime.now()
        self.scrape_domain = scrape_domain
        self.scrape_store_name = scrape_store_name
        self.extra_data = extra_data

        self.scrape_file_folder = f'{self.base_folder}/{slugify.slugify(scrape_store_name)}/{self.scrape_datetime.strftime("%m-%Y")}/'
        self.scrape_file_name = self.scrape_file_folder + f'{slugify.slugify(scrape_store_name)}_{self.scrape_datetime.strftime("%m_%d_%Y_%H_%M_%S")}.json'
        Path(self.scrape_file_folder).mkdir(parents=True, exist_ok=True)

        self.rows = []



    def standerdize_item(self,_itm):

        Name = _itm.get("store_info", {}).get("name", None)

        yield dict(Name=Name)


    def scrape_data(self):
        yield {}

    def run_scraper(self):
        for itmm in self.scrape_data():
            for _std_itm in self.standerdize_item(itmm):
                self.rows.append(_std_itm)

    def export_file(self):
        df = pd.DataFrame(self.rows)
        df['scrape_datetime'] = self.scrape_datetime
        df['scrape_domain'] = self.scrape_domain
        df['scrape_store_name'] = self.scrape_store_name
        # df['extra_data_dict'] = self.extra_data
        df.to_json(self.scrape_file_name, orient='records')

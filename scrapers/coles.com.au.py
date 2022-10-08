import json

import requests

from scrapers.BaseScraper import BaseScraper


class scraper(BaseScraper):

    def __init__(self):
        super().__init__(
            scrape_domain='coles.com.au',
            scrape_store_name='coles',
        )



    def scrape_data(self):
        session = requests.session()
        headers = {
            'Host': 'apigw.coles.com.au',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://www.coles.com.au',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.coles.com.au/',
            'accept-language': 'en-IN,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ml;q=0.6,hi;q=0.5',
        }

        au_locations = json.loads(open('constants/au.json','r',encoding='utf-8-sig').read())
        for au_location_item in au_locations:
            try:
                response = session.get('https://apigw.coles.com.au/digital/colesweb/v1/stores/search', params={
                    'latitude': au_location_item["lat"],
                    'longitude': au_location_item["lng"],
                    'brandIds': '2,1',
                    'numberOfStores': '15',
                }, headers=headers).json()

                for store in response['stores']:
                    yield store

            except:
                pass




    def standerdize_item(self,_itm):

        Name = _itm.get("storeName", None)
        Status = _itm.get("status", None)
        Address = _itm.get("address", None)
        State = _itm.get("state", None)
        Locality = _itm.get("suburb", None)
        Zip = _itm.get("postcode", None)
        Country = _itm.get("country", None)
        PhoneNumbers = [_itm.get("phone", None)]
        Website = _itm.get("website", None)
        Latitude = _itm.get("latitude", None)
        Longitude = _itm.get("longitude", None)
        Emails = None
        Brand = _itm.get("brandName", None)

        yield dict(Name=Name, Brand=Brand, Status=Status, Address=Address, State=State, Locality=Locality, Zip=Zip,
                   Country=Country,
                   PhoneNumbers=PhoneNumbers, Website=Website, Emails=Emails, Latitude=Latitude, Longitude=Longitude)

if __name__ == '__main__':
    s = scraper()
    s.run_scraper()
    s.export_file()

import requests

from scrapers.BaseScraper import BaseScraper


class scraper(BaseScraper):

    def __init__(self):
        super().__init__(
            scrape_domain='fatburger.com',
            scrape_store_name='Fatburger',
        )

    def scrape_recursive(self,_session, _header, _page):
        params = {
            'auth_token': 'BBOAPSVZOXCPKFUV',
            'center': '',
            'coordinates': '',
            'multi_account': 'true',
            'page': f'{_page}',
            'pageSize': '100',
        }
        response = _session.get('https://api.momentfeed.com/v1/analytics/api/llp.json', params=params,
                                headers=_header).json()
        for item in response:
            yield item
        if len(response) == 100:
            yield from self.scrape_recursive(_session, _header, _page + 1)

    def scrape_data(self):
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

        yield from self.scrape_recursive(session, headers, 1)


    def standerdize_item(self,_itm):

        Name = _itm.get("store_info", {}).get("name", None)
        Status = _itm.get("store_info", {}).get("status", None)
        Address = _itm.get("store_info", {}).get("address", None)
        State = _itm.get("store_info", {}).get("region", None)
        Locality = _itm.get("store_info", {}).get("region", None)
        Zip = _itm.get("store_info", {}).get("postcode", None)
        Country = _itm.get("store_info", {}).get("country", None)
        PhoneNumbers = [_itm.get("store_info", {}).get("phone", None)]
        Website = _itm.get("store_info", {}).get("website", None)
        Latitude = _itm.get("store_info", {}).get("latitude", None)
        Longitude = _itm.get("store_info", {}).get("longitude", None)
        Emails = None
        Brand = self.scrape_store_name

        yield dict(Name=Name,Brand = Brand, Status=Status, Address=Address, State=State,Locality =Locality, Zip=Zip, Country=Country,
                   PhoneNumbers=PhoneNumbers, Website=Website, Emails=Emails, Latitude=Latitude, Longitude=Longitude)

if __name__ == '__main__':
    s = scraper()
    s.run_scraper()
    s.export_file()

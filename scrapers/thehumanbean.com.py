import json
import re

import requests

from scrapers.BaseScraper import BaseScraper
import bs4


class scraper(BaseScraper):

    def __init__(self):
        super().__init__(
            scrape_domain='thehumanbean.com',
            scrape_store_name='The Human Bean',
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

        def match_and_map(txt):
            try:
                return json.loads(txt)
            except:
                return None

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
            for x in matches:
                y = match_and_map(x)
                if y is not None:
                    yield y


    def standerdize_item(self,_itm):

        Name = _itm.get("name", None)
        Status = _itm.get("status", None)
        Country = _itm.get("country", None)
        PhoneNumbers = [_itm.get("phone", None),_itm.get("phone_2nd", None)]
        Website = _itm.get("self_url", None)
        Latitude = _itm.get("lat", None)
        Longitude = _itm.get("long", None)
        Emails = [_itm.get("email",None)]
        State = str(Name)[0:2]
        Locality = _itm.get("region", None)
        Zip = _itm.get("postcode", None)

        Address = _itm.get("address", None)
        if Address is not None:

            soup = bs4.BeautifulSoup(Address, "lxml")
            Address = soup.find('div',{"class":'street-address'}).text
            Zip = soup.find('span',{"class":'postal-code'}).text

        Brand = self.scrape_store_name

        yield dict(Name=Name, Brand=Brand, Status=Status, Address=Address, State=State, Locality=Locality, Zip=Zip,
                   Country=Country,
                   PhoneNumbers=PhoneNumbers, Website=Website, Emails=Emails, Latitude=Latitude, Longitude=Longitude)

if __name__ == '__main__':
    s = scraper()
    s.run_scraper()
    s.export_file()


import cloudscraper
from scrapers.BaseScraper import BaseScraper


class scraper(BaseScraper):

    def __init__(self):
        super().__init__(
            scrape_domain='au.gingerpeople.com',
            scrape_store_name='gingerpeople',
        )



    def scrape_data(self):


        session = cloudscraper.create_scraper()  # returns a CloudScraper instance

        response = session.get('https://au.gingerpeople.com/wp-admin/admin-ajax.php', params={
            'action': 'asl_load_stores',
            'nonce': 'e97446b1c2',
            'lang': '',
            'load_all': '1',
            'layout': '1',
        })

        for itm in response.json():
            yield itm

    def standerdize_item(self,_itm):

        Name = _itm.get("title", None)
        Status = _itm.get("status", None)
        Country = 'au'
        PhoneNumbers = [_itm.get("phone", None)]
        Website = _itm.get("website", None)
        Latitude = _itm.get("lat", None)
        Longitude = _itm.get("lng", None)
        Emails = [_itm.get("email",None)]
        State = _itm.get("state", None)
        Locality = _itm.get("city", None)
        Zip = _itm.get("postal_code", None)
        Address = _itm.get("street", None)


        Brand = self.scrape_store_name

        yield dict(Name=Name, Brand=Brand, Status=Status, Address=Address, State=State, Locality=Locality, Zip=Zip,
                   Country=Country,
                   PhoneNumbers=PhoneNumbers, Website=Website, Emails=Emails, Latitude=Latitude, Longitude=Longitude)

if __name__ == '__main__':
    s = scraper()
    s.run_scraper()
    s.export_file()


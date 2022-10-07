import asyncio
import datetime
import json
import time
from time import perf_counter
import aiohttp
import re
import pandas
import pandas as pd
import slugify.slugify

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'referer': 'https://www.google.com/',
    'accept-language': 'en-IN,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ml;q=0.6,hi;q=0.5',
}


async def match_and_map(txt):
    try:
        return json.loads(txt)
    except:
        return None


async def main():
    regex = r"""^location_data\.push\((.*)\)\;$"""
    async with aiohttp.ClientSession() as session:
        async with session.get('https://thehumanbean.com/find/', headers=headers) as r:
            if r.status != 200:
                r.raise_for_status()
            response_html = await r.text()
            response_html = response_html.replace("\t", '').replace("\n", '').replace('location_data.push',
                                                                                      '\n\nlocation_data.push').replace(
                "'", '"').replace(",}", '}')
            matches = re.findall(regex, response_html, re.VERBOSE | re.IGNORECASE | re.MULTILINE)
            tasks = [asyncio.create_task(match_and_map(x)) for x in matches]
            res = await asyncio.gather(*tasks)
            return res


if __name__ == '__main__':

    scrape_datetime = datetime.datetime.now()
    scrape_domain = f'thehumanbean.com'
    scrape_store_name = 'The Human Bean'
    scrape_file_name = f'{slugify.slugify(scrape_store_name)}_{scrape_datetime.strftime("%m_%d_%Y_%H_%M_%S")}.json'

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    resluts = asyncio.run(main())
    df = pd.DataFrame(resluts)

    df['scrape_datetime'] = scrape_datetime
    df['scrape_domain'] = scrape_domain
    df['scrape_store_name'] = scrape_store_name

    df.to_json(scrape_file_name,orient='records')



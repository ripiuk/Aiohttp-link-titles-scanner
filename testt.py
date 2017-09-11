import asyncio
import aiohttp
import csv

WORKERS_NUM = 100


def get_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for url in reader:
            yield url[0]


def shreder(text):
    return text[text.find('<title>')+7:text.find('</title>')]


async def fetch(session: 'aiohttp.ClientSession', url_stream, storage, bad_links):
    for url in url_stream:
        try:
            async with session.get(url, timeout=10) as response:
                html = await response.text(encoding='utf-8')
                title = shreder(html)
                print(title)
                storage.append(title)
        except (aiohttp.ClientConnectorError, asyncio.TimeoutError) as e:
            print(url, e)
            bad_links.append(url)
        except UnicodeDecodeError as err:
            print(err)
            bad_links.append(url)


async def main(file):
    async with aiohttp.ClientSession() as session:
        url_stream = get_csv(file)
        links = []
        bad_links = []
        tasks = [asyncio.ensure_future(fetch(session, url_stream, links, bad_links))
                 for _ in range(WORKERS_NUM)]
        await asyncio.wait(tasks)
        return links

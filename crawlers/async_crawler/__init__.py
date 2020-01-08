# from .crawler import get_site_content

if __name__ == '__main__':

    import crawler
    import asyncio

    URL = 'https://aiohttp.readthedocs.io'

    loop = asyncio.get_event_loop()

    try:
        task = crawler.get_site_content(URL)
        result = loop.run_until_complete(task)
        print('Result: ', result)
    finally:
        loop.close()

import aiohttp

default_headers = (('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) '
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/75.0.3770.100 Safari/537.36'),)


async def get_site_content(url, headers=None):
    if not headers:
        headers = dict(default_headers)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.text()

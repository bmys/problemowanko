import aiohttp


async def get_site_content(url, headers=None):
    if not headers:
        headers = {'User-Agent': 'Googlebot-News'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return await resp.read()

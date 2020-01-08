import asyncio
import json
import requests
from crawlers import async_get_site_content
from scrappers import parse_offer

BASE_URL = "https://justjoin.it/"
# BASE_URL = "https://angular.io"
just_join_offer_list = {
    'offer': ("li", {"class": "offer-item"}, 'href')
}

just_join_offer = {
    'url': ("a", {"class": "item"}, 'href'),
    'company_name': ("span", {"class": "company-name"}, 'text'),
    'job_title': ("span", {"class": "title"}, 'text'),
    'salary': ("span", {"class": "salary"}, 'text'),
}


async def main():
    content = await async_get_site_content(BASE_URL)
    print(content)

    input('.....')

    content2 = requests.get(BASE_URL).text

    print('Are equal: ', content == content2)
    print(content2)

    # print(content)
    offers = parse_offer(content, just_join_offer)
    offers = list(offers)
    # print(json.dumps(offers))


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()

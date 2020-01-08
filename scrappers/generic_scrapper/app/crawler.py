import json
from typing import Text, Mapping
from bs4 import BeautifulSoup
from string import ascii_letters, digits


def clean_text(text):
    return ''.join(
        filter(lambda ch: ch in ascii_letters or ch in digits or ch == ' ', text))


def parse_offer(document_text: Text, info):
    base_soup: BeautifulSoup = BeautifulSoup(document_text, features="html.parser")
    offers = base_soup.find_all("li", {"class": "offer-item"})
    print(offers)

    return (collect_offer_info(offer, info) for offer in offers)


def collect_offer_info(offer_soup, additional_info: Mapping):
    def extract(selector):
        *selectors, getter = selector
        value = offer_soup.find(*selectors)
        return value.text if getter == 'text' else value.get(getter)

    return {k: extract(v) for k, v in additional_info.items()}

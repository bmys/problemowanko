#!/usr/bin/env python
import app
import json

if __name__ == "__main__":
    offers = app.fetch_offers()
    offers = list(offers)

    print(json.dumps(offers, cls=app.OfferEncoder))

import feedparser
import json
import requests

VERSION = "0.1.1"


def app_version():
    print("gnakrydev: ", VERSION)


def ping_mobile_app(params):
    gdev_broker_url = "https://broker-api.gnakrydev.com/webhooks/cmd?apiKey=" + params.apikey
    message_type = "ping"
    message_id = "cmd"

    payload = {"id": message_id, "type": message_type}
    requests.post(gdev_broker_url, data=json.dumps(payload))


def cve_feed():
    Feed = feedparser.parse('https://www.cert.ssi.gouv.fr/feed/')
    for feed in Feed.entries:
        print("-------------------------------------------------")
        print("-------------------------------------------------")
        print(feed.title)
        print(feed.link)

import feedparser
import json
import requests
import argparse
import feedparser
import json
import requests
import yaml
import uuid
import logging
import sys
from .Konstants import VERSION

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = logging.getLogger(__name__)


def app_version():
    print("gnakrydev: ", VERSION)


def ping_mobile_app(params):
    message_type = "ping"
    message_id = "cmd"
    payload = {"id": message_id, "type": message_type}
    webhook_message(params.apikey, payload)


def cve_feed():
    Feed = feedparser.parse('https://www.cert.ssi.gouv.fr/feed/')
    for feed in Feed.entries:
        print("-------------------------------------------------")
        print("-------------------------------------------------")
        print(feed.title)
        print(feed.link)


def health_check(params):
    with open(params.config) as file:
        endpoint_list = yaml.load(file, Loader=yaml.FullLoader)
        for endpoint in endpoint_list["endpoints"]:
            response = requests.get(endpoint["url"], verify=False)
            if response.status_code == 200:
                payload = {"id": endpoint["url"], "type": "success",
                           "title": endpoint["name"], "category": "healthCheck"}
                webhook_message(params.apikey, payload)
                logger.debug(endpoint["name"] + " => " +
                             endpoint["url"] + ":  🆗 ✅ 😀")
                if params.verbose:
                    print(endpoint["name"] + " => " +
                          endpoint["url"] + ":  🆗 ✅ 😀")
            else:
                payload = {"id": endpoint["url"], "type": "error",
                           "title": endpoint["name"], "category": "healthCheck"}
                webhook_message(params.apikey, payload)
                logger.debug(endpoint["name"] + " => " +
                             endpoint["url"] + ":  ❌ 😱 🚨")
                if params.verbose:
                    print(endpoint["name"] + " => " +
                          endpoint["url"] + ":  ❌ 😱 🚨")


def send_message(params):
    message_type = params.type if params.type else "info"
    message_id = params.id if params.id else str(uuid.uuid4())
    payload = {"id": message_id, "type": message_type,
               "title": params.title, "message": params.content, "category": "message"}
    webhook_message(params.apikey, payload)


def webhook_message(apikey, payload):
    gdev_broker_url = "https://broker-api.gnakrydev.com/webhooks/message?apiKey=" + apikey
    requests.post(gdev_broker_url, data=json.dumps(payload))

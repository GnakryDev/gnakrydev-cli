import argparse
import feedparser
import json
import requests
import yaml
import uuid
import logging
import sys
from .cli_package.library import ping_mobile_app, cve_feed, app_version
# Allow request for self signed https certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def health_check(params):
    gdev_broker_url = "https://broker-api.gnakrydev.com/webhooks/message?apiKey=" + params.apikey
    with open(params.config) as file:
        endpoint_list = yaml.load(file, Loader=yaml.FullLoader)
        for endpoint in endpoint_list["endpoints"]:
            response = requests.get(endpoint["url"], verify=False)
            if response.status_code == 200:
                payload = {"id": endpoint["url"], "type": "success",
                           "title": endpoint["name"], "category": "healthCheck"}
                requests.post(gdev_broker_url, data=json.dumps(payload))
                logger.debug(endpoint["name"] + " => " +
                             endpoint["url"] + ":  🆗 ✅ 😀")
                if params.verbose:
                    print(endpoint["name"] + " => " +
                          endpoint["url"] + ":  🆗 ✅ 😀")
            else:
                payload = {"id": endpoint["url"], "type": "error",
                           "title": endpoint["name"], "category": "healthCheck"}
                requests.post(gdev_broker_url, data=json.dumps(payload))
                logger.debug(endpoint["name"] + " => " +
                             endpoint["url"] + ":  ❌ 😱 🚨")
                if params.verbose:
                    print(endpoint["name"] + " => " +
                          endpoint["url"] + ":  ❌ 😱 🚨")


def send_message(params):

    gdev_broker_url = "https://broker-api.gnakrydev.com/webhooks/message?apiKey=" + params.apikey
    message_type = params.type if params.type else "info"
    message_id = params.id if params.type else str(uuid.uuid4())

    payload = {"id": message_id, "type": message_type,
               "title": params.title, "message": params.content, "category": "message"}
    requests.post(gdev_broker_url, data=json.dumps(payload))


def cli():
    parser = argparse.ArgumentParser(description='Gnakrydev-cli  app')
    subparser = parser.add_subparsers(dest='command')
    version = subparser.add_parser(
        'version', help="Show the app version")
    health = subparser.add_parser(
        'health', help="Perform a health-check of the endpoints listed on the YML file")
    message = subparser.add_parser(
        'message', help="Send a notification to the Gnakrydev Mobile-APP")
    cve = subparser.add_parser('cve', help="List CERT-FR rss recents  vulns")
    ping = subparser.add_parser(
        'ping', help="Send a ping message to the  Gnakrydev Mobile-APP")

    # GnakryDev YML config file
    health.add_argument('--config', type=str,
                        required=True, metavar="", help="YAML config file path")

    # ApiKey available on the mobile-app
    health.add_argument('--apikey', type=str, required=True, metavar="",
                        help="apiKey available on the mobile-app")
    # ApiKey available on the mobile-app
    ping.add_argument('--apikey', type=str, required=True, metavar="",
                      help="apiKey available on the mobile-app")
    #
    health.add_argument('--verbose', action='store_true',
                        help="Show request details in stdout")
    #
    message.add_argument('--apikey', type=str, required=True, metavar="",
                         help="apiKey available on the mobile-app")
    #
    message.add_argument('--id', type=str, metavar="",
                         help="Message ID, Default= ramdom uuid")
    #
    message.add_argument('--title', type=str, metavar="",
                         required=True, help="Message title")

    # Message content
    message.add_argument('--content', type=str, metavar="",
                         required=True, help="Message content")

    # Message type
    message.add_argument('--type', type=str, metavar="",
                         help="Message type:  info, warning, success, error. Default= info")

    args = parser.parse_args()

    if args.command == 'version':
        app_version()
    elif args.command == 'health':
        health_check(args)
    elif args.command == 'message':
        send_message(args)
    elif args.command == 'cve':
        cve_feed()
    elif args.command == 'ping':
        ping_mobile_app(args)

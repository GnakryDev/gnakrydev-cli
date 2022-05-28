import argparse
import json
import requests
import yaml
import uuid
# Allow request for self signed https certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
                if params.verbose:
                    print(endpoint["name"] + " => " +
                          endpoint["url"] + ":  🆗 ✅ 😀")
            else:
                payload = {"id": endpoint["url"], "type": "error",
                           "title": endpoint["name"], "category": "healthCheck"}
                requests.post(gdev_broker_url, data=json.dumps(payload))
                if params.verbose:
                    print(endpoint["name"] + " => " +
                          endpoint["url"] + ":  ❌ 😱 🚨")


def send_message(params):

    gdev_broker_url = "https://broker-api.gnakrydev.com/webhooks/message?apiKey=" + params.apikey
    if params.type:
        message_type = params.type
    else:
        message_type = "info"
    payload = {"id": str(uuid.uuid4()), "type": message_type,
               "title": params.title, "message": params.content, "category": "message"}
    requests.post(gdev_broker_url, data=json.dumps(payload))


def cli():
    parser = argparse.ArgumentParser(description='Gnakrydev-cli  app')
    subparser = parser.add_subparsers(dest='command')
    health = subparser.add_parser('health')
    message = subparser.add_parser('message')

    # GnakryDev YML config file
    health.add_argument('--config', type=str,
                        required=True, help="YML config file")

    # ApiKey available on the mobile-app
    health.add_argument('--apikey', type=str, required=True,
                        help="apiKey available on the mobile-app")

    #
    health.add_argument('--verbose', action='store_true',
                        help="Show request details in stdout")
    message.add_argument('--apikey', type=str, required=True,
                         help="apiKey available on the mobile-app")
    #
    message.add_argument('--title', type=str,
                         required=True, help="Message title")

    # Message content
    message.add_argument('--content', type=str,
                         required=True, help="Message content")

    # Message type
    message.add_argument('--type', type=str,
                         help="Message type:  info, warning, success, error. Default= info")

    args = parser.parse_args()

    if args.command == 'health':
        health_check(args)
    elif args.command == 'message':
        send_message(args)

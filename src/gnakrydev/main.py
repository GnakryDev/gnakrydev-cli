import argparse
import json
import requests
import yaml

# Allow request for self signed https certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def health_check(gnakrydev_yml_file, apiKey):
    gdev_broker_url = "https://broker-api.gnakrydev.com/webhooks/message?apiKey=" + apiKey
    with open(gnakrydev_yml_file) as file:
        endpoint_list = yaml.load(file, Loader=yaml.FullLoader)
        for endpoint in endpoint_list["endpoints"]:
            response = requests.get(endpoint["url"], verify=False)
            if response.status_code == 200:
                payload = {"id": endpoint["url"], "type": "success",
                           "title": endpoint["name"], "category": "healthCheck"}
                requests.post(gdev_broker_url, data=json.dumps(payload))
            else:
                payload = {"id": endpoint["url"], "type": "error",
                           "title": endpoint["name"], "category": "healthCheck"}
                requests.post(gdev_broker_url, data=json.dumps(payload))


def cli():
    parser = argparse.ArgumentParser(description='Gnakrydev-cli client app')
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--apikey', type=str, required=True)

    args = parser.parse_args()
    health_check(args.config, args.apikey)

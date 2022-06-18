import argparse
import feedparser
import json
import requests
import yaml
import uuid
import logging
import sys
from .cli_package.library import ping_mobile_app, cve_feed, app_version, health_check, send_message, docker_container_health
# Allow request for self signed https certificates
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def cli():
    # Initialize the parser
    parser = argparse.ArgumentParser(description='Gnakrydev-cli  app')
    # Create a subparser
    subparser = parser.add_subparsers(dest='command')
    # Create a command
    version = subparser.add_parser(
        'version', help="Show the app version")
    health = subparser.add_parser(
        'health', help="Perform a health-check of the endpoints listed on the YML file")
    message = subparser.add_parser(
        'message', help="Send a notification to the Gnakrydev Mobile-APP")
    cve = subparser.add_parser('cve', help="List CERT-FR rss recents  vulns")
    ping = subparser.add_parser(
        'ping', help="Send a ping message to the  Gnakrydev Mobile-APP")

    docker = subparser.add_parser(
        'docker', help="Docker command SDK")

    # Create arguments for the command

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

    # ApiKey available on the mobile-app
    docker.add_argument('--apikey', type=str, required=True, metavar="",
                        help="apiKey available on the mobile-app")

    docker.add_argument('--c_status', action='store_true',
                        help="Show and send containers status")

    # Load all arguments from the CLI
    args = parser.parse_args()

    # Check
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
    elif args.command == 'docker':
        # ping_mobile_app(args)
        docker_container_health(args)

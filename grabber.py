import argparse
import os
import re
import signal
import sys
from urllib.parse import urlparse

import requests


class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()


def handler(signum, frame):
    exit(0)


def is_valid_file(arg):
    if os.path.exists(arg):
        return arg
    elif os.access(os.path.dirname(arg), os.W_OK):
        return arg
    else:
        raise argparse.ArgumentTypeError("Provided file path is not valid")


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='URL of flubot downloader', required=True)
    parser.add_argument('-p', '--path', help='Path for file output', required=False, type=is_valid_file)
    parser.add_argument('--domain-only', dest="domain", help='Return unique domains only', required=False, action="store_true", default=False)
    return parser


regex = re.compile(r'(?:href=")([^"]*)(?:">Download application)')
session = requests.session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; PRA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36'
}
grabbed = []


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    p = setup_args()
    args = p.parse_args()

    url = args.url
    domain = args.domain

    if args.path:
        f = open(args.path, "a+")
        sys.stdout = Tee(sys.stdout, f)

    no_new_count = 0
    while no_new_count < 20:
        req = session.get(url)
        if not req.ok:
            print("Site looks down!")
            exit()

        matches = regex.findall(req.text)

        if len(matches) == 0:
            print("No download URLs detected")

        for match in matches:
            if domain:
                up = urlparse(match)
                match = up.scheme + '://' + up.hostname
            if match not in grabbed:
                grabbed.append(match)
                no_new_count = 0
                print(match)
            else:
                no_new_count += 1

    print("No new domains detected for 20 attempts. Stopping!")

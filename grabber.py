import requests
import re
import argparse
import os
from urllib.parse import urlparse
import signal


def handler(signum, frame):
    exit(0)


def is_valid_file(parser, arg):
    if os.path.exists(arg):
        return arg
    elif os.access(os.path.dirname(arg), os.W_OK):
        return arg
    else:
        raise "Provided file path is not valid"


def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='URL of flubot downloader', required=True)
    parser.add_argument('-p', '--path', help='Path for file output', required=False, type=lambda x: is_valid_file(parser, x))
    parser.add_argument('--domain-only', dest="domain", help='Return unique domains only', required=False, action="store_true", default=False)
    return parser


regex = re.compile(r'(?:href=")([^"]*)(?:">Download application)')
session = requests.session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; PRA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36'
}
grabbed = []


if __name__ == '__main__':
    p = setup_args()
    args = p.parse_args()

    url = args.url
    path = args.path
    domain = args.domain

    signal.signal(signal.SIGINT, handler)

    while True:
        req = session.get(url)
        if not req.ok:
            print("Site looks down!")
            exit()

        matches = regex.findall(req.text)
        for match in matches:
            if domain:
                up = urlparse(match)
                match = up.scheme + '://' + up.hostname
            if match not in grabbed:
                grabbed.append(match)
                print(match)
                if path is not None:
                    with open(path, "a+") as f:
                        f.write(match + "\n")

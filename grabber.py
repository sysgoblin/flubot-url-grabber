#!/usr/bin/python3
import argparse
import os
import re
import signal
import sys
from urllib.parse import urlparse
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

import requests

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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', help='URL of flubot downloader')
    group.add_argument('-i', '--input', help='Path for input file containing URLs to scan', type=is_valid_file)
    parser.add_argument('-p', '--path', help='Path for file output', required=False, type=is_valid_file)
    parser.add_argument('--domain-only', dest="domain", help='Return domains only, not full URLs', required=False, action="store_true", default=False)
    return parser


regex = re.compile(r'(?:class="btn" href=")([^"]*)(?:">)')
# session = requests.session()
session = FuturesSession()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; PRA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36'
}
grabbed = []

def output(match, path):
    print(match)
    if path is not None:
        with open(path, 'a+') as f:
            f.write(match + "\n")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    p = setup_args()
    args = p.parse_args()

    if args.input:
        with open(args.input, 'r') as f:
            urls = f.read().splitlines()
    elif args.url:
        urls = [args.url]
    else:
        print("No input?")
        exit()

    domain = args.domain

    for url in urls:
        loop = True
        while loop:
            new_count = 0
            futures = [session.get(url) for i in range(10)]
            for future in as_completed(futures):
                req = future.result()
                if not req.ok:
                    print("Site looks down!")
                    continue

                match = regex.findall(req.text)[0]

                if not match:
                    print("No download URLs detected")
                    continue

                if domain:
                    up = urlparse(match)
                    match = up.scheme + '://' + up.hostname
                if match not in grabbed:
                    grabbed.append(match)
                    new_count += 1
                    output(match, args.path)
                
                if new_count == 0:
                    loop = False
        print("No new URLs detected for 10 attempts. Stopping!")

#!/usr/bin/env python3

import argparse
import os
import sys
from textwrap import dedent

try:
    import requests
except ImportError:
    print("'requests' module is not installed", file=sys.stderr)
    sys.exit(1)

import utils

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CustomArgumentParser(argparse.ArgumentParser):
    """Override ArgumentParser's help message"""
    def format_help(self):
        help_text = dedent(f"""\
        chan-parser is a script for downloading attachments from one or several threads on 2ch or 4chan.
        https://github.com/m3tro1d/chan-scraper

        Usage: {self.prog} {{all|images|videos}} [OPTIONS] URL [URL]...

        URL:
          Thread's URL

        Options:
          -h,  --help     show help
          -o,  --output   output directory (def: current)
        """)
        return help_text

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parse_arguments():
    """Process input arguments"""
    parser = CustomArgumentParser(usage="%(prog)s {all|images|videos} [OPTIONS] URL [URL]...")

    parser.add_argument("mode", choices=["all", "images", "videos"])

    parser.add_argument("urls", nargs="*")

    parser.add_argument("-o", "--output", default=".")

    args = parser.parse_args()
    return args


def check_arguments(urls, directory):
    """Checks if the arguments are valid"""
    # Check input URLs
    if not len(urls):
        print("Error: no URL provided.")
        sys.exit(1)
    # Check output directory
    if not os.path.isdir(directory):
        os.mkdir(directory)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    """Entry point of the script"""
    # Get the input arguments
    args = parse_arguments()
    mode = args.mode
    urls = args.urls
    directory = os.path.abspath(args.output)

    # Check the input arguments
    check_arguments(urls, directory)

    # Parse single thread
    if len(urls) == 1:
        utils.parse_thread(urls[0], mode, directory, True)
    # Parse multiple threads
    else:
        utils.parse_multiple_threads(urls, mode, directory)


# Entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupt", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print("\nConnection error", file=sys.stderr)
        sys.exit(1)
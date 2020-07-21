import argparse
import os
import sys

import requests

import extractors.dvach as dvach


def get_extension(name):
    return name.split(".")[-1]


def is_image(ext):
    return (ext == "jpg" or ext == "jpeg" or
        ext == "png" or ext =="gif")


def is_video(ext):
    return ext == "webm" or ext == "mp4"


def count_files(files_list, mode="all"):
    """Returns files amount according to the specified mode"""
    n = 0
    for _, file_name in files_list:
        ext = get_extension(file_name)
        if mode == "images" and is_image(ext):
            n += 1
        elif mode == "videos" and is_video(ext):
            n += 1
        elif mode == "all":
            n += 1
    return n


def save_file(url, directory, name):
    """Save a file into the specified directory"""
    # Check if the image already exists
    full_name = os.path.join(directory, name)
    if not os.path.isfile(full_name):
        img_file = open(full_name, "wb")
        for chunk in requests.get(url):
            img_file.write(chunk)
        img_file.close()


# Parse arguments
parser = argparse.ArgumentParser(
    description="""Downloads all files, images or videos from the
    thread on 2ch.hk.""")

parser.add_argument("MODE", choices=["all", "images", "videos"],
    help="parse mode, e.g. what files to download")

parser.add_argument("URL",
    help="thread url")

parser.add_argument("-o", metavar="DIR", default=".",
    help="output directory (default: current)")

args = parser.parse_args()
mode = args.MODE
url = args.URL
directory = os.path.abspath(args.o)


try:
    # Get all the files' URLs
    file_list = dvach.get_files_urls_names(url)
    # Count the files
    amount = count_files(file_list, mode)
except Exception as ex:
    # Handle requests exceptions
    print("Request error: {}".format(ex))
    print("Download failed, exiting.")
    sys.exit(1)


# Ask user
print("{} files will be saved in the '{}' directory.".format(amount,
    directory))
choice = input("Proceed (Y/n)? ")
if not (choice.lower() in ["y", ""]):
    print("As you wish...")
    sys.exit(0)


# Check the output directory
if not os.path.isdir(directory):
    print("\nHmm, '{}' directory doesn't seem to exist...".format(directory))
    print("Nevermind, I'll just create one.")
    os.mkdir(directory)


# Actual downloading is happening here
print("\nDownloading...")
# Posts loop
n = 1
for file_url, file_name in file_list:
    ext = get_extension(file_url)
    # Save the files according to the mode
    if ((mode == "images" and is_image(ext)) or
        (mode == "videos" and is_video(ext)) or
        (mode == "all")):
        save_file(file_url,
            directory,
            file_name)
        print("{:>3}/{} - {}".format(n, amount, file_name))
        n += 1

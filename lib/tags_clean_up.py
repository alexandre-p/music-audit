#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import browser
import argparse
import sys
from mutagen import File
from mutagen.mp3 import HeaderNotFoundError
import os

DEFAULT_FOLDER = './'

def update_progress(progress, total):
    percent = int(progress / total * 100)
    sys.stdout.write("\r%d/%d (%d%%)" % (progress, total, percent))
    sys.stdout.flush()


def init_command_parser():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Audit a music library')
    parser.add_argument('--folder', '-f', help='Music library folder', default=DEFAULT_FOLDER, action=browser.ReadableDir)

    return parser.parse_args()


def main():
    arguments = init_command_parser()

    print("Looking for files...")

    fileBrowser = browser.Browser(arguments.folder)
    files = list(fileBrowser.find(['mp3']))

    number_of_files = len(files)
    print("Working on %d files" % number_of_files)
    tags_to_delete = ["media", "comment", "copyright", "encodedby", "organization"]
    failed_to_open = []
    for i, f in enumerate(files):
        update_progress(i + 1, number_of_files)
        needs_saving = False
        try:
            music_file = File(os.path.join(f[1], f[0]), easy=True)
        except HeaderNotFoundError:
            failed_to_open.append(os.path.join(f[1], f[0]))
            continue

        if "performer" not in music_file or (music_file["performer"] != music_file['artist']):
            music_file["performer"] = music_file['artist']
            needs_saving = True

        for tag in tags_to_delete:
            if tag in music_file:
                del music_file[tag]
                needs_saving = True

        if needs_saving is True:
            music_file.tags.save()

    print("")
    print("Done")
    print("")
    for f in failed_to_open:
        print(f)
    print("")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye !")
        sys.exit(0)

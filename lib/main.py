#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from music import MusicFile
import sys
import argparse
import reporter
import browser
import audit

DEFAULT_FOLDER = './'
REQUIRED_TAGS = ['album', 'title', 'artist', 'date', 'tracknumber']


def init_command_parser():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Audit a music library')
    parser.add_argument('--folder', '-f', help='Music library folder', default=DEFAULT_FOLDER, action=browser.ReadableDir)

    parser.add_argument('--required-tags', help='Scan Music for this tags', default=['album', 'title', 'artist', 'date', 'tracknumber'], nargs='+')
    parser.add_argument('--tags-audit', '-t', help='Audit tags', action="store_true")
    parser.add_argument('--tags-report-by-tag', help='Show errors by tag', action="store_true")

    parser.add_argument('--bitrate-audit', '-b', help='Audit bitrate', action="store_true")
    parser.add_argument('--bitrate-repartition', '-r', help='Show bitrate repartition', action="store_true")

    parser.add_argument('--output', '-o', help='Output CSV file', type=argparse.FileType('wb', 0))

    return parser.parse_args()


def update_progress(progress, total):
    percent = int(progress / total * 100)
    sys.stdout.write("\r%d/%d (%d%%)" % (progress, total, percent))
    sys.stdout.flush()


def main():
    arguments = init_command_parser()

    print("Looking for files...")

    fileBrowser = browser.Browser(arguments.folder)
    files = list(fileBrowser.find(['mp3']))

    runner = audit.Runner()
    if arguments.tags_audit or arguments.tags_report_by_tag:
        tagsAuditor = audit.Tags(arguments.required_tags)
        if arguments.tags_audit:
            tagsAuditor.add_reporter(reporter.TagErrorsByRoot())

        if arguments.tags_report_by_tag:
            tagsAuditor.add_reporter(reporter.TagErrorByTag())

        runner.add_auditor(tagsAuditor)

    if arguments.bitrate_audit or arguments.bitrate_repartition:
        bitrateAuditor = audit.Bitrate()
        if arguments.bitrate_audit:
            bitrateAuditor.add_reporter(reporter.BitrateByRoot())

        if arguments.bitrate_repartition:
            bitrateAuditor.add_reporter(reporter.BitrateRepartition())

        runner.add_auditor(bitrateAuditor)

    number_of_files = len(files)
    print("Auditing %d files" % number_of_files)

    for i, f in enumerate(files):
        update_progress(i + 1, number_of_files)
        music_file = MusicFile(f[0], f[1], arguments.folder)
        runner.audit(music_file)

    print("")
    print("")

    for a in runner.auditors:
        for r in a.reporters:
            r.echo()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye !")
        sys.exit(0)

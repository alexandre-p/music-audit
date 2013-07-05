import sys


class Runner(object):
    def __init__(self):
        self._auditors = []
        self._progress_listeners = []

    @property
    def auditors(self):
        return self._auditors

    def add_auditor(self, auditor):
        self._auditors.append(auditor)

    def add_progress_listener(self, listener):
        self._progress_listeners.append(listener)

    def notify_progress(self, value, total):
        for listener in self._progress_listeners:
            listener.update(value, total)

    def audit(self, music_file):
        for auditor in self._auditors:
            auditor.audit(music_file)
            for reporter in auditor.reporters:
                reporter.data = auditor.results


class Auditor(object):
    _reporters = []

    def audit(self):
        raise NotImplementedError()

    @property
    def results(self):
        return self._results

    def report(self):
        if self.reporter is not None:
            self.reporter.echo()

    @property
    def reporters(self):
        return self._reporters

    def add_reporter(self, reporter):
        self._reporters.append(reporter)


class Tags(Auditor):
    def __init__(self, required_tags):
        self._results = {}
        self._required_tags = required_tags

    def audit(self, music_file):
        for missing_tag in music_file.get_missing_tags(self._required_tags):
            self._results.setdefault(missing_tag, []).append(music_file)


class Bitrate(Auditor):
    def __init__(self):
        self._results = {}

    def audit(self, music_file):
        bitrate = music_file.bitrate
        self._results.setdefault(bitrate, []).append(music_file)


class ProgressListener(object):
    def update(self, value, total):
        raise NotImplementedError()


class ConsoleProgressListener(ProgressListener):
    def update(self, value, total):
        percent = int(value / total * 100)
        sys.stdout.write("\r%d/%d (%d%%)" % (value, total, percent))
        sys.stdout.flush()

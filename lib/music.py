import os
from mutagen import File
from mutagen.mp3 import HeaderNotFoundError


class MusicFile(object):
    _tags = None
    _error = False
    _file = None
    _bitrate = None
    _tags = None
    _root = None
    _short_path = None

    def __init__(self, filename, dirname, folder):
        self._filename = filename
        self._dirname = dirname
        self._filePath = os.path.join(dirname, filename)
        self._folder = folder

    @property
    def bitrate(self):
        if self._bitrate is None:
            self._load_file()
            if hasattr(self._file, 'info') and hasattr(self._file.info, 'bitrate'):
                self._bitrate = self._file.info.bitrate
            else:
                self._bitrate = 0

        return self._bitrate

    @property
    def tags(self):
        if self._tags is None:
            self.get_tags()
        return self._tags

    def get_tags(self):
        if self._tags is None:
            try:
                self._tags = File(self._filePath, easy=True)
            except HeaderNotFoundError:
                self._tags = []
                self._error = True
        return self._tags

    def get_missing_tags(self, tags):
        if self._tags is None:
            try:
                self._tags = File(self._filePath, easy=True)
            except HeaderNotFoundError:
                self._error = True
                return

        for tag in tags:
            if tag not in self.get_tags():
                yield tag

    def _load_file(self):
        try:
            self._file = File(self._filePath)
        except HeaderNotFoundError:
            pass

    @property
    def short_path(self):
        if self._short_path is None:
            self._short_path = self._filePath.replace(self._folder, '').replace('./', '')
        return self._short_path

    @property
    def root(self):
        if self._root is None:
            self._root = self.short_path.split(os.sep)[0]
        return self._root

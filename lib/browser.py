import argparse
import os


class ReadableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            if not prospective_dir.endswith(os.sep):
                prospective_dir += os.sep
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


class Browser(object):
    def __init__(self, folder):
        self._folder = folder

    def find(self, extensions):
        for dirname, dirnames, filenames in os.walk(self._folder):
            for filename in filenames:
                for extension in extensions:
                    if filename.lower().endswith(extension):
                        yield (filename, dirname)

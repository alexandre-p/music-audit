from __future__ import division


class Reporter(object):
    """An abstract class for audit reporters

    Attributes:
    data -- Result of the audit
    result -- Data transformation result
    """
    def __init__(self):
        self._result = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def result(self):
        if self._result is None:
            self._result = self.get()
        return self._result

    def get(self):
        """Process audit data to get wanted information"""
        pass

    def echo(self):
        """Output processed data"""
        pass


class Tags(Reporter):
    """Tags reporter"""
    pass


class TagErrorByTag(Tags):
    """Error report broken down by missing tag"""
    def get(self):
        results = {}
        for tag, files in self._data.items():
            results[tag] = results.setdefault(tag, {})
            for f in files:
                results[tag][f.root] = results[tag].setdefault(f.root, 0) + 1

        return results

    def echo(self):
        for tag, roots in self.result.items():
            print('=== %s ===' % tag.title())
            for root, count in roots.items():
                print('%s : %d' % (root, count))
            print("")


class TagErrorsByRoot(Tags):
    """Error report broken down by root folder of the music files"""
    def get(self):
        errors_by_root = {}
        for tag, files in self._data.items():
            for f in files:
                errors_by_root[f.root] = errors_by_root.setdefault(f.root, 0) + 1

        return errors_by_root

    def echo(self):
        total_errors = 0
        for root, count in sorted(self.result.items()):
            total_errors += count
            print("%s : %d" % (root, count))
        print("")
        print("Total errors : %d" % total_errors)


class Bitrate(Reporter):
    """Bitrate reporter"""
    _bitrate_steps = [0, 128000, 192000, 256000, 320000]

    @property
    def bitrate_steps(self):
        return self._bitrate_steps

    @bitrate_steps.setter
    def bitrate_steps(self, value):
        self._bitrate_steps = sorted(value)

    def _print_count_results(self, results, reverse=True):
        for root, count in sorted(results.items(), key=lambda t: t[1], reverse=reverse):
            print("%s : %d" % (root, count))

    def get_normalized_bitrates(self):
        data = dict(self._data)

        for bitrate in sorted([b for b in data.keys() if b not in self.bitrate_steps]):
            normalized_bitrate = self.get_bitrate_closest_step(bitrate)
            data.setdefault(normalized_bitrate, []).extend(data[bitrate])

            del data[bitrate]

        return data

    def get_bitrate_closest_step(self, bitrate):
        for step in reversed(self.bitrate_steps):
            if bitrate >= step:
                return step
        return 0


class BitrateByRoot(Bitrate):
    """Bitrate report broken down by root folder of the music files"""
    def get(self):
        data = self.get_normalized_bitrates()
        results = {}
        for bitrate, files in sorted(data.items()):
            for f in files:
                results[bitrate][f.root] = results.setdefault(bitrate, {}).get(f.root, 0) + 1
        return results

    def echo(self):
        for bitrate, roots in self.result.items():
            print("=== %d ===" % (bitrate / 1000))
            self._print_count_results(roots, True)
            print("")


class BitrateRepartition(Bitrate):
    """Bitrate repartition visualisation"""
    def get(self):
        return self.get_normalized_bitrates()

    def echo(self):
        print("")
        print("=== Bitrates ===")
        sizes = [len(files) for files in self.result.values()]
        total = sum(sizes)
        maxCount = max(sizes)
        for bitrate, files in sorted(self.result.items()):
            count = len(files)
            number_of_dash = max(int(count / total * 50), 1)
            number_of_spaces = 50 - number_of_dash
            print("\t%d\t%s%s%d" % (bitrate / 1000, "#" * number_of_dash, " " * number_of_spaces, count))

        print("\t\t%s%s" % (" " * 50, "-" * len(str(maxCount))))
        print("\t\t%s%d" % (" " * 50, total))

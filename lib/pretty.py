import sys

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


# From http://code.activestate.com/recipes/475186-has_colorsstream-does-an-output-stream-support-col/
def has_colours(stream):
    """Checks if colours can be printed in the current output"""
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)


def echo(text, color=None, background=None, bold=False, underline=False):
    """Display text, with formatting if possible"""
    if has_colours:
        code = []
        if bold:
            code.append("1")
        if underline:
            code.append("4")
        if color:
            code.append(str(30 + color))
        if background:
            code.append(str(40 + background))

        if len(code) > 0:
            text = "\x1b[%sm%s\x1b[0m" % (";".join(code), text)

        sys.stdout.write(text)
    else:
        sys.stdout.write(text)

    sys.stdout.write("\n")

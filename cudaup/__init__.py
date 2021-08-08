''' cudaup '''
import sys
import argparse
import traceback

from .version_limits import ( # pylint: disable=E0402
    MINIMUM_VERSION, VERSION_LIMIT
)

BUILD_TEMP = "src/*/*/lib/*-*"
SYSTEM_SHELL = "/bin/sh"

def fail(msg):
    ''' fail with msg '''
    backtrace = traceback.format_stack()
    print("\n%s\n\n%s" % (msg, ''.join(backtrace[:-1])), file=sys.stderr)
    sys.exit(1)

def check_python_version():
    ''' check version '''
    svi = sys.version_info

    if not VERSION_LIMIT > svi >= MINIMUM_VERSION:
        fail(
            "Did not meet python version requirements\n"
            "Current version = (%s, %s, %s)\n"
            "Minimum version = %s\n"
            "Version limit = %s" %
            (
                svi.major, svi.minor, svi.micro,
                MINIMUM_VERSION, VERSION_LIMIT
            )
        )

class ArgumentParser():  # pylint: disable=R0903
    ''' Simplified argument parser '''
    def __init__(self, description):
        self.parser = argparse.ArgumentParser(description=description)

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            self.parser.add_argument(*args, **kwargs)
            return self
        return self.parser.parse_args()

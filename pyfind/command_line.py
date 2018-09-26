import argparse
import sys


class Arguments:

    def __init__(self, args=sys.argv[1:]):
        self.origin_args = args
        self.parser = argparse.ArgumentParser(description="",
                                              prog="python -m pyfind")

    @property
    def add_argument(self):
        return self.parser.add_argument

    @property
    def args(self):
        return self.parser.parse_args(self.origin_args)

    def get(self, key):
        return getattr(self.args, key)

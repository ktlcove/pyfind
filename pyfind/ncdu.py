import collections
import json
import os
import subprocess

from pyfind import CONFIG


class Ncdu:

    def __init__(self, ncdu_path=None):
        self.ncdu = ncdu_path or CONFIG["ncdu_path"]

    @property
    def cmd(self):
        return f"{self.ncdu} -0xo- {{0}} 2> /dev/null "

    def _execute(self, path):

        if not os.path.isdir(path):
            raise RuntimeError(f"input must be a dir")

        code, origin_result = subprocess.getstatusoutput(self.cmd.format(path))

        if code != 0:
            raise RuntimeError(f"{self.cmd.format(path)} return: {code} != 0")

        data = json.loads(origin_result)

        real_data = data[3]

        return real_data

    def _filter_one(self, item, base_path, min_size, max_size, result):
        if min_size is not None and item.get("dsize", 0) < min_size:
            return item.get("dsize", 0)
        if max_size is not None and item.get("dsize", 0) > max_size:
            return item.get("dsize", 0)
        path = os.path.join(base_path, item["name"]) if base_path \
            else item["name"]
        result[path] = {"dsize": item.get("dsize", 0), "inode": item["ino"]}
        return item.get("dsize", 0)

    def _filter(self, data, base_path=None, recurse=False,
                min_size=None, max_size=None,
                result=None):

        if type(data) is dict:
            # dict 是个文件
            return self._filter_one(data, base_path, min_size, max_size, result)
        else:
            # list 是个目录 第一个元素是目录自身 其余是目录内子项
            path = os.path.join(base_path, data[0]["name"]) if base_path \
                else data[0]["name"]
            dir_total = data[0].get("asize", 0)
            if recurse and data[1:]:
                for item in data[1:]:
                    s = self._filter(item, base_path=path, min_size=min_size,
                                     max_size=max_size, result=result,
                                     recurse=recurse)
                    dir_total += s
            self._filter_one(data[0], base_path, min_size, max_size, result)

            return dir_total

    def execute(self, path, recurse=False, min_size=None, max_size=None):
        data = self._execute(path)
        result = collections.OrderedDict()
        self._filter(data, base_path=None,
                            min_size=min_size, max_size=max_size,
                            recurse=recurse, result=result)
        return result
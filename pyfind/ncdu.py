# coding:utf8
import collections
import json
import os

from pyfind._six import getstatusoutput


class SortedDict:

    def __init__(self, size):
        self._size = size
        self._data = collections.defaultdict(list)
        self._order = []
        self._count = 0

    def __len__(self):
        return self._count

    @property
    def min(self):
        if self._order:
            return self._order[0]
        return None

    @property
    def max(self):
        if self._order:
            return self._order[-1]
        return None

    def keys(self):
        return self._order[::-1]

    def __setitem__(self, key, value):
        if self._count < self._size:
            self._data[key].append(value)
            self._count += 1
            self._order.append(key)
            self._order.sort()
        elif key >= self.min:
            self._data[key].append(value)
            self._count += 1
            self._order.append(key)
            self._order.sort()
            # pop
            if self._count - self._size and \
                    self._count - self._size == len(self._data[self.min]):
                self._data.pop(self.min)
                self._order = self._order[self._count - self._size:]

                # print(key, value, self._order,
                #     {k: len(v) for k, v in self._data.items()})

                self._count = len(self._order)

    def items(self):
        keys = list(set(self._order))
        keys.sort()
        keys.reverse()
        # print(keys)
        # pprint.pprint(dict(self._data))
        result = []
        for key in keys:
            # print("add ", key)
            for v in self._data[key]:
                # print("add ", key, v)
                result.append((key, v))
        # pprint.pprint(result)
        return result

    def __getitem__(self, item):
        return self._data.__getitem__(item)

    def __iter__(self):
        return self._order.__iter__()


class Ncdu:
    """
    find 的文件大小检索在这里做
    """

    def __init__(self, ncdu_path=None):
        # 可执行文件路径
        self.ncdu = ncdu_path or "ncdu"

    @property
    def cmd(self):
        return self.ncdu + ' -0xo- {} 2> /dev/null'

    def _execute(self, path):
        """
        输入是目标目录
        输出为目录内所有文件及信息
        """
        if not os.path.isdir(path):
            raise RuntimeError("input must be a dir")

        code, origin_result = getstatusoutput(self.cmd.format(path))
        if code != 0:
            cmd = self.cmd.format(path)
            raise RuntimeError("{} return: {} != 0".format(cmd, code))

        data = json.loads(origin_result)

        real_data = data[3]

        return real_data

    def _set_count(self, data, result, base_path=None):
        if type(data) is list:
            path = os.path.join(base_path, data[0]["name"]) if base_path \
                else data[0]["name"]

            data[0]["ino_count"] = len(data) - 1 + sum([
                self._set_count(i, result, base_path=path)
                if type(i) is list else 1 for i in data[1:]
            ])
            data[0]["path"] = path

            result[data[0]["ino_count"]] = data[0]

            return data[0]["ino_count"]

        return 1

    def _filter_one(self, item, base_path, min_size, max_size, result):

        """
        根据条件决定是否将item加入到result
        并返回item的dsize

        没有asize 没有dsize的文件是空文件
        文件夹没有dsize只有asize
        """

        if min_size is not None and item.get("dsize", 0) < min_size:
            return item.get("dsize", 0)
        if max_size is not None and item.get("dsize", 0) > max_size:
            return item.get("dsize", 0)
        path = os.path.join(base_path, item["name"]) if base_path \
            else item["name"]
        result[path] = {"dsize": item.get("dsize", 0), "inode": item["ino"]}
        return item.get("dsize", 0)

    def _filter(self, data, base_path=None, recurse=False,
                min_size=None, max_size=None, with_dir=None,
                result=None):

        """递归检索data"""

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
            if with_dir:
                data[0]["dsize"] = dir_total
                self._filter_one(data[0],
                                 base_path, min_size, max_size, result)

            return dir_total

    def execute(self, path, recurse=False, min_size=None, max_size=None,
                with_dir=None):
        """
        入口
        :param path: 目标文件夹路径
        :param recurse: 递归检索
        :param min_size: 最小大小
        :param max_size: 最大大小
        :param with_dir: 检索文件夹大小
        :return: 符合要求的文件及信息 （dict格式）
        """
        data = self._execute(path)
        result = collections.OrderedDict()
        self._filter(data, base_path=None,
                     min_size=min_size, max_size=max_size,
                     recurse=recurse, result=result, with_dir=with_dir)
        return result

    def _get_size_top_add_one(self, item, base_path, result):
        path = os.path.join(base_path, item["name"]) if base_path \
            else item["name"]
        result[item.get("dsize")] = {"dsize": item.get("dsize", 0),
                                     "inode": item["ino"],
                                     "path": path}

    def _get_size_top(self, data, base_path=None, result=None):
        if type(data) is dict:
            # dict 是个文件
            self._get_size_top_add_one(data, base_path=base_path, result=result)
        else:
            # list 是个目录 第一个元素是目录自身 其余是目录内子项
            path = os.path.join(base_path, data[0]["name"]) if base_path \
                else data[0]["name"]
            for item in data[1:]:
                self._get_size_top(item, base_path=path, result=result)

    def get_size_top(self, path, count=10):
        data = self._execute(path)
        result = SortedDict(count)
        self._get_size_top(data, base_path=None, result=result)
        real_result = collections.OrderedDict()

        for size, info in result.items():
            # print(size, info)
            real_result[info["path"]] = info
        return real_result

    def get_inode_top(self, path, count=10):
        data = self._execute(path)
        result = SortedDict(count)
        self._set_count(data, result)
        real_result = collections.OrderedDict()
        for size, info in result.items():
            real_result[info["path"]] = info
        return real_result


if __name__ == '__main__':
    Ncdu().get_inode_top(".")
# coding:utf8
import collections
import json
import os

from pyfind._six import getstatusoutput

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

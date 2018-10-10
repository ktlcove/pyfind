# coding:utf8
import os
import re

from six import print_

from pyfind.ncdu import Ncdu


def which(pgm):
    if os.path.isabs(pgm):
        if os.path.exists(pgm) and os.access(pgm, os.X_OK):
            return pgm
        else:
            return
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p


def environment_check(ncdu_path):
    if not which(ncdu_path):
        raise RuntimeError('{ncdu_path} command not found.'.format(**vars()))


Key = re.compile(r'(?P<size>\d+)(?P<unit>k|m|g)?', flags=re.I)


def size(s):
    """
    把输入转化成字节数
    """

    if s is None:
        return None
    if type(s) is str:
        result = Key.match(s)
        if not result:
            raise ValueError("{s} is not a regular input".format(**vars()))
        size = int(result.groupdict().get("size"))
        unit = result.groupdict().get("unit")
        if unit:
            if unit.lower() == "g":
                size *= 1024
                unit = "m"
            if unit.lower() == "m":
                size *= 1024
                unit = "k"
            if unit.lower() == "k":
                size *= 1024

        return size

    if type(s) is int or type(s) is float:
        return int(s)

    raise ValueError("size input must be str or int")


def convert_size_by_unit(size, unit):
    """
    把字节数转成对应单位
    """

    if unit == "g":
        return size / 1024 / 1024 / 1024

    if unit == "m":
        return size / 1024 / 1024

    if unit == "k":
        return size / 1024

    return size


class Find:
    """
    find 主类
    init
        初始化把所有参数都接受并作处理
    run
        用户接口方法
        返回为dict
        key 为 路径 ， value 为详细信息 （k->v， dict格式）

    show
        pretty 加强版的 run
    """

    DEFAULT_COLUMNS = ["dsize", "inode"]

    def __init__(self, path, mode="manual", min_size=None, max_size=None,
                 recurse=True, count=10,
                 columns=None, with_dir=None, **kwargs):
        self.path = path
        self.mode = mode
        self.min_size = size(min_size)
        self.max_size = size(max_size)
        self.recurse = recurse
        self.kwargs = kwargs
        self.columns = columns or self.DEFAULT_COLUMNS
        self.with_dir = with_dir
        self.count = count

    def _filter_size(self):
        ncdu = Ncdu(ncdu_path=self.kwargs.get("ncdu_path", None))
        result = ncdu.execute(self.path, recurse=self.recurse,
                              min_size=self.min_size, max_size=self.max_size,
                              with_dir=self.with_dir)
        return result

    def _size_top(self):
        ncdu = Ncdu(ncdu_path=self.kwargs.get("ncdu_path", None))
        result = ncdu.get_size_top(self.path, count=self.count)
        return result

    def _inode_top(self):
        ncdu = Ncdu(ncdu_path=self.kwargs.get("ncdu_path", None))
        result = ncdu.get_inode_top(self.path, count=self.count)
        return result

    def run(self):
        if self.mode == "manual":
            result = self._filter_size()
        elif self.mode == "sizetop":
            result = self._size_top()
        elif self.mode == "inodetop":
            result = self._inode_top()
        else:
            result = {}
        return result

    def show(self, sep="\t", end="\n", size_unit="m"):
        for path, detail in self.run().items():
            print_(path, end="")
            for key in self.columns:
                print_(sep, end="")
                if key == "dsize" and detail.get(key) is not None:
                    print_("{:0.2f}{}".format(
                        convert_size_by_unit(detail.get(key), size_unit),
                        size_unit),
                        end="")
                else:
                    print_(detail.get(key, "-"), end="")
            print_(end, end="")

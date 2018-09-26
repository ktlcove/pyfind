import re
import shutil

from pyfind.config import CONFIG
from pyfind.ncdu import Ncdu


def environment_check():
    if not shutil.which(CONFIG["ncdu_path"]):
        raise RuntimeError(f'{CONFIG["ncdu_path"]} command not found.')


Key = re.compile(r'(?P<size>\d+)(?P<unit>k|m|g)?', flags=re.I)


def size(s):
    if s is None:
        return None
    if type(s) is str:
        result = Key.match(s)
        if not result:
            raise ValueError(f"{s} is not a regular input")
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
    """

    DEFAULT_COLUMNS = ["dsize", "inode"]

    def __init__(self, path, min_size=None, max_size=None, recurse=True,
                 ext_args=None, columns=None, with_dir=None):
        self.path = path
        self.min_size = size(min_size)
        self.max_size = size(max_size)
        self.recurse = recurse
        self.ext_args = ext_args or {}
        self.columns = columns or self.DEFAULT_COLUMNS
        self.with_dir = with_dir

    def _filter_size(self):
        ncdu = Ncdu(ncdu_path=self.ext_args.get("ncdu_path", None))
        result = ncdu.execute(self.path, recurse=self.recurse,
                              min_size=self.min_size, max_size=self.max_size,
                              with_dir=self.with_dir)
        return result

    def run(self) -> dict:
        result = self._filter_size()
        return result

    def show(self, sep="\t", end="\n", size_unit="m"):
        for path, detail in self.run().items():
            print(f"{path}", end="")
            for key in self.columns:
                print(sep, end="")
                if key == "dsize":
                    print("{:0.2f}{}".format(
                        convert_size_by_unit(detail.get(key), size_unit),
                        size_unit),
                        end="")

                else:
                    print(detail.get(key, "-"), end="")
            print(end, end="")

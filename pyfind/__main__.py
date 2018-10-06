# coding:utf8
from pyfind import Find, environment_check
from pyfind.command_line import Arguments


def main():
    arguments = Arguments()

    arguments.add_argument("--mode", action="store",
                           dest="mode",
                           default="manual", type=str,
                           choices=["manual", "sizetop", "inodetop"],
                           help="筛选模式 默认为手动（manual） 需自定义各个筛选参数\n"
                                "sizetop: 获取指定目录下count个最大文件\n"
                                "inodetop: 获取指定目录下count个inode最多的目录")

    arguments.add_argument("--min-size", action="store", dest="min_size",
                           default=None, type=str,
                           help="过滤条件： 文件最小大小")

    arguments.add_argument("--max-size", action="store", dest="max_size",
                           default=None, type=str,
                           help="过滤条件： 文件最大大小")

    arguments.add_argument("--ncdu-path", action="store", dest="ncdu_path",
                           default="ncdu",
                           help="功能参数： ncdu execute file path")

    arguments.add_argument("--recurse", action="store_true", dest="recurse",
                           default=True,
                           help="功能条件： 递归检索， 如果为False 只检查当前目录")

    arguments.add_argument("--with-dir", action="store_true", dest="with_dir",
                           default=False,
                           help="功能条件： 目录类型是否是目标对象")

    arguments.add_argument("--count", action="store", dest="count",
                           default=10, type=int,
                           help="功能条件： 查询结果数量控制器")

    arguments.add_argument("--show-sep", action="store", dest="show_sep",
                           default="\t", type=str,
                           help="打印条件： 水平分隔符")

    arguments.add_argument("--show-end", action="store", dest="show_end",
                           default="\n", type=str,
                           help="打印条件： 垂直分隔符")

    arguments.add_argument("--show-size-unit", action="store",
                           dest="show_size_unit",
                           default="", type=str,
                           choices=["m", "g", "k", ""],
                           help="打印条件： 文件大小的单位")

    arguments.add_argument("--show-columns", action="store",
                           dest="show_columns",
                           default=None, type=str,
                           help="打印条件： 要显示的列`,`分割，"
                                "ino, asize, dsize, ino_count")

    arguments.add_argument("path", type=str,
                           help="查找的根目录")

    environment_check(arguments.args.ncdu_path)

    Find(arguments.args.path,
         mode=arguments.args.mode,
         recurse=arguments.args.recurse,
         min_size=arguments.args.min_size,
         max_size=arguments.args.max_size,
         with_dir=arguments.args.with_dir,
         columns=arguments.args.show_columns.split(",") \
             if arguments.args.show_columns else None,
         ncdu_path=arguments.args.ncdu_path,
         count=arguments.args.count). \
        show(sep=arguments.args.show_sep,
             end=arguments.args.show_end,
             size_unit=arguments.args.show_size_unit)


if __name__ == '__main__':
    main()

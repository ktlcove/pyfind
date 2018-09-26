from pyfind import environment_check, Find
from pyfind.command_line import Arguments

if __name__ == '__main__':
    environment_check()

    arguments = Arguments()
    arguments.add_argument("--min-size", action="store", dest="min_size",
                           default=None, type=str,
                           help="过滤条件： 文件最小大小")

    arguments.add_argument("--max-size", action="store", dest="max_size",
                           default=None, type=str,
                           help="过滤条件： 文件最大大小")

    arguments.add_argument("--recurse", action="store_true", dest="recurse",
                           default=True,
                           help="功能条件： 递归检索， 如果为False 只检查当前目录")

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
                           help="打印条件： 垂直分隔符")

    arguments.add_argument("--show-columns", action="store",
                           dest="show_columns",
                           default=None, type=str,
                           help="打印条件： 要显示的列`,`分割，"
                                "目前有俩(inode,asize)")

    arguments.add_argument("path", type=str,
                           help="run find in this dir")

    r = Find(arguments.args.path,
             recurse=arguments.args.recurse,
             min_size=arguments.args.min_size,
             max_size=arguments.args.max_size,
             columns=arguments.args.show_columns.split(",") \
                 if arguments.args.show_columns else None). \
        show(sep=arguments.args.show_sep,
             end=arguments.args.show_end,
             size_unit=arguments.args.show_size_unit)

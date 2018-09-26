# pyfind

find 的 python实现（暂时只实现了size得上下限）

## install
```bash
git clone https://github.com/ktlcove/pyfind.git
cd pyfind
pip install .
```

above command will create a executable file in /path/to/your/python/bin

## basic usage of this module
```
pyfind -h
usage: python -m pyfind [-h] [--min-size MIN_SIZE] [--max-size MAX_SIZE]
                        [--ncdu-path NCDU_PATH] [--recurse] [--with-dir]
                        [--show-sep SHOW_SEP] [--show-end SHOW_END]
                        [--show-size-unit {m,g,k,}]
                        [--show-columns SHOW_COLUMNS]
                        path

positional arguments:
  path                  查找的根目录

optional arguments:
  -h, --help            show this help message and exit
  --min-size MIN_SIZE   过滤条件： 文件最小大小
  --max-size MAX_SIZE   过滤条件： 文件最大大小
  --ncdu-path NCDU_PATH
                        功能参数： ncdu execute file path
  --recurse             功能条件： 递归检索， 如果为False 只检查当前目录
  --with-dir            功能条件： 目录类型是否是目标对象
  --show-sep SHOW_SEP   打印条件： 水平分隔符
  --show-end SHOW_END   打印条件： 垂直分隔符
  --show-size-unit {m,g,k,}
                        打印条件： 文件大小的单位
  --show-columns SHOW_COLUMNS
                        打印条件： 要显示的列`,`分割，目前有俩(inode,asize)
```


## example usage and success output
```bash
pyfind --min-size=512m --show-size-unit=g /
/System/Library/Speech/Voices/Ting-Ting.SpeechVoice/Contents/Resources/PCMWave	0.59g	8590906590
/System/Library/Caches/com.apple.coresymbolicationd/data	6.36g	8603462983
/private/var/db/dyld/dyld_shared_cache_x86_64h	1.09g	8604343544
/Users/ktlcove/Library/Android/sdk/system-images/android-27/google_apis/x86/system.img	2.51g	8592387592
/Users/ktlcove/Library/Android/sdk/system-images/android-27/google_apis/x86/userdata.img	0.55g	8592387533
/Users/ktlcove/Library/Containers/com.docker.docker/Data/vms/0/Docker.raw	3.19g	8604456973
...
```

# todo:
    can't run in python 2.7
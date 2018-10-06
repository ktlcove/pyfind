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
usage: pyfind [-h] [--mode {manual,sizetop,inodetop}] [--min-size MIN_SIZE]
              [--max-size MAX_SIZE] [--ncdu-path NCDU_PATH] [--recurse]
              [--with-dir] [--count COUNT] [--show-sep SHOW_SEP]
              [--show-end SHOW_END] [--show-size-unit {m,g,k,}]
              [--show-columns SHOW_COLUMNS]
              path

positional arguments:
  path                  查找的根目录

optional arguments:
  -h, --help            show this help message and exit
  --mode {manual,sizetop,inodetop}
                        筛选模式 默认为手动（manual）
                        需自定义各个筛选参数 sizetop:
                        获取指定目录下count个最大文件 inodetop:
                        获取指定目录下count个inode最多的目录
  --min-size MIN_SIZE   过滤条件： 文件最小大小
  --max-size MAX_SIZE   过滤条件： 文件最大大小
  --ncdu-path NCDU_PATH
                        功能参数： ncdu execute file path
  --recurse             功能条件： 递归检索， 如果为False
                        只检查当前目录
  --with-dir            功能条件： 目录类型是否是目标对象
  --count COUNT         功能条件： 查询结果数量控制器
  --show-sep SHOW_SEP   打印条件： 水平分隔符
  --show-end SHOW_END   打印条件： 垂直分隔符
  --show-size-unit {m,g,k,}
                        打印条件： 文件大小的单位
  --show-columns SHOW_COLUMNS
                        打印条件： 要显示的列`,`分割，ino, asize,
                        dsize, ino_count
```


## example usage and success output
```bash
# 手动检索(manual)
pyfind --min-size=512m --show-size-unit=g /
/System/Library/Speech/Voices/Ting-Ting.SpeechVoice/Contents/Resources/PCMWave	0.59g	8590906590
/System/Library/Caches/com.apple.coresymbolicationd/data	6.36g	8603462983
/private/var/db/dyld/dyld_shared_cache_x86_64h	1.09g	8604343544
/Users/ktlcove/Library/Android/sdk/system-images/android-27/google_apis/x86/system.img	2.51g	8592387592
/Users/ktlcove/Library/Android/sdk/system-images/android-27/google_apis/x86/userdata.img	0.55g	8592387533
/Users/ktlcove/Library/Containers/com.docker.docker/Data/vms/0/Docker.raw	3.19g	8604456973
...

# 获取指定目录inode 排名(inodetop)
pyfind --mode=inodetop  --show-columns="ino_count,ino" /
# 路径 文件数 自己inode号
/	4362320	2
/Users	1737273	418000
/Users/ktlcove	1737249	736721
/Applications	1370364	8589934650
/Users/ktlcove/Library	995874	741608
/Applications/Xcode.app	611910	8604788475
/Applications/Xcode.app/Contents	611909	8604788476
/Applications/Xcode.app/Contents/Developer	588880	8604791087
/Users/ktlcove/Library/Mail	571121	797694
/Users/ktlcove/Library/Mail/V5	571118	797697

# 获取指定目录 大文件排名(sizetop)
pyfind --mode=sizetop  --count=5 /
/Users/ktlcove/Downloads/Avengers.Infinity.War.2018.720p.BluRay.x264-SPARKS[rarbg]/Avengers.Infinity.War.2018.720p.BluRay.x264-SPARKS.mkv	7051575296.00	8603503532
/Users/ktlcove/Library/Containers/com.docker.docker/Data/vms/0/Docker.raw	3429937152.00	8604456973
/Users/ktlcove/Library/Android/sdk/system-images/android-27/google_apis/x86/system.img	2691883008.00	8592387592
/Users/ktlcove/.minikube/machines/minikube/minikube.rawdisk	2513506304.00	8604464569
/Users/ktlcove/Downloads/AdobePhotoshopCC2018.zip	1778409472.00	8603020194


```
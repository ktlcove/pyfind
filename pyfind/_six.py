import sys

if sys.version_info.major == 3:
    import subprocess

    getstatusoutput = subprocess.getstatusoutput

else:
    import commands

    getstatusoutput = commands.getstatusoutput

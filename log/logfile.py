#coding:gbk

from trace import *
try:
    import log
except:
    import sys
    sys.path.append("..")
    import log


class FileOutput(Output):
    def __init__(self, logfile):
        Output.__init__(self)
        try:
            self.mFile = open(logfile, "w")
            self.mFile.truncate(0)
        except Exception as e:
            log.error(e)

    def flush(self):
        self.mFile.flush()

    def onTrace(self, msg, level):
        logStr = ""
        if level == levelTrace:
            logStr = "[trace] %s"%msg
        elif level == levelHintHint:
            pass
        elif level == levelHintGood:
            logStr = "[good] %s"%msg
        elif level == levelWarning:
            logStr = "[warning] %s"%msg
        elif level == levelError:
            logStr = "[error] %s"%msg
        elif level == levelEmphasize:
            logStr = "[Emphasize] %s"%msg

        if logStr != "":
            self.mFile.write("%s\n"%logStr)


if __name__ == "__main__":
    o = FileOutput("log.log")
    o.onTrace("trace", levelTrace)
    o.onTrace("hint", levelHintHint)

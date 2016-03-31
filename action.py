#coding=gbk

import time, os, shutil
import log
import mclient as mc

class QuitAction:
    def run(self):
        return 1

class HintAction(mc.Command):
    def __init__(self, hintStr):
        self.mName = hintStr

    def run(self):
        log.hint(self.mName)
        return 0

class OpenCloudIndex(mc.Command):
    def __init__(self, hintStr):
        self.mName = hintStr

    def run(self):
        os.system("start ./filecloudindex/filecloudindex.exe")
        return 0

class CopySingleFile(mc.Command):
    def __init__(self, srcFile, tarDir):
        self.mSrcFile = srcFile
        self.mTarDir = tarDir
        self.mName = "复制%s至%s"%(srcFile, tarDir)

    def run(self):
        if os.path.exists(self.mSrcFile):
            self.preRun()
            shutil.copy(self.mSrcFile, self.mTarDir)
            self.postRun()
        else:
            log.error("文件%s不存在"%self.mSrcFile)

        return 0

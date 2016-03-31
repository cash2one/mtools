#coding=gbk

DefaultCdnDir = "/Res_Weiduan"
DefaultResDir = "../Data"

import util
from command import *
from migrate import *
from optimize import *


class MigrateRes(Command):
    def __init__(self, srcDir, tarDir, rebuildSrcDir = False):
        Command.__init__(self)

        self.mName = "资源迁移：%s -> %s"%(srcDir, tarDir)
        self.mSrcDir = srcDir
        self.mTarDir = tarDir
        self.mRebuildSrcDir = rebuildSrcDir

    def run(self):
        self.preRun()
        migrateRes(self.mSrcDir, self.mTarDir, self.mRebuildSrcDir)
        self.postRun()
        return 0


class RestoreMustFile(Command):
    def __init__(self):
        Command.__init__(self)
        self.mName = "恢复必要资源"

    def run(self):
        self.preRun()
        moveBackMustFile(DefaultResDir, DefaultCdnDir)
        self.postRun()
        return 0


class Optimization(Command):
    def __init__(self):
        Command.__init__(self)
        self.mName = "体验优化"

    def run(self):
        self.preRun()
        optimize(DefaultResDir, DefaultCdnDir)
        self.postRun()
        return 0


class UnlinkCommand(Command):
    def __init__(self, dirName, suffix):
        Command.__init__(self)
        self.mSuffix = suffix
        self.mDir = dirName
        self.mName = "删除%s文件"%suffix

    def run(self):
        self.preRun()
        util.unlinkRes(self.mDir, self.mSuffix)
        self.postRun()
        return 0



CmdId_MigrateToCdn = 1
CmdId_MigrateToRes = 2
CmdId_RestoreMustFile = 3
CmdId_Optimize = 4
CmdId_UnlinkZip = 5

GlobalCmds = {
    CmdId_MigrateToCdn:MigrateRes(DefaultResDir, DefaultCdnDir, True),
    CmdId_MigrateToRes:MigrateRes(DefaultCdnDir, DefaultResDir),
    CmdId_RestoreMustFile:RestoreMustFile(),
    CmdId_Optimize:Optimization(),
    CmdId_UnlinkZip:UnlinkCommand(DefaultResDir, "zip")
}

#coding=gbk

import time, os, shutil
import log
import mclient as mc

ActionGroup = mc.CommandGroup

class QuitAction:
    def run(self):
        return 1

class HintAction(mc.Command):
    def __init__(self, hintStr):
        self.mName = "打开打包工具(生成后再执行3)"

    def run(self):
        log.hint(self.mName)

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


_g_inputAction = {
    "1":ActionGroup(mc.GlobalCmds[mc.CmdId_MigrateToCdn], mc.GlobalCmds[mc.CmdId_RestoreMustFile]),
    "2":OpenCloudIndex("打开打包工具(生成后再执行3)"),
    "3":CopySingleFile("%s/fileindex.csv"%(mc.DefaultCdnDir), "./filecloud"),
    "4":mc.GlobalCmds[mc.CmdId_MigrateToRes],
    "q":QuitAction(),
}

_g_hintMsg  = "------------------------------------------------------------------------\n"
_g_hintMsg += "生成所有Zip文件:\n"
tmpActKey = ["1", "2", "3", "4",]
for key in tmpActKey:
    _g_hintMsg += "%s. %s\n"%(key, _g_inputAction[key].getName())

# _g_hintMsg += "1. %s\n"%_g_inputAction["1"].getName()
# _g_hintMsg += "2. %s\n"%_g_inputAction["2"].getName()
# _g_hintMsg += "%-35s%-35s\n"%("3. 复制配置文件到云服务器", "4. 微端资源迁回")

_g_hintMsg += "\n微端打包:\n"
_g_hintMsg += "%-35s%-35s\n"%("101. 生成最小微端资源集", "102. 体验优化")
_g_hintMsg += "%-35s%-35s\n"%("103. 打包(类似大端打包方式)", "104. 微端资源迁回")

_g_hintMsg += "\n打包更新资源(CDN)\n"
_g_hintMsg += "%-35s%-35s\n"%("201. 迁移微端资源到%s目录"%mc.GlobalCmds[mc.CmdId_MigrateToCdn].getName(), "202. 打开打包工具")

_g_hintMsg += "\n其他命令:\n"
_g_hintMsg += "%-35s\n"%("51. 删除Data目录下的所有Zip文件")
_g_hintMsg += "------------------------------------------------------------------------"

def main():
    log.output2Console()

    if not os.path.exists("../Data"):
        log.error("目录结构不正确")
        raw_input("按任意键退出")
        return

    while True:
        try:
            log.hint(_g_hintMsg)
            x = raw_input(">>")

            if _g_inputAction.has_key(x):
                exitCode = _g_inputAction[x].run()
                if exitCode != 0:
                    break

            continue

            if x == 101:
                x = 1
            elif x == 104:
                x = 4
            elif x == 201:
                x = 1
            elif x == 202:
                x = 2

            if x == 1:
                begTime = time.time()
                mtools.mvResToCdnDir()
                optimize.moveBackMustFile()
                endTime = time.time()
                log.good("Done! Time:%f\n"%(endTime-begTime))
            elif x == 2:
                os.system("start ./filecloudindex/filecloudindex.exe")
            elif x == 3:
                csvFile = "fileindex.csv"
                csvPath = "%s/%s"%(mtools.MCDNDIR, csvFile)
            elif x == 4:
                begTime = time.time()
                curDir = os.path.abspath(".")
                if os.access("%s"%mtools.MCDNDIR, os.F_OK):
                    mtools.moveBackRes()
                    endTime = time.time()
                    log.good("Done! Time:%f\n"%(endTime-begTime))
                else:
                    log.error("%s文件夹不存在\n"%mtools.MCDNDIR)

            elif x == 102:
                begTime = time.time()
                optimize.optimize()
                endTime = time.time()
                log.good("Done! Time:%f!\n"%(endTime-begTime))
            elif x == 103:
                log.error("(⊙︿⊙) 打包好后，记得执行下一步哦！")

            elif x == 51:
                begTime = time.time()
                unlinkRes(mtools.MRESDIR, "(zip)")
                endTime = time.time()
                log.good("Done! Time:%f!\n"%(endTime-begTime))
            else:
                break
        except Exception as e:
            log.error(e)


if __name__ == '__main__':
    main()

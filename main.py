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
        self.mName = "�򿪴������(���ɺ���ִ��3)"

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
        self.mName = "����%s��%s"%(srcFile, tarDir)

    def run(self):
        if os.path.exists(self.mSrcFile):
            self.preRun()
            shutil.copy(self.mSrcFile, self.mTarDir)
            self.postRun()
        else:
            log.error("�ļ�%s������"%self.mSrcFile)

        return 0


_g_inputAction = {
    "1":ActionGroup(mc.GlobalCmds[mc.CmdId_MigrateToCdn], mc.GlobalCmds[mc.CmdId_RestoreMustFile]),
    "2":OpenCloudIndex("�򿪴������(���ɺ���ִ��3)"),
    "3":CopySingleFile("%s/fileindex.csv"%(mc.DefaultCdnDir), "./filecloud"),
    "4":mc.GlobalCmds[mc.CmdId_MigrateToRes],
    "q":QuitAction(),
}

_g_hintMsg  = "------------------------------------------------------------------------\n"
_g_hintMsg += "��������Zip�ļ�:\n"
tmpActKey = ["1", "2", "3", "4",]
for key in tmpActKey:
    _g_hintMsg += "%s. %s\n"%(key, _g_inputAction[key].getName())

# _g_hintMsg += "1. %s\n"%_g_inputAction["1"].getName()
# _g_hintMsg += "2. %s\n"%_g_inputAction["2"].getName()
# _g_hintMsg += "%-35s%-35s\n"%("3. ���������ļ����Ʒ�����", "4. ΢����ԴǨ��")

_g_hintMsg += "\n΢�˴��:\n"
_g_hintMsg += "%-35s%-35s\n"%("101. ������С΢����Դ��", "102. �����Ż�")
_g_hintMsg += "%-35s%-35s\n"%("103. ���(���ƴ�˴����ʽ)", "104. ΢����ԴǨ��")

_g_hintMsg += "\n���������Դ(CDN)\n"
_g_hintMsg += "%-35s%-35s\n"%("201. Ǩ��΢����Դ��%sĿ¼"%mc.GlobalCmds[mc.CmdId_MigrateToCdn].getName(), "202. �򿪴������")

_g_hintMsg += "\n��������:\n"
_g_hintMsg += "%-35s\n"%("51. ɾ��DataĿ¼�µ�����Zip�ļ�")
_g_hintMsg += "------------------------------------------------------------------------"

def main():
    log.output2Console()

    if not os.path.exists("../Data"):
        log.error("Ŀ¼�ṹ����ȷ")
        raw_input("��������˳�")
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
                    log.error("%s�ļ��в�����\n"%mtools.MCDNDIR)

            elif x == 102:
                begTime = time.time()
                optimize.optimize()
                endTime = time.time()
                log.good("Done! Time:%f!\n"%(endTime-begTime))
            elif x == 103:
                log.error("(�Ѧ��) ����ú󣬼ǵ�ִ����һ��Ŷ��")

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

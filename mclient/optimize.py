# coding=gbk

import csv
import log
import util


def optimizeActorAni():
    """�Ż�΢�ͻ��˶�������"""
    dirList = [
        "Player_M_ck", "Player_M_ck_gz", "Player_W_ck", "Player_W_ck_gz",
        "Player_M_ds", "Player_M_ds_gz", "Player_W_ds", "Player_W_ds_gz",
        "Player_M_fs", "Player_M_fs_gz", "Player_W_fs", "Player_W_fs_gz",
        "Player_M_zj", "Player_M_zj_gz", "Player_W_zj", "Player_W_zj_gz",
    ]

    curDir = os.path.abspath(".")
    tarDir = os.path.abspath(MRESDIR)
    os.chdir(MCDNDIR)
    for name in dirList:
        dirName = "./Models/" + name
        if os.path.exists(dirName):
            mvRes(dirName, tarDir, "(fb)")
        else:
            log.error("Ŀ¼ %s%s ������"%(MCDNDIR, dirName))
    os.chdir(curDir)
    log.trace("current dir:%s"%os.path.abspath("."))


def optimizeAllAni():
    curDir = os.path.abspath(".")
    tarDir = os.path.abspath(MRESDIR)
    os.chdir(MCDNDIR)
    mvRes("./Models", tarDir, "(fb)")
    os.chdir(curDir)


def optimizeByCsv(csvPath):
    csvObj = csv.reader(file(csvPath, 'rb'))

    absResPath = os.path.abspath(MRESDIR)
    curDir = os.path.abspath(".")
    for line in csvObj:
        if len(line) > 0:
            os.chdir(MCDNDIR)
            pathname = line[0]
            if not os.path.exists(pathname):
                log.error("�ļ� %s/%s ������"%(MCDNDIR, pathname))
                os.chdir(curDir)
                continue

            targetPath = os.path.join(absResPath, pathname)
            log.trace("from:"+pathname+"  to:"+targetPath)
            try:
                os.unlink(targetPath)
            except:
                pass
            os.renames(pathname, targetPath)
            os.chdir(curDir)
    log.trace("current dir:%s"%os.path.abspath("."))


def visitCsvFile(pathname, param):
    lpathname = pathname.lower()
    pattern = re.compile(param["pattern"])
    m = pattern.match(lpathname)
    if m:
        optimizeByCsv(pathname)


def optimize():
    # �������������Ż�
    optimizeActorAni()
    # optimizeAllAni()

    # ����csv�����Ż�����
    param = {}
    param["pattern"] = ".*optimize.*\.csv$"
    walktree("./", visitCsvFile, param)


def moveBackMustFile():
    param = {}
    param["pattern"] = ".*mustfile.*\.csv$"
    walktree("./", visitCsvFile, param)


if __name__ == '__main__':
    moveBackMustFile()
    os.system("pause")

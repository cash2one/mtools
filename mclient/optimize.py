# coding=gbk

import csv, re, os
import log
import util


def optimizeActorAni(resDir, cdnDir):
    """优化微客户端动画播放"""
    log.good("回滚角色动画资源 ...")
    dirList = [
        "Player_M_ck", "Player_M_ck_gz", "Player_W_ck", "Player_W_ck_gz",
        "Player_M_ds", "Player_M_ds_gz", "Player_W_ds", "Player_W_ds_gz",
        "Player_M_fs", "Player_M_fs_gz", "Player_W_fs", "Player_W_fs_gz",
        "Player_M_zj", "Player_M_zj_gz", "Player_W_zj", "Player_W_zj_gz",
    ]

    curDir = os.path.abspath(".")
    tarDir = os.path.abspath(resDir)
    os.chdir(cdnDir)
    for name in dirList:
        dirName = "./Models/" + name
        if os.path.exists(dirName):
            util.mvRes(dirName, tarDir, "(fb)")
        else:
            log.error("目录 %s%s 不存在"%(cdnDir, dirName))
    os.chdir(curDir)
    log.good("回滚角色动画资源 结束")


def optimizeAllAni(resDir, cdnDir):
    curDir = os.path.abspath(".")
    tarDir = os.path.abspath(resDir)
    os.chdir(cdnDir)
    util.mvRes("./Models", tarDir, "(fb)")
    os.chdir(curDir)


def optimizeByCsv(csvPath, resDir, cdnDir):
    log.good("处理 %s ..."%csvPath)
    csvObj = csv.reader(file(csvPath, 'rb'))

    absResPath = os.path.abspath(resDir)
    curDir = os.path.abspath(".")
    for line in csvObj:
        if len(line) > 0:
            os.chdir(cdnDir)
            pathname = line[0]
            if not os.path.exists(pathname):
                # log.error("文件 %s/%s 不存在"%(cdnDir, pathname))
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

    log.good("处理 %s 结束"%csvPath)
    # log.trace("current dir:%s"%os.path.abspath("."))


def visitCsvFile(pathname, param):
    lpathname = pathname.lower()
    pattern = re.compile(param["pattern"])
    resDir = param["resdir"]
    cdnDir = param["cdndir"]
    m = pattern.match(lpathname)
    if m:
        optimizeByCsv(pathname, resDir, cdnDir)


def optimize(resDir, cdnDir):
    # 动画播放体验优化
    optimizeActorAni(resDir, cdnDir)
    # optimizeAllAni()

    # 依据csv表来优化体验
    param = {}
    param["pattern"] = ".*optimize.*\.csv$"
    param["resdir"] = resDir
    param["cdndir"] = cdnDir
    util.walktree("./", visitCsvFile, param)


def moveBackMustFile(resDir, cdnDir):
    param = {}
    param["pattern"] = ".*mustfile.*\.csv$"
    param["resdir"] = resDir
    param["cdndir"] = cdnDir
    util.walktree("./", visitCsvFile, param)


if __name__ == '__main__':
    os.system("pause")

# coding=gbk

import os
import util

def migrateRes(relSrcDir, tarDir, resList, rebuildSrcDir = False):
    """资源迁移"""

    curDir = os.path.abspath(".")
    srcDir = os.path.abspath(relSrcDir)
    tarDir = os.path.abspath(tarDir)
    for key, val in resList.items():
        for item in val:
            strdir = item[0]
            strpat = item[1]
            igndir = len(item) > 2 and item[2] or ""
            os.chdir(srcDir)
            util.mvRes(strdir, tarDir, strpat, igndir)
            os.chdir(curDir)

    if rebuildSrcDir:
        dirList = resList.keys()
        for name in dirList:
            dirname = os.path.join(relSrcDir, name)
            if not os.path.exists(dirname):
                while True:
                    try:
                        os.makedirs(dirname)
                        break
                    except:
                        pass
                    # print("mkdir %s failed, current directory:%s"%(dirname, os.path.abspath(".")))

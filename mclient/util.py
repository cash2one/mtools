# coding=gbk

import os, sys, re, shutil
import traceback
import log
from stat import *


def walktree(top, callback, param):
    if not os.access(top, os.F_OK):
        return 0

    if param.has_key("igndir") and top.find(param["igndir"]) >= 0:
        return 0

    filecount = 0
    for f in os.listdir(top):
        if f.find(".svn") != -1:
            continue

        pathname = os.path.join(top, f)
        try:
            st = os.stat(pathname)
            if not st:
                continue

            mode = st.st_mode
            if S_ISDIR(mode):
                filecount += walktree(pathname, callback, param)
            elif S_ISREG(mode):
                try:
                    callback(pathname, param)
                except Exception as e:
                    log.error(e)
            if os.access(pathname, os.F_OK):
                filecount += 1
        except:
            continue
    return filecount


def cbUnlinkFile(pathname, param):
    pattern = param["pattern"]
    lpathname = pathname.lower()
    m = pattern.match(lpathname)
    if m:
        os.unlink(pathname)
        log.trace("unlink:%s"%pathname)


def unlinkRes(srcDir, suffix, igndir=""):
    param = {}
    param["pattern"] = re.compile(".*\.(%s$)"%suffix)
    if igndir != "":
        param["igndir"] = igndir
    walktree(srcDir, cbUnlinkFile, param)


def moveFile(pathname, param):
    pattern = param["pattern"]
    initDir = param["initdir"]
    tarDir = param["tardir"]
    lpathname = pathname.lower()
    m = pattern.match(lpathname)
    if m:
        targetPath = os.path.join(tarDir, pathname)
        log.trace("from:"+pathname+"  to:"+targetPath)
        try:
            os.unlink(targetPath)
        except:
            pass

        os.renames(pathname, targetPath)
        os.chdir(initDir)


def mvRes(srcDir, tarDir, suffix, igndir=""):
    param = {}
    param["pattern"] = re.compile(".*\.%s$"%suffix)
    param["initdir"] = os.path.abspath(".")
    param["tardir"] = tarDir
    if igndir != "":
        param["igndir"] = igndir
    walktree(srcDir, moveFile, param)

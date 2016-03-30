#coding=gbk

import time
try:
    import log
except:
    import sys
    sys.path.append("..")
    import log


class Command:
    def __init__(self):
        self.mName = "AbsCommand"
        self.mRunTime = 0

    def run(self):
        return 0

    def preRun(self):
        self.mRunTime = time.time()

    def postRun(self):
        log.good("命令：%s"%self.getName())
        log.good("执行时长:%f\n"%(time.time()-self.mRunTime))

    def getName(self):
        return self.mName


class CommandGroup(Command):
    def __init__(self, *cmds):
        Command.__init__(self)

        self.mName = "Group Command"
        self.mCmds = []
        if cmds:
            self.mCmds.extend(cmds)

    def addCmd(self, cmd):
        self.mCmds.append(cmd)

    def getName(self):
        name = ""
        for cmd in self.mCmds:
            if name != "":
                name = "%s->[%s]"%(name, cmd.getName())
            else:
                name = "[%s]"%cmd.getName()

        return name

    def run(self):
        self.preRun()
        exitCode = 0
        for cmd in self.mCmds:
            exitCode = exitCode | cmd.run()
        self.postRun()
        return exitCode


class TestCommand(Command):
    def __init__(self):
        Command.__init__(self)
        self.mName = "TestCommand"

    def run(self):
        print("test")
        return 0



if __name__ == "__main__":
    import os
    os.chdir("..")
    cmdGroup = CommandGroup(TestCommand(), TestCommand())
    cmdGroup.run()
    print(cmdGroup.getName())

#coding=gbk

import time, os, shutil
import log
import mclient as mc
from action import *

ActionGroup = mc.CommandGroup


## ����
_g_inputAction = {
    "1":ActionGroup(mc.GlobalCmds[mc.CmdId_MigrateToCdn], mc.GlobalCmds[mc.CmdId_RestoreMustFile]),
    "2":OpenCloudIndex("�򿪴������(���ɺ���ִ��3)"),
    "3":CopySingleFile("%s/fileindex.csv"%(mc.DefaultCdnDir), "./filecloud"),
    "4":mc.GlobalCmds[mc.CmdId_MigrateToRes],

    "uzip":mc.GlobalCmds[mc.CmdId_UnlinkZip],

    "q":QuitAction(),
}

_g_inputAction["a"] = _g_inputAction["1"]
_g_inputAction["b"] = mc.GlobalCmds[mc.CmdId_Optimize]
_g_inputAction["c"] = HintAction("���(���ƴ�˴����ʽ)")
_g_inputAction["d"] = _g_inputAction["4"]
_g_inputAction["ab"] = ActionGroup(_g_inputAction["a"], _g_inputAction["b"])

_g_inputAction["ta"] = mc.GlobalCmds[mc.TempSceneCmd_MigrateToRoot]
_g_inputAction["tb"] = mc.GlobalCmds[mc.TempSceneCmd_MigrateToRes]

_g_inputAction["pa"] = mc.GlobalCmds[mc.CmdId_Partner_MigrateToCdn]
_g_inputAction["pb"] = mc.GlobalCmds[mc.CmdId_Partner_PatchRes]
_g_inputAction["pd"] = mc.GlobalCmds[mc.CmdId_Partner_MigrateToRes]


## ��ʾ
_g_helpinfo  = "------------------------------------------------------------------------\n"
_g_helpinfo += "��ȡ/ѹ��:\n"
tmpActKey = ["1", "2", "3", "4",]
for key in tmpActKey:
    _g_helpinfo += "%s: %s\n"%(key, _g_inputAction[key].getName())

_g_helpinfo += "\n��ȡ/����������Դ(�����Ż�):\n"
tmpActKey = ["a", "b", "c", "d", "ab"]
for key in tmpActKey:
    _g_helpinfo += "%s: %s\n"%(key, _g_inputAction[key].getName())

_g_helpinfo += "\n��������:\n"
tmpActKey = ["uzip",]
for key in tmpActKey:
    _g_helpinfo += "%s: %s\n"%(key, _g_inputAction[key].getName())

_g_helpinfo += "\n��ʱ����:\n"
tmpActKey = ["ta", "tb",]
for key in tmpActKey:
    _g_helpinfo += "%s: %s\n"%(key, _g_inputAction[key].getName())

_g_helpinfo += "\n�������:\n"
tmpActKey = ["pa", "pb", "pd"]
for key in tmpActKey:
    _g_helpinfo += "%s: %s\n"%(key, _g_inputAction[key].getName())
_g_helpinfo += "------------------------------------------------------------------------"

_g_inputAction["h"] = HintAction(_g_helpinfo)

def main():
    log.output2Console()

    if not os.path.exists("../Data"):
        log.error("Ŀ¼�ṹ����ȷ")
        raw_input("��������˳�")
        return

    while True:
        try:
            # log.hint(_g_helpinfo)
            log.flushTrace()
            x = raw_input(">>")

            if _g_inputAction.has_key(x):
                exitCode = _g_inputAction[x].run()
                if exitCode != 0:
                    break
        except Exception as e:
            log.error(e)


if __name__ == '__main__':
    main()
